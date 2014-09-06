from collections import Counter
from itertools import groupby
import json
import logging
from urllib import request
from urllib import error as urlerror


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dataset(url):
    '''Fetches the JSON dataset and returns a python List of the same

    :param url: A link to the dataset
    :returns: List dataset
    '''
    req = request.urlopen(url)
    try:
        return json.loads(
            req.read().decode(req.headers.get_content_charset()))
    except (urlerror.URLError, ValueError) as e:
        logger.error('Error: %s', e.message)
    except Exception:
        logger.error('Error 37!')


def calculate(url=None):
    '''Processes the data set and returns the required "summary" dict

    :param url: A link to the JSON water points dataset
    :returns: summary dict

    Pretty print result with:-
    json.dumps(return_value, indent=4, sort_keys=True)
    '''

    if not url:
        url = ("https://raw.githubusercontent.com/onaio/"
               "ona-tech/master/data/water_points.json")

    data_set = get_dataset(url) or []
    return \
    {
        'number_functional':
            Counter(x['water_functioning'] for x in data_set)['yes'],
            # or len(filter(lambda x:x['water_functioning']=='yes',data_set)),  # noqa
            # or len([x for x in data_set if x['water_functioning']=='yes']),  # noqa
        'number_water_points':
            Counter(x['communities_villages'] for x in data_set),
        'community_ranking': dict(map(lambda t: (t[0], (Counter(
            x['water_functioning'] for x in t[1])['yes'] * 100) / len(t[1])),
            [(k, list(g)) for k, g in groupby(data_set,
                lambda x: x['communities_villages'])])),
    }
