from collections import defaultdict
from datetime import datetime
import itertools
import os
import string
from time import time
import warnings

import numpy as np
import pandas as pd
from tabulate import tabulate

from chaiverse.competition import get_competitions, COMPETITION_TYPE_CONFIGURATION
from chaiverse.feedback import get_feedback, is_submission_updated
from chaiverse.login_cli import auto_authenticate
from chaiverse.utils import print_color, cache, get_submissions, distribute_to_workers


DEFAULT_MAX_WORKERS = max(1, min(20, os.cpu_count() - 3))
PUBLIC_LEADERBOARD_MINIMUM_FEEDBACK_COUNT = 0

MODEL_EVAL_SCORE_COLS = ['stay_in_character', 'user_preference', 'entertaining']

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)
pd.set_option("display.colheader_justify","center")

warnings.filterwarnings('ignore', 'Mean of empty slice')


def display_leaderboard(
    developer_key=None,
    regenerate=False,
    detailed=False,
    max_workers=DEFAULT_MAX_WORKERS,
):
    default_competition = {
        'id': 'Default',
        'type': 'default',
        'submission_start_date': '2024-01-15', # temp workaround
        'submission_end_date': '2025-01-15', # temp workaround
    }

    df = display_competition_leaderboard(
        competition=default_competition,
        detailed=detailed,
        regenerate=regenerate,
        developer_key=developer_key,
        max_workers=max_workers,
    )
    return df


def display_competition_leaderboard(
    competition=None,
    detailed=False,
    regenerate=False, 
    developer_key=None,
    max_workers=DEFAULT_MAX_WORKERS
):
    competition = competition if competition else get_competitions()[-1]
    competition_type = competition.get('type') or 'submission_closed_feedback_round_robin'
    fetch_feedback = competition_type != 'default'

    submission_date_range = (
        competition.get('submission_start_date') or '2024-01-05', # temp work around
        competition.get('submission_end_date') or '2024-01-13', # temp work around
    )
    feedback_date_range = (
        competition.get('start_time') or 0,
        competition.get('end_time') or float('inf')
    )
    submission_ids = competition.get('submissions')
    competition_id = competition.get('id')
    display_title = f'{competition_id} Leaderboard'

    df = cache(get_leaderboard, regenerate)(
        developer_key=developer_key,
        max_workers=max_workers,
        submission_date_range=submission_date_range,
        feedback_date_range=feedback_date_range,
        submission_ids=submission_ids,
        fetch_feedback=fetch_feedback
        )

    if len(df) > 0:
        display_df = df.copy()
        display_df = get_display_leaderboard(
            display_df, 
            detailed=detailed, 
            competition_type=competition_type
        )
        _pprint_leaderboard(display_df, display_title)
    else:
        print('No eligible submissions found!')
    return df


def get_leaderboard(
        developer_key=None,
        max_workers=DEFAULT_MAX_WORKERS,
        submission_date_range=None,
        feedback_date_range=None,
        submission_ids=None,
        fetch_feedback=False,
        ):
    submissions = get_submissions(developer_key, submission_date_range)
    submissions = _filter_submissions(submissions, submission_ids) if submission_ids else submissions
    feedback_timestamp_start = feedback_date_range[0]
    feedback_timestamp_end = feedback_date_range[1]
    df = distribute_to_workers(
        get_leaderboard_row,
        submissions.items(),
        developer_key=developer_key,
        feedback_time_range=(feedback_timestamp_start, feedback_timestamp_end),
        max_workers=max_workers,
        fetch_feedback=fetch_feedback
    )
    df = pd.DataFrame(df)
    if len(df):
        df = _get_filled_leaderboard(df)
        df.index = np.arange(1, len(df)+1)
    return df


def get_display_leaderboard(df, detailed, competition_type):
    competition_configuration = COMPETITION_TYPE_CONFIGURATION[competition_type]
    sort_params = competition_configuration['sort_params']
    output_columns = competition_configuration['output_columns']

    df = df if detailed else _get_ranked_leaderboard(df, sort_params)
    df = df if detailed else _get_deduped_leaderboard(df)
    df = _get_formatted_leaderboard(df)
    df = df if detailed else df[output_columns]
    df.index = np.arange(1, len(df)+1)
    return df


def _filter_submissions(submissions, submission_ids):
    filtered_submissions = {
        submission_id: data
        for submission_id, data in submissions.items()
        if submission_id in submission_ids
    }
    return filtered_submissions


