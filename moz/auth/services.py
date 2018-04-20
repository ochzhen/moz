import requests
from flask import current_app


def get_country_code(ipaddress):
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
        current_app.logger.warning(str(data))
        if r.status_code != requests.codes.ok or data['status'] == 'fail':
            current_app.logger.error(
                'Geolocation api status FAIL: %s\t%s\t%s', r.status_code, url, data['message'])
            return None
        code = data['countryCode'].upper()
        current_app.logger.warning('Country code: %s , url: %s', code, url)
        return code
    except Exception as e:
        current_app.logger.error('Geolocation api exception: %s\t%s', url, str(e))


def country_code_by_geoip_nekudo(ip):
    url = 'http://geoip.nekudo.com/api/%s/short' % (ip)
    try:
        r = requests.get(url)
        data = r.json()
        current_app.logger.warning(str(data))
        if r.status_code != requests.codes.ok or ('type' in data and data['type'] == 'error'):
            current_app.logger.error(
                'Geolocation api error: %s\t%s\t', r.status_code, url, data['msg'])
            return None
        code = data['country'].['code'].upper()
        current_app.logger.warning('Country code: %s , url: %s', code, url)
        return code
    except Exception as e:
        current_app.logger.error('Geolocation api exception: %s\t%s', url, str(e))


def country_code_by_geoplugin(ip):
    params = { 'ip': ip }
    url = 'http://www.geoplugin.net/json.gp'
    try:
        r = requests.get(url, params=params)
        data = r.json()
        current_app.logger.warning(str(data))
        if r.status_code != requests.codes.ok or data['geoplugin_status'] != 200:
            current_app.logger.error(
                'Geolocation api error: %s\t%s\t%s', r.status_code, url, data['geoplugin_status'])
            return None
        code = data['geoplugin_countryCode'].upper()
        current_app.logger.warning('Country code: %s , url: %s', code, url)
        return code
    except Exception as e:
        current_app.logger.error('Geolocation api exception: %s\t%s', url, str(e))
