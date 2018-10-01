import random
import string
from ipaddress import ip_address
import matplotlib.pyplot as plt
import requests
import numpy as np


def find_ip_addrs_in_range(start, end):
    """Given a start and end IPV4 addresses, return all addresses in between"""
    start = ip_address(start)
    end = ip_address(end)
    result = []
    while start <= end:
        result.append(str(start))
        start += 1
    return result


def generate_random_ad_req(ip_ranges, site_id_size=6):
    """Generate a random ad request with minimal useful keys, i.e., site.id and device.ip"""
    return {
        'site':{
            'id': ''.join(random.choice(string.ascii_lowercase) for _ in range(site_id_size))
        },
        'device': {
            'ip': random.choice(ip_ranges)
        }
    }


def stress_test(no_of_msgs=1000):
    """Hit our data augmentation endpoint several times"""
    ip_ranges = find_ip_addrs_in_range('4.1.13.255', '4.14.243.127')
    for i in range(no_of_msgs):
        if i % 20 == 0:
            print(i)
        service_endpoint = 'http://127.0.0.1:5000/'
        requests.post(service_endpoint, json=generate_random_ad_req(ip_ranges))


def analyze_perf_batch_times():
    with open('../E2ETime.txt', 'r') as f:
        times = [float(t) for t in f.read().split()]
        mu, median = np.mean(times), np.median(times)
        plt.hist(times, bins='auto')
        plt.text(800, 250, 'mean=%s \nmedian=%s' % (mu, median))
        plt.xlabel('Augmentation Latency(ms)')
        plt.suptitle('Histogram of data augmentation latency for ~5000 requests')
        plt.show()


if __name__ == '__main__':
    #stress_test(10000)
    analyze_perf_batch_times()