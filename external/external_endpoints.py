#GET
SITE_DEMOGRAPHICS_URL = 'http://159.89.185.155:3000/api/sites/{site_id}/demographics'
GEO_IP_COUNTRY_LOOK_UP = 'https://geoip.maxmind.com/geoip/v2.1/country/{ip_address}'

MAXMIND_CREDS = ('136413', 'nZOHRkQ4kYuG')  # TODO: put these creds in a separate cryptic store


#POST
PUBLISHER_LOOK_UP = 'http://159.89.185.155:3000/api/publishers/find'