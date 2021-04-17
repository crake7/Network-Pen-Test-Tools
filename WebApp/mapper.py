import contextlib
import os
import queue
import requests
import sys
import threading
import time

agent    = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
filtered = [".jpg",".gif", ".png", ".css"]
target   = input('Enter target URL: ')
threads  = 10

answers  = queue.Queue()        # Found files on target web app
web_paths = queue.Queue()        # Files to locate on remote server

def test_remote():
    header = {'User-Agent': agent}
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{target}{path}'
        time.sleep(2)       # avoid throttling/lockout on target's web app
        r = requests.get(url, headers=header)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write("+")
        else:
            sys.stdout.write("x")
        sys.stdout.flush()

def run():
    mythreads = list()
    for i in range(threads):
        print(f'Spawning thread {i}')
        t = threading.Thread(target = test_remote)
        mythreads.append(t)
        t.start()

    for thread in mythreads:
        # wait for all threads to complete before returning
        thread.join()

def gather_paths():
    # Generates a dirpath, dirnames(empty), filenames by walking the local directry tree
    for root, _, files in os.walk('.'):
        for fname in files:
            # splits the filename in two: name and suffix
            if os.path.splitext(fname)[1] in filtered:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)

# Creates a simple context manager that converts a generator function into a context manager.  
@contextlib.contextmanager
def chdir(path):
    """On __enter__, change directory to specified path.
       On __exit__,  change directory back to original.
    """
    # Saves current dir
    this_dir = os.getcwd()
    # Change it into the new one
    os.chdir(path)
    try:
        # yields control to gather_paths()
        yield
    finally:
        # reverts to the original dir
        os.chdir(this_dir)

if __name__ == '__main__':
    with chdir("/home/kali/Downloads/wordpress"):
        gather_paths()
    input('Press return to continue')

    run()
    with open('mapped-paths.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('Done')