def get_leaderboard_row(submission_item, developer_key=None, feedback_time_range=None, fetch_feedback=False):
    submission_id, meta_data = submission_item
    total_feedback_count = meta_data['thumbs_up'] + meta_data['thumbs_down']
    is_updated = is_submission_updated(submission_id, total_feedback_count)
    feedback = {"total_feedback_count": total_feedback_count}
    if fetch_feedback:
        feedback = get_submission_feedback(submission_id, developer_key, reload=is_updated, feedback_time_range=feedback_time_range)
    return {'submission_id': submission_id, **meta_data, **feedback}


@auto_authenticate
def get_submission_feedback(submission_id, developer_key, reload=True, feedback_time_range=None):
    feedback = get_feedback(submission_id, developer_key, reload=reload)
    feedback_metrics = FeedbackMetrics(feedback.raw_data)
    feedback_metrics.filter_for_timestamp_range(feedback_time_range)
    feedback_metrics.filter_duplicated_uid()
    metrics = calc_metrics(feedback_metrics)
    return metrics


def calc_metrics(feedback_metrics):
    metrics = {}
    if len(feedback_metrics.convo_metrics) > 0:
        metrics = {
            'mcl': feedback_metrics.mcl,
            'thumbs_up_ratio': feedback_metrics.thumbs_up_ratio,
            'thumbs_up_ratio_se': feedback_metrics.thumbs_up_ratio_se,
            'repetition': feedback_metrics.repetition_score,
            'total_feedback_count': feedback_metrics.total_feedback_count,
        }
    return metrics


class FeedbackMetrics():
    def __init__(self, feedback_data):
        feedback_dict = feedback_data['feedback']
        feedback_dict = _insert_server_timestamp(feedback_dict)
        self.feedbacks = list(feedback_dict.values())

    def filter_duplicated_uid(self):
        self.feedbacks = _filter_duplicated_uid_feedbacks(self.feedbacks)

    def filter_for_timestamp_range(self, feedback_time_range=None):
        (begin_time, end_time) = feedback_time_range if feedback_time_range else (0, float('inf'))
        self.feedbacks = [
            feedback for feedback in self.feedbacks
            if begin_time < feedback['server_timestamp'] < end_time 
        ]

    @property
    def convo_metrics(self):
        return [ConversationMetrics(feedback['messages']) for feedback in self.feedbacks]

    @property
    def thumbs_up_ratio(self):
        is_thumbs_up = [feedback['thumbs_up'] for feedback in self.feedbacks]
        thumbs_up = sum(is_thumbs_up)
        thumbs_up_ratio = np.nan if not thumbs_up else thumbs_up / len(is_thumbs_up)
        return thumbs_up_ratio

    @property
    def thumbs_up_ratio_se(self):
        num = self.thumbs_up_ratio * (1 - self.thumbs_up_ratio)
        denom = self.total_feedback_count**0.5
        se = np.nan if self.total_feedback_count < 2 else num / denom
        return se

    @property
    def total_feedback_count(self):
        return len(self.feedbacks)

    @property
    def mcl(self):
        return np.mean([m.mcl for m in self.convo_metrics])

    @property
    def repetition_score(self):
        scores = np.array([m.repetition_score for m in self.convo_metrics])
        is_public = np.array([feedback.get('public', True) for feedback in self.feedbacks])
        return np.nanmean(scores[is_public])


def _insert_server_timestamp(feedback_dict):
    for feedback_id, feedback in feedback_dict.items():
        feedback['server_timestamp'] = int(feedback_id.split('_')[-1])
    return feedback_dict


def _filter_duplicated_uid_feedbacks(feedbacks):
    user_feedbacks = defaultdict(list)
    for feedback in feedbacks:
        user_id = feedback["conversation_id"].split("_")[3]
        user_feedbacks[user_id].append(feedback)
    feedbacks = [metrics[0] for _, metrics in user_feedbacks.items()]
    return feedbacks


class ConversationMetrics():
    def __init__(self, messages):
        self.messages = messages

    @property
    def mcl(self):
        return len([m for m in self.messages if not m['deleted']])

    @property
    def repetition_score(self):
        responses = [m['content'] for m in self.messages if not self._is_from_user(m)]
        score = np.nan if len(responses) < 2 else get_repetition_score(responses)
        return score

    def _is_from_user(self, message):
        return '_bot' not in message['sender']['uid']


