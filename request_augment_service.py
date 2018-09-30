import json

from flask import Flask, request, abort

from external.external_requests import (
    get_site_demographics,
    get_country_by_device_ip,
    publisher_details_by_site_id
)
from utils import timeit

app = Flask(__name__)


@timeit('fetching site demographics')
def inject_site_demographics(request_dict):
    site_id = request_dict['site']['id']
    demographics = get_site_demographics(site_id)
    if demographics:
        request_dict['site']['demographics'] = demographics
    return request_dict


@timeit('fetching publisher details by site id')
def inject_publisher_details(request_dict):
    site_id = request_dict['site']['id']
    pub_details = publisher_details_by_site_id(site_id)
    if not pub_details or not pub_details.get('id'):
        abort(400, 'Publisher ID could not be eshtablished')
    request_dict['site']['publisher'] = pub_details
    return request_dict


@timeit('fetching country of device ip')
def inject_device_country(request_dict):
    ip = request_dict['device']['ip']
    country = get_country_by_device_ip(ip)
    if country:
        if country == 'US':
            request_dict['device']['country'] = country
        else:
            abort(400, 'You are trying to access from outside US')
    return request_dict


INDIVIDUAL_PROCESSING_UNITS = (  # configurable pipeline
    inject_device_country,
    inject_site_demographics,
    inject_publisher_details
)


@app.route('/', methods=['POST'])
@timeit('E2E pipeline')
def augment_ad_request():
    """Entry point of data pipeline service"""
    req_data = request.get_json()
    for ipu in INDIVIDUAL_PROCESSING_UNITS:
        req_data = ipu(req_data)
    return json.dumps(req_data)


if __name__ == '__main__':
    app.run(debug=True)
