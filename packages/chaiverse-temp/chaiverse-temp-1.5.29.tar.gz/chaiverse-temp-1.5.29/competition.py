import requests

from chaiverse.utils import get_url


COMPETITIONS_ENDPOINT = '/competitions'


def get_competitions():
    url = get_url(COMPETITIONS_ENDPOINT)
    response = requests.get(url)
    assert response.ok, response.json()
    competitions = response.json()
    competitions = [_process_competition(competition) for competition in competitions]
    return competitions


def _process_competition(competition):
    submission_start_date = competition.get('submission_start_date', "2024-01-05")
    submission_end_date = competition.get('submission_end_date', "2024-01-13")
    competition['submission_start_date'] = submission_start_date
    competition['submission_end_date'] = submission_end_date
    return competition

