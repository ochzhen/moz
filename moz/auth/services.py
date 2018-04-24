import requests
from flask import current_app


def get_country_code(ipaddress):
    if not current_app.config['CHECK_LOCATION']:
        return 'UA'

    ip = str(ipaddress)
    
    code = country_code_by_ip_api(ip)
    if code:
        return code

    code = country_code_by_geoip_nekudo(ip)
    if code:
        return code

    code = country_code_by_geoplugin(ip)
    if code:
        return code

    return 'UA'


def country_code_by_ip_api(ip):
    params = { 'fields': 'status,countryCode,message' }
    url = 'http://ip-api.com/json/' + ip
    try:
        r = requests.get(url, params=params)
        data = r.json()
        if r.status_code != requests.codes.ok or data['status'].lower() == 'fail':
            current_app.logger.error(
                'Geolocation api status FAIL: %s\t%s\t%s', r.status_code, url, data['message'])
            return None
        code = data['countryCode'].upper()
        return code
    except Exception as e:
        current_app.logger.error('Geolocation api exception: %s\t%s', url, str(e))


def country_code_by_geoip_nekudo(ip):
    url = 'http://geoip.nekudo.com/api/%s/short' % (ip)
    try:
        r = requests.get(url)
        data = r.json()
        if r.status_code != requests.codes.ok or ('type' in data and data['type'].lower() == 'error'):
            current_app.logger.error(
                'Geolocation api error: %s\t%s\t%s', r.status_code, url, data['msg'])
            return None
        code = data['country']['code'].upper()
        return code
    except Exception as e:
        current_app.logger.error('Geolocation api exception: %s\t%s', url, str(e))


def country_code_by_geoplugin(ip):
    params = { 'ip': ip }
    url = 'http://www.geoplugin.net/json.gp'
    try:
        r = requests.get(url, params=params)
        data = r.json()
        if r.status_code != requests.codes.ok or data['geoplugin_status'] != 200:
            current_app.logger.error(
                'Geolocation api error: %s\t%s\t%s', r.status_code, url, data['geoplugin_status'])
            return None
        code = data['geoplugin_countryCode'].upper()
        return code
    except Exception as e:
        current_app.logger.error('Geolocation api exception: %s\t%s', url, str(e))
