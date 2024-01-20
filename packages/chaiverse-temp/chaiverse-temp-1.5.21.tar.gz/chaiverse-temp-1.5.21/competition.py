import requests

from chaiverse.utils import get_url


COMPETITIONS_ENDPOINT = '/competitions'


COMPETITION_TYPE_CONFIGURATION = {}

COMPETITION_TYPE_CONFIGURATION['default'] = {
    "output_columns": [
        'developer_uid',
        'model_name',
        'is_custom_reward',
        'stay_in_character',
        'user_preference',
        'entertaining',
        'safety_score',
        "overall_rank",
        'size',
        'status',
        'submission_id',
    ],
    "sort_params": {
        "by": "overall_score",
        "ascending": True
    }
}

COMPETITION_TYPE_CONFIGURATION['submission_closed_feedback_round_robin'] = {
    "output_columns": [
        'developer_uid',
        'model_name',
        'thumbs_up_ratio',
        'overall_rank',
        'total_feedback_count',
        'repetition',
        'stay_in_character',
        'user_preference',
        'entertaining',
        'safety_score',
        'is_custom_reward',
        'submission_id',
        'size',
    ],
    "sort_params": {
        "by": "thumbs_up_ratio",
        "ascending": False
    }
}


def get_competitions():
    url = get_url(COMPETITIONS_ENDPOINT)
    response = requests.get(url)
    assert response.ok, response.json()
    return response.json()

