import json

import requests
from external.external_endpoints import SITE_DEMOGRAPHICS_URL, GEO_IP_COUNTRY_LOOK_UP, PUBLISHER_LOOK_UP
from utils import memoize


# GET

@memoize
def get_site_demographics(site_id):
    req = requests.get(SITE_DEMOGRAPHICS_URL.format(site_id=site_id))
    if req.status_code == 200:
        return json.loads(req.content.decode('utf8')).get('demographics')


@memoize
def get_country_by_device_ip(ip):
    geo_data = requests.get(
        GEO_IP_COUNTRY_LOOK_UP.format(ip_address=ip), auth=('136413', 'nZOHRkQ4kYuG')
    )
    if geo_data.status_code == 200:
        return json.loads(geo_data.content.decode('utf8'))['country']['iso_code']


# POST

@memoize
def publisher_details_by_site_id(site_id):
    post_req = {
        'q': {
            'siteID': site_id
        }
    }
    publisher_details = requests.post(PUBLISHER_LOOK_UP, json=post_req)
    if publisher_details.status_code == 200:
        return json.loads(publisher_details.content.decode('utf8')).get('publisher')
