import json

import requests

from external.external_endpoints import SITE_DEMOGRAPHICS_URL, GEO_IP_COUNTRY_LOOK_UP, PUBLISHER_LOOK_UP
from utils import memoize


# GET

@memoize
def get_site_demographics(site_id):
    return requests.get(SITE_DEMOGRAPHICS_URL.format(site_id=site_id)).content.decode('utf8')


@memoize
def get_country_by_device_ip(ip):
    geo_data = requests.get(
        GEO_IP_COUNTRY_LOOK_UP.format(ip_address=ip), auth=('136413', 'nZOHRkQ4kYuG')
    ).content.decode('utf8')
    return json.loads(geo_data)['country']['iso_code']


# POST

@memoize
def publisher_details_by_site_id(site_id):
    post_req = {
        'q': {
            'siteID': site_id
        }
    }
    publisher_details = requests.post(PUBLISHER_LOOK_UP, json=post_req).content
    return publisher_details.decode('utf8')
