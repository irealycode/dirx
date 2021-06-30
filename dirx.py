#!/usr/bin/env python3
import requests
import sys
import os
import threading
import random
import queue

#-----------------------------------------------------------#

arg_list = ['-w ', '-u ','-t ','-ra','-er','-h']
wordlist_agr = '-w '
url_arg = '-u '
wordlist = ''
url = ''
ac = '200,302,403,400'
n_threads = 20
q = queue.Queue()
r = queue.Queue()
i2 = 0

#-----------------------------------------------------------#

try :
    args = sys.argv[1:]
    args = ' '.join(args)
    args = str(args)
    if arg_list[5] in args:
        helpp = """
        help menu

        -u : url
        -w : wordlist
        -t : number of threads
       -ra : random agents
       -er : hide errors
        -h : help
        """
        print(helpp)
        exit()
    wordlist = args.split(arg_list[0],1)[1]
    wordlist = wordlist.split().pop(0)
    url = args.split(arg_list[1],1)[1]
    url = url.split().pop(0)
    
    
    if arg_list[2] in args:
        n_threads = args.split(arg_list[2],1)[1]
        n_threads = int(n_threads.split().pop(0))
    if arg_list[3] in args:
        random_agent = True
        rra = 'Random'
    else:
        random_agent = False
        rra = 'dirx v1.0'
    if arg_list[4] in args:
        er = True
    else:
        er = False
    
    

except:
    print('./dirx.py -u http://exemple.com -w wordlist')
    exit()
# print(f'url:{url}, wordlist:{wordlist}')

with open(wordlist) as dirnum:
    n=0
    for i in dirnum:
        n += 1
banner = f"""
=====================================================================================
-------------------------------------dirx-v1.0---------------------------------------
=====================================================================================
 GET HTTP/1.1

 Url : {url}
 User-agent : {rra}
 Direcrories Loaded : {n}
 Accepting Status : {ac}
 Threads : {n_threads}

=====================================================================================
---------------------------------made-by-irealycode----------------------------------
=====================================================================================

    """
print(banner)

def main():
    global q
    global i2
    # dirs = open(wordlist)
    # dirs = dirs.readlines()
    # ua = open('user-agents.txt').read().splitlines()
    # for i in range(len(dirs)):
    
    while True:
        try:
            dir = q.get()
            directory = dir
            full_url = url+'/'+directory
            if random_agent:
                ua = open('user-agents.txt').read().splitlines()
                user_agent = {'User-agent': random.choice(ua)}
            else:
                user_agent = {'User-agent': 'dirx v1.0'}
            # print(f'get {full_url}/{directory} user-agent:{user_agent}')random.choice(ua)
            try:
                req = requests.get(full_url, headers = user_agent, timeout=5)
                if str(req.status_code) != '404':
                    print(f'{full_url} : {req.status_code}')
            except:
                if not er:
                    print(f'timeout or error on : {full_url} -er to disable')
            i2 += 1
            print(f'directories tested : {i2}', end='\r')
        except KeyboardInterrupt:
            print('bye')
            exit()
    
    
try:
    dirs = open(wordlist).read().splitlines()
    for dir in dirs:
        q.put(dir)
        
    for t in range(n_threads):
        thread = threading.Thread(target=main)
        thread.daemon = True
        thread.start()
    q.join()
except KeyboardInterrupt:
    print('\nbye.')
    exit()

main()
