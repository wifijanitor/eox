#! /usr/bin/env python3

import argparse
import requests
import sys
import credentials as creds


pid = None
file = None
email = None


def parseOptions():
    global file
    global pid
    global email
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
    parser.add_argument('-e', '--email',
                        metavar='email',
                        help="email we are sending report too",
                        dest='email')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    file = str(args.File_Name)
    pid = str(args.Search)
    email = str(args.email)


def get_token():
    '''
    Get access Token and store as a variable
    '''
    auth_url = "https://cloudsso.cisco.com/as/token.oauth2"
    auth_payload = {
        'grant_type': 'client_credentials',
        'client_id': creds.client_id,
        'client_secret': creds.client_secret}
    auth_headers = {
        'content-type': "application/x-www-form-urlencoded"
    }
    r = requests.post(auth_url, data=auth_payload,
                      headers=auth_headers)
    d = r.json()
    token = d['access_token']
    EOX(token)


def EOX(token):
    eol = {}
    body = ""
    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID//"
    querystring = {"responseencoding": "json"}
    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + token
    }
    if len(file) >= 6:
        with open(file, 'rt') as product:
            for line in product:
                row = line.rstrip()
                response = requests.get(url + row,
                                        headers=headers,
                                        params=querystring
                                        )
                f = response.json()
                c = f['EOXRecord']
                eol['EOXRecord'].extend(c)
    else:
        response = requests.get(url + pid,
                                headers=headers,
                                params=querystring
                                )
        f = response.json()
        for epid in f['EOXRecord']:
            prod = epid['EOLProductID']
            link = '<a href="' + \
                epid['LinkToProductBulletinURL'] + '">' + \
                epid['LinkToProductBulletinURL'] + '</a>'
            eol[prod] = link
    for k, v in eol.items():
        body = body + k + '<br>' + v + '<br>'
    send_mail(email, body)


def send_mail(email, body):
    print("sending mail")
    print(email)
    return requests.post(
        "https://api.mailgun.net/v3/apps.wifijanitor.com/messages",
        auth=("api", creds.mail),
        data={"from": "EOX Report <stevrod@cdw.com>",
              "to": [email],
              "subject": "Here is the requested EOL/EOS Information",
              "html": "<html>" + body +
              "</html>"}
    )


def main():
    parseOptions()
    get_token()


if __name__ == '__main__':
    main()
