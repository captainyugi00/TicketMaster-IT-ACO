from logs import TaskLogger

from queueit import (
    TicketMasterQueue
)

class TicketMasterLogin:

    def __init__(self, session, username, password, task_id) -> None:
        self.username = username
        self.password = password
        self.session = session
        self.task_id = task_id

        self.task_id = task_id
        self.logger = TaskLogger(self.task_id)

    def get_login(self):

        self.logger.status('Initiating login...')

        try:
            r = self.session.get(
                url='https://shop.ticketmaster.it/accountLogin.html',
                headers={
                    'method': 'GET',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': '/accountLogin.html',
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
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': 'https://www.ticketmaster.it/',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
            )
        except Exception as e:
            self.logger.error(f'Exception on Login Initialize: {e}. Retrying...')
            return 0

        if 'queue' in r.url:
            response = TicketMasterQueue(
                session=self.session, 
                original_url=self.url, 
                queue_url=r.url, 
                queue_text=r.text, 
                task_id=self.task_id
            ).queue_flow()

            return response

        return r

    def post_login(self, referer=None):

        self.logger.status('Logging in...')

        try:
            url = 'https://shop.ticketmaster.it/accountLogin.html' if not referer else referer.split('?')[0]
            r = self.session.post(
                url=url,
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': url.split('shop.ticketmaster.it')[1],
                    'content-length': '95',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'upgrade-insecure-requests': '1',
                    'origin': 'https://shop.ticketmaster.it',
                    'content-type': 'application/x-www-form-urlencoded',
                    'user-agent': self.session.headers['User-Agent'],
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': 'https://shop.ticketmaster.it/accountLogin.html' if not referer else referer,
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'landingPage': '' if not referer else referer.split('?')[1].split('=')[1].replace('%2F', '/'),
                    'login': self.username,
                    'password': self.password,
                    'rememberMe': 'true',
                    'doLogin': '',
                },
                show_redirects=True
            )
        except Exception as e:
            self.logger.error(f'Exception on Login POST: {e}. Retrying...')
            return 0

        if 'queue' in r.url:
            response = TicketMasterQueue(
                session=self.session, 
                original_url=self.url, 
                queue_url=r.url, 
                queue_text=r.text, 
                task_id=self.task_id
            ).queue_flow()

            return response

        if 'termsandconditions' in r.url:
            terms = self.session.post( # livenation
                url=r.url,
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': r.url.split('shop.ticketmaster.it')[1],
                    'content-length': '95',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'upgrade-insecure-requests': '1',
                    'origin': 'https://shop.ticketmaster.it',
                    'content-type': 'application/x-www-form-urlencoded',
                    'user-agent': self.session.headers['User-Agent'],
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': r.url,
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'landingPage': 'historyBack.html',
                    'applicationTermsAndConditions': '47',
                    'applicationTermsAndConditions_47': '47',
                    'applicationTermsAndConditions': '43',
                    'applicationTermsAndConditions_43': '43',
                    'doSave': 'Conferma',
                    'dsNotes': '',
                }
            )

            return self.post_login(referer=referer)

        if self.session.get_cookie('TMS_TCKTMSTR_cdLoginCrypt', 'shop.ticketmaster.it') != 0:
            self.logger.success('Successfully logged in!')
        else:
            self.logger.error('Login failed!')
            return 0

        return r
