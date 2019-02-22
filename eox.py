#! /bin/python

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
    eol = {}
    body = ""
    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID//"
    querystring = {"responseencoding": "json"}
    headers = {
        'accept': "application/json",
        'authorization': "Bearer " + token
    }
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
        body = body + prod + '<br>' + link + '<br>' + '<br>'
    send_mail(email, body)


def send_mail(email, body):
    return requests.post(
        "https://api.mailgun.net/v3/apps.wifijanitor.com/messages",
        auth=("api", creds.mail),
        data={"from": "Steve Rodriguez <steve@apps.wifijanitor.com>",
              "to": email,
              "subject": "Here is the requested EOL/EOS Information",
              "html": "<html>" + body +
              "</html>"}
    )


def front_page():
    print("Content-type: text/html")
    print('')
    print("""
    <html>
    <body>
    <form action='eox.py' METHOD='POST'>
    Email Address to send report:
    <input type = 'text' checked name = 'email'/>&nbsp;
    <br>
    Comma seperated list of PID for EOL check:
    <input type = 'text' checked name = 'pid'/>&nbsp;
    <p>
    <p>
    <input type='submit' />
    <p>
    """)


def bad_email(email):
    print("Content-type: text/html")
    print('')
    print("""
    <html>
    <body>
    <form action='eox.py' METHOD='POST'>
    Email Address to send report too:
    <input type = 'text' checked name = 'email'/>&nbsp;
    <br>
    Comma seperated list of PID for EOL check:
    <input type = 'text' checked name = 'pid'/>&nbsp;
    <p>
    <p>
    <input type='submit' />
    <p>
    The email %s is not a CDW email.
    If you have an issue, please email Steve.</h2>
    </form>
    </body>
    </html > """ % (email))


def bad_pid():
    print("Content-type: text/html")
    print('')
    print("""
    <html>
    <body>
    <form action='eox.py' METHOD='POST'>
    Email Address to send report:
    <input type = 'text' checked name = 'email'/>&nbsp;
    <br>
    Comma seperated list of PID for EOL check:
    <input type = 'text' checked name = 'pid'/>&nbsp;
    <p>
    <p>
    <input type='submit' />
    <p>
    Please provide at least one PID</h2>
    </form>
    </body>
    </html>
    """)


def output(email):
    print("Content-type: text/html")
    print('')
    print("""
    <html>
    <body>
    <form action='eox.py' METHOD='POST'>
    Email Address to send report:
    <input type = 'text' checked name = 'email'/>&nbsp;
    <br>
    Comma seperated list of PID for EOL check:
    <input type = 'text' checked name = 'pid'/>&nbsp;
    <p>
    <p>
    <input type='submit' />
    <p>
    <br><br>
    Thank you, your report has been emailed to %s
    </form>
    </body>
    </html>
    """ % (email))


form = cgi.FieldStorage()
if not form.getvalue('email'):
    front_page()
    email = form.getvalue('email')
    pid = form.getvalue('pid')
elif not form.getvalue('pid'):
    bad_pid()
    email = form.getvalue('email')
    pid = form.getvalue('pid')
else:
    email = form.getvalue('email')
    pid = form.getvalue('pid')
    if email.split('@')[-1].lower() != 'cdw.com':
        bad_email(email)
    else:
        get_token()
        output(email)
