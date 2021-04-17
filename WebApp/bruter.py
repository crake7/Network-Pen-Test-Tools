import queue
import requests
import threading
import time
import sys

agent      = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
extensions = ['.php', '.bak', '.orig', '.inc']
target     = input('Enter the target URL: ')
threads    = 10
wordlist   = "/home/kali/Downloads/SVNDigger/all.txt"

answers    = queue.Queue()

def get_words(resume=None):
    '''Return the "words" queue to test on target '''

    def extend_words(word):
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')

        for extension in extensions:
            words.put(f'/{word}{extension}')
    
    with open(wordlist) as f:
        raw_words = f.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        # Allows to resume brute force session in case of interruption
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')

        else:
            #print(word)
            extend_words(word)
    # We parse the entire fill and return a Queue full of words to use in the brute-forcing
    return words 

def dir_bruter(words):
    headers = {'User-Agent': agent}
    while not words.empty():
        url = f'{target}{words.get()}'
        time.sleep(2)           # avoid throttling on target's web app
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x'); sys.stderr.flush()
            continue

        if r.status_code == 200:
            answers.put(url)
            print(f'\nSuccess ({r.status_code}: {url})')
        # The status code depends on the configuration of the remote web server, adjust accordingly    
        elif r.status_code == 404:
            sys.stderr.write('.'); sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')


def run():
    mythreads = list()
    for _ in range(threads):
        t = threading.Thread(target = dir_bruter, args=(words,))
        t.start()
    for thread in mythreads:
        threading.join()


if __name__ == '__main__':
    words = get_words()
    print('Press return to continue.')
    sys.stdin.readline()
    run()
    with open('brute-forced.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
