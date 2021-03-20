import argparse
import requests

from requests.adapters   import HTTPAdapter
from requests.auth       import AuthBase
from requests.exceptions import Timeout

class TokenAuth(AuthBase):
    ''' Implements a custom authentication scheme '''

    def __init__(self, header, value):
        self.header = header
        self.value  = value
        
    def __call__(self, r):
        ''' Attach an API token to a custom auth header '''
        # print(r.headers)
        r.headers[self.header] = f'{self.value}'
        # print(r.headers)
        return r

def get_headers(headers):
    header, value = (headers.split(":"))
    return header, value

def open_session(hostname, header, value):
    ''' Allows to persist parameters and cookies across requests. It reuses the same TCP connection'''
    session = requests.Session()
    # Retry the connection in case it fails
    adapter = HTTPAdapter(max_retries=3)
    session.auth  = TokenAuth(header, value)
    session.mount = (hostname, adapter)
    
    try:
        response = session.get(hostname, timeout =5)
        return response
    except ConnectionError as e:
        print(e)

HELP = """\
You must specify the custom Auth header name and its value as such:  <header>:<value>
If you with to persist parameters across requests (useful with authenticated requests),
you must use the "Session" argument (-s) for a HTTP persistent connection.
"""

def main():

    parser = argparse.ArgumentParser(
        usage       = "./token-auth-request.py <hostname> <header>:<value> [options] -s",
        description = "Send a custom GET request adding a custom Auth header and its value",
        epilog      = HELP,)  
    
    parser.add_argument("hostname", type = str, action = "store", help = 'hostname')
    parser.add_argument("headers",              action = "store", help = 'header:value' )
    parser.add_argument("-s","--session", action ="store_true", dest='session', help = 'open a session')

    args = parser.parse_args()
    # print(args.hostname)
    header, value = get_headers(args.headers)
    # print(header, value)

    if args.session:
        session = open_session(args.hostname, header, value)
        for key, value in session.headers.items():
            print(key + str(":") + value)
        
    else:
        try:
            response = requests.get(args.hostname, timeout=5, auth=TokenAuth(header,value))
        # print(response)
        except Timeout:
            print('The request timed out')
    
        if response.status_code:
            print("Response headers:")
            for key, value in response.headers.items():
                print(key + str(":") + value)
        else:
            print("HTTP Response outside the range 200-400")


if __name__ == '__main__':
    main()