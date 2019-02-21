#! /usr/bin/env python3

import os
import requests
import sys
import cgi
from datetime import datetime
import credentials as creds


my_token = "no-token"
pid = None
eol = {'EOXRecord': []}


def get_token():
    '''
    Get access Token and store as a variable
    '''


global my_token
auth_url = "https://cloudsso.cisco.com/as/token.oauth2"
auth_payload = {
    'grant_type': 'client_credentials',
    'client_id': creds.client_id,
    'client_secret': creds.client_secret
}
auth_headers = {
    'content-type': "application/x-www-form-urlencoded"
}
r = requests.post(auth_url, data=auth_payload, headers=auth_headers)
d = r.json()
my_token = d['access_token']


def EOX():
    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID//"
    querystring = {"responseencoding": "json"}
    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + my_token
    }
    response = requests.get(web.url + pid,
                            headers=headers,
                            params=web.querystring
                            )
    f = response.json()
    c = f['EOXRecord']
    eol['EOXRecord'].extend(c)


def writer():
    for epid in eol['EOXRecord']:
        print(epid['EOLProductID'] + '\n' +
              epid['LinkToProductBulletinURL'] + '\n')


form = cgi.FieldStorage()
if not form.getvalue('pid'):
    front_page()
    pid = form.getvalue('pid').strip()
