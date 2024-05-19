from time import time, sleep
from uuid import uuid4
from logs import TaskLogger
from urllib.parse import urlparse
from urllib.parse import parse_qs

class TicketMasterQueue:

    def __init__(self, session, original_url, queue_url, queue_text:str, task_id):
        """TicketMaster Queue

        Args:
            session (str): TLS Session
            original_url (str): Original Request URL
            queue_url (str): Redirect URL (Queue)
            queue_text (str): Queue Response Text
            task_id (str): Task ID
        """

        self.session = session
        self.original_url = original_url
        self.queue_url = queue_url
        self.task_id = task_id

        self.logger = TaskLogger(self.task_id)

        parsed_queue_url = urlparse(queue_url)
        self.enqueue_value = parse_qs(parsed_queue_url.query)['e'][0]
        self.cid = 'it-IT'
        self.seid = str(uuid4())
        self.sets = str(int(time() * 1000))

        self.queue_id = None
        self.queueitem = None

        self.layout_name = queue_text.split('new QueueIt.Queue.InQueueView({')[1].split(')}')[0].split('layout:')[1].split(',')[0].replace("'", '').strip()
        self.layout_version = queue_text.split('new QueueIt.Queue.InQueueView({')[1].split(')}')[0].split('layoutVersion:')[1].split(',')[0].replace("'", '').strip()

    def enqueue(self):

        r = self.session.post(
            url=f'https://queueshop.ticketmaster.it/spa-api/queue/ticketmasteritaly/{self.enqueue_value}/enqueue?cid={self.cid}',
            headers={
                'method': 'POST',
                'authority': 'queueshop.ticketmaster.it',
                'scheme': 'https',
                'path': f'/spa-api/queue/ticketmasteritaly/{self.enqueue_value}/enqueue?cid={self.cid}',
                'content-length': '',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'user-agent': self.session.headers['User-Agent'],
                'content-type': 'application/json',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-queueit-qpage-referral': 'https://shop.ticketmaster.it/',
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua-platform': '"macOS"',
                'origin': 'https://queueshop.ticketmaster.it',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': self.queue_url,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
            },
            json={
	            "layoutName": self.layout_name,
	            "customUrlParams": "",
	            "targetUrl": self.original_url,
	            "Referrer": "https://shop.ticketmaster.it/"
            }
        )

        self.queue_id = r.json()['queueId']

        return r

    def check_queue_status(self):

        if self.queueitem != None:
            headers = {
                'method': 'POST',
                'authority': 'queueshop.ticketmaster.it',
                'scheme': 'https',
                'path': f'/spa-api/queue/ticketmasteritaly/{self.enqueue_value}/{self.queue_id}/status?cid={self.cid}&l={self.layout_name.replace(" ", "%20")}&seid={self.seid}&sets={self.sets}',
                'content-length': '',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'user-agent': self.session.headers['User-Agent'],
                'content-type': 'application/json',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest',
                'x-queueit-queueitem-v1': self.queueitem,
                'sec-ch-ua-platform': '"macOS"',
                'origin': 'https://queueshop.ticketmaster.it',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': self.queue_url,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
            }
        else:
            headers = {
                'method': 'POST',
                'authority': 'queueshop.ticketmaster.it',
                'scheme': 'https',
                'path': f'/spa-api/queue/ticketmasteritaly/{self.enqueue_value}/{self.queue_id}/status?cid={self.cid}&l={self.layout_name.replace(" ", "%20")}&seid={self.seid}&sets={self.sets}',
                'content-length': '',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'user-agent': self.session.headers['User-Agent'],
                'content-type': 'application/json',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua-platform': '"macOS"',
                'origin': 'https://queueshop.ticketmaster.it',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': self.queue_url,
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
            }

        r = self.session.post(
            url=f'https://queueshop.ticketmaster.it/spa-api/queue/ticketmasteritaly/{self.enqueue_value}/{self.queue_id}/status?cid={self.cid}&l={self.layout_name.replace(" ", "%20")}&seid={self.seid}&sets={self.sets}',
            headers=headers,
            json={
	            "targetUrl": self.original_url,
	            "customUrlParams": "",
	            "layoutVersion": self.layout_version,
	            "layoutName": self.layout_name,
	            "isClientRedayToRedirect": True,
	            "isBeforeOrIdle": False
            }
        )

        if r.headers.get('x-queueit-queueitem-v1', None) != None:
            self.queueitem = r.headers['x-queueit-queueitem-v1']

        if r.json().get('pageId') == 'queue':
            self.logger.warning(f'Task is in Queue, users ahead: {r.json()["ticket"]["usersInLineAheadOfYou"]}')
            return 11

        elif r.json().get('pageId') == 'before':
            self.logger.warning(f'Task is in Pre-Queue.')
            return 11

        self.logger.success('Task passed Queue!')

        return r.json()['redirectUrl']

    def get_response(self, url):

        r = self.session.get(
            url=url,
            headers={
                'method': 'GET',
                'authority': 'shop.ticketmaster.it',
                'scheme': 'https',
                'path': url.split('ticketmaster.it')[1],
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'upgrade-insecure-requests': '1',
                'user-agent': self.session.headers['User-Agent'],
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-dest': 'document',
                'referer': 'https://queueshop.ticketmaster.it/',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
            }
        )

        return r

    def queue_flow(self):

        while True:
            try:
                self.enqueue()
            except Exception as e:
                self.logger.error(f'Exception in task enqueue: {e}. Retrying...')
                continue
            break

        while True:
            try:
                redirect_url = self.check_queue_status()

                if redirect_url == 11:
                    sleep(5)
                    continue
                else:
                    return self.get_response(url=redirect_url)
            except Exception as e:
                self.logger.error(f'Exception in task queue check: {e}. Retrying...')
                continue
