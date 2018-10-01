import json
from expiringdict import ExpiringDict
import requests
from external.external_endpoints import SITE_DEMOGRAPHICS_URL, GEO_IP_COUNTRY_LOOK_UP, PUBLISHER_LOOK_UP, MAXMIND_CREDS

ONE_DAY = 86400  # seconds

# Caches for different external calls
DEMOGRAPHICS_CACHE = ExpiringDict(10**7, 86400)
COUNTRY_IP_CACHE = ExpiringDict(10**7, 86400)
PUBLISHER_CACHE = ExpiringDict(10**7, 86400)


# GET

def get_site_demographics(site_id):
    if site_id in DEMOGRAPHICS_CACHE:
        return DEMOGRAPHICS_CACHE[site_id]
    req = requests.get(SITE_DEMOGRAPHICS_URL.format(site_id=site_id))
    if req.status_code == 200:
        demographics = json.loads(req.content.decode('utf8')).get('demographics')
        if demographics:  # cache only when the service responded with data
            DEMOGRAPHICS_CACHE[site_id] = demographics
            return DEMOGRAPHICS_CACHE[site_id]


def get_country_by_device_ip(ip):
    """GET request to MaxMind service for country. Always hit the cache first before making a network call"""
    if ip in COUNTRY_IP_CACHE:
        return COUNTRY_IP_CACHE[ip]
    geo_data = requests.get(
        GEO_IP_COUNTRY_LOOK_UP.format(ip_address=ip), auth=MAXMIND_CREDS
    )
    if geo_data.status_code == 200:
        try:
            COUNTRY_IP_CACHE[ip] = json.loads(geo_data.content.decode('utf8'))['country']['iso_code']
            return COUNTRY_IP_CACHE[ip]
        except KeyError:
            return


# POST

def publisher_details_by_site_id(site_id):
    if site_id in PUBLISHER_CACHE:
        return PUBLISHER_CACHE[site_id]
    post_req = {
        'q': {
            'siteID': site_id
        }
    }
    publisher_details = requests.post(PUBLISHER_LOOK_UP, json=post_req)
    if publisher_details.status_code == 200:
        pub_details = json.loads(publisher_details.content.decode('utf8')).get('publisher')
        if pub_details:
            PUBLISHER_CACHE[site_id] = pub_details
            return PUBLISHER_CACHE[site_id]
