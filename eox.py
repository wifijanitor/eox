#! /usr/bin/env python3

import requests
import cgi
import credentials as creds


def get_token():
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': creds.client_id,
        'client_secret': creds.client_secret
    }
    headers = {
        'content-type': "application/x-www-form-urlencoded"
    }
    r = requests.post(url, data=payload, headers=headers)
    d = r.json()
    token = d['access_token']
    EOX(token)


def EOX(token):
    body = ""
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
    for i in f['EOXRecord']:
        prod = epid['EOLProductID']
        link = '<a href="' + \
            epid['LinkToProductBulletinURL'] + '>' + \
            epid['LinkToProductBulletinURL'] + '</a>'
        eol[prod] = link
    for k, v in eol.items():
        body = body + k + '<br>' + v + '<br>'
    send_mail(email, body)


def send_mail(email, body):
    return requests.post(
        "https://api.mailgun.net/v3/apps.wifijanitor.com/messages",
        auth=("api", creds.mail),
        data={"from": "EOX Report <stevrod@cdw.com>",
              "to": [email],
              "subject": "Here is the requested EOL/EOS Information",
              "html": "<html>"  body
              "</html>"}
    )


def front_page():
    print("Content-type: text/html")
    print()
    print("""
    <html>
    <body>
    <form action='eox.py' METHOD='POST'>
    Email Address to send report:
    <input type = 'text' checked name = 'email'/>&nbsp;
    <br>
    Comma seperated list of PID for EOL check:
    <input type = 'text' checked name = 'pid'/>&nbsp:
    <p>
    <p>
    <input type='submit' />
    <p>
    """)


def bad_email(email):
    print("""
    <html>
    <body>
    <form action='eox.py' METHOD='POST'>
    Email Address to send report too:
    <input type = 'text' checked name = 'email'/>&nbsp;
    <p>
    <p>
    <input type='submit' />
    <p>
    The email %s is not a CDW email.
    If you have an issue, please email Steve.</h2>
    </form>
    </body>
    < / html > """ % (email))


def bad_pid():
    print("""
    <html>
    <body>
    <form action='eox.py' METHOD='POST'>
    Email Address to send report:
    <input type = 'text' checked name = 'email'/>&nbsp;
    <br>
    Comma seperated list of PID for EOL check:
    <input type = 'text' checked name = 'pid'/>&nbsp:
    <p>
    <p>
    <input type='submit' />
    <p>
    Please provide at least one PID</h2>
    </form>
    </body>
    </html>
    """)


form = cgi.FieldStorage()
if not form.getvalue('pid'):
    bad_pid()
if not form.getvalue('email'):
    front_page()
    email = form.getvalue('email').strip()
else:
    email = form.getvalue('email').strip()
    pid = form.getvalue('pid').strip()
    if email.split('@')[-1].lower() != 'cdw.com':
        bad_email(email)
    else:
        get_token()
