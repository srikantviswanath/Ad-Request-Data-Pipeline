import json

from flask import Flask, request

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
    request_dict['site']['demographics'] = get_site_demographics(site_id)
    return request_dict


@timeit('fetching publisher details by site id')
def inject_publisher_details(request_dict):
    site_id = request_dict['site']['id']
    request_dict['site']['publisher'] = publisher_details_by_site_id(site_id)
    return request_dict


@timeit('fetching country of device ip')
def inject_device_country(request_dict):
    ip = request_dict['device']['ip']
    request_dict['device']['country'] = get_country_by_device_ip(ip)
    return request_dict


INDIVIDUAL_PROCESSING_UNITS = (
    inject_device_country,
    inject_site_demographics,
    inject_publisher_details
)


@app.route('/', methods=['POST'])
@timeit('E2E pipeline')
def augment_ad_request():
    req_data = request.get_json()
    for ipu in INDIVIDUAL_PROCESSING_UNITS:
        req_data = ipu(req_data)
    return json.dumps(req_data)


if __name__ == '__main__':
    app.run(debug=True)
