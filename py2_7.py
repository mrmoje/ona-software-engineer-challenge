from collections import Counter
from itertools import groupby
import logging
import urllib2
import simplejson


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dataset(url):
    '''Fetches the JSON dataset and returns a python List of the same

    :param url: A link to the dataset
    :returns: List dataset
    '''
    request = urllib2.Request(url, None,
                              {'User-Agent': 'mrmoje/ona/py2.py'})
    try:
        return simplejson.load(
            urllib2.build_opener().open(request))
    except (urllib2.HTTPError, urllib2.URLError,
            simplejson.JSONDecodeError) as e:
        logger.error('Error: %s', e.message)
    except Exception:
        logger.error('Error 37!')


def calculate(url=None):
    '''Processes the data set and returns the required "summary" dict

    :param url: A link to the JSON water points dataset
    :returns: summary dict

    Pretty print result with:-
    simplejson.dumps(return_value, indent=4, sort_keys=True)
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
        'community_ranking': dict(map(lambda t: (t[0], (len(filter(
            lambda x:x['water_functioning']!='yes',t[1])) * 100) / len(t[1])),
            [(k, list(g)) for k, g in groupby(data_set,
                lambda x: x['communities_villages'])])),
    }
