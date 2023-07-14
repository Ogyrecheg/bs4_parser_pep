from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
URL_PEP = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}

PRETTY_CHOICE = 'pretty'
FILE_CHOICE = 'file'
