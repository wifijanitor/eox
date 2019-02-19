#! /usr/bin/env python3

import requests
import argparse
import sys
import credentials as creds
from pprint import pprint
#import logging

# initialize logging, otherwise you will not see anything from requests
'''
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
'''


my_token = "no-token"
pid = None
file = None


class web():
    '''
    Information on where calls are being made, and what informatio is needed
    '''
    auth_url = "https://cloudsso.cisco.com/as/token.oauth2"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': creds.client_id,
        'client_secret': creds.client_secret}
    auth_headers = {
        'content-type': "application/x-www-form-urlencoded"
    }
    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID//"
    querystring = {"responseencoding": "json"}
    '''headers = {
        'accept': "application/json",
        'authorization': "Bearer " + my_token
    }
    '''


def parseOptions():
    global file
    global pid
    parser = argparse.ArgumentParser(
        prog='EOX Finder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
            Seach for EOL and EOS products.
            You can either provide a list of up to 20 PID that is comma
            seperated. "*" can be used as a wildcard
            Or you can specifiy a file name.
            If providing a file name, please use the absolute path
        ''')
    parser.add_argument('-f', '--file',
                        metavar='File_Name',
                        help="File with prodicut ID to search for",
                        dest='File_Name')
    parser.add_argument('-s', '--search',
                        metavar='Search',
                        help="Single or comma seperated list \
                        of PID to search for",
                        dest='Search')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 1.0')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    file = str(args.File_Name)
    pid = str(args.Search)


def get_token():
    global my_token
    '''
    Get access Token and store as a variable
    '''
    r = requests.post(web.auth_url, data=web.payload, headers=web.auth_headers)
    d = r.json()
    my_token = d['access_token']
    return my_token


def EOX():
    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + my_token
    }
    '''
    try:
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1
    '''
    if len(file) == 1:
        with open(file, 'rt') as product:
            for row in product:
                response = requests.get(web.url + row,
                                        headers=headers,
                                        params=web.querystring
                                        )
    else:
        response = requests.get(web.url + pid,
                                headers=headers,
                                params=web.querystring
                                )
    pprint(response.json())
#    eol = response.json()


def main():
    parseOptions()
    get_token()
    EOX()


if __name__ == '__main__':
    main()
