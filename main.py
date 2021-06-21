import threading
from queue import Queue
from general import *
from spider import Spider
from domain import *
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user = "root", passwd = "atefclubiste", database = "linkscrawled")
mycursor = mydb.cursor()
PROJECT_NAME = 'getlinksmytek'
HOMEPAGE = "https://www.mytek.tn/"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE=PROJECT_NAME + '/queue.txt'
NUMBER_OFTHREADS=8
queue=Queue()
CRAWLED_FILE  = PROJECT_NAME + '/crawled.txt'
Spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)
# create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OFTHREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()

# do the next job in the queue
def work():
    while True:
        url=queue.get()
        Spider.crawl_page(threading.current_thread().name,url)
# each queued is a new link
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# checking if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links)>0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_workers()
crawl()