def get_repetition_score(responses):
    # average jaccard similarities over unigrams
    list_of_tokens = _tokenize_responses(responses)
    pairs = zip(list_of_tokens[:-1], list_of_tokens[1:])
    similarities = [_get_jaccard_similarity(set1, set2) for set1, set2 in pairs]
    return np.mean(similarities)


def _get_jaccard_similarity(set1, set2):
    intersection_len = len(set1.intersection(set2))
    union_len = len(set1.union(set2))
    return intersection_len / union_len


def _tokenize_responses(responses):
    return [set(_remove_punctuation(text).split()) for text in responses]


def _remove_punctuation(text):
    translation_table = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translation_table)
    if len(cleaned_text.split()) == 0:
        cleaned_text = '...'
    return cleaned_text.lower()


def _get_filled_leaderboard(df):
    # maintain backwards compatibility with model_name field
    _fill_default_value(df, 'model_name', df['submission_id'])
    _fill_default_value(df, 'is_custom_reward', False)
    for col in _get_filled_columns():
        _fill_default_value(df, col, None)
    return df


def _get_ranked_leaderboard(df, sort_params):
    df = _filter_submissions_with_few_feedback(df)
    df = _add_individual_rank(df, value_column='thumbs_up_ratio', rank_column='thumbs_up_rank', ascending=False)
    rank_columns = []
    for score_column in MODEL_EVAL_SCORE_COLS:
        rank_column = f'{score_column}_rank'
        rank_columns.append(rank_column)
        df = _add_individual_rank(df, value_column=score_column, rank_column=rank_column, ascending=False)
    df = _add_overall_rank(df, rank_columns=rank_columns)
    df = _sort(df, sort_params)
    return df


def _get_deduped_leaderboard(df):
    df = _get_submissions_with_unique_model(df)
    df = _get_submissions_with_unique_dev_id(df)
    return df


def _fill_default_value(df, field, default_value):
    if field not in df:
        df[field] = None
    if default_value is not None:
        df[field] = df[field].fillna(default_value)


def _get_formatted_leaderboard(df):
    df['timestamp'] = df.apply(lambda x: datetime.fromisoformat(x['timestamp']), axis=1)
    df['size'] = df.model_num_parameters.apply(_get_model_size)
    df['date'] = df['timestamp'].dt.date
    df.drop(['timestamp'], axis=1, inplace=True)
    df['is_custom_reward'] = df['is_custom_reward'].replace({
        True: '✅',
        False: '❌'
    })
    df = df.reset_index(drop=True)
    return df


def _get_model_size(num_parameters):
    size = f'{int(round(num_parameters/1e9,0))}' if num_parameters else 'n/a'
    return size


def _get_submissions_with_unique_model(df):
    df = df.drop_duplicates(subset=['model_repo', 'reward_repo'], keep='first')
    return df


def _filter_submissions_with_few_feedback(df):
    filtered_df = df[df.total_feedback_count >= PUBLIC_LEADERBOARD_MINIMUM_FEEDBACK_COUNT]
    return filtered_df


def _add_individual_rank(df, value_column, rank_column, ascending=True):
    df[rank_column] = df[value_column].rank(ascending=ascending, na_option='bottom')
    return df


def _add_overall_rank(df, rank_columns):
    ranks = [df[column] for column in rank_columns]
    overall_score = np.mean(ranks, axis=0)
    df.loc[:, 'overall_score'] = overall_score
    df.loc[:, 'overall_rank'] = df.overall_score.rank(na_option='bottom')
    return df


def _sort(df, sort_params):
    df = df.sort_values(**sort_params, na_position='last').reset_index(drop=True)
    return df


def _get_submissions_with_unique_dev_id(df):
    out = df.drop_duplicates('developer_uid', keep='first')
    return out


def _pprint_leaderboard(df, title):
    print_color(f'\n💎 {title}:', 'red')
    print(tabulate(df.round(3).head(30), headers=df.columns, numalign='center'))


def get_sorted_available_models(developer_key):
    models = get_submissions(developer_key=developer_key)
    available_models = [k for k, v in models.items() if v['status'] == 'deployed']
    sorted_available_models = sorted(available_models)
    return sorted_available_models


def _get_filled_columns():
    columns = []
    for competition_type in COMPETITION_TYPE_CONFIGURATION.keys():
        new_columns = COMPETITION_TYPE_CONFIGURATION[competition_type]['output_columns']
        columns.extend(new_columns)
    return columns