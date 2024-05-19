from logs import TaskLogger
from bs4 import BeautifulSoup

class TicketMasterChangeNominative:
    
    def __init__(self, session, order_id) -> None:

        self.session = session
        self.order_id = order_id

        self.logger = TaskLogger(self.task_id)

        self.order_response = None
        self.change_nominative_data = {}

    def show_order(self):

        r = self.session.get(
            url=f'https://shop.ticketmaster.it/mostra-ordine.html?idOrder={self.order_id}',
            headers={
                'method': 'GET',
                'authority': 'shop.ticketmaster.it',
                'scheme': 'https',
                'path': f'/mostra-ordine.html?idOrder={self.order_id}',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'upgrade-insecure-requests': '1',
                'user-agent': self.session.headers['User-Agent'],
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://shop.ticketmaster.it/i-miei-ordini.html',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
            }
        )

        return r

    def get_cambio_nominativo(self):

        r = self.session.get(
            url=f'https://shop.ticketmaster.it/richiesta-cambio-nominativo.html?idOrder={self.order_id}',
            headers={
                'method': 'GET',
                'authority': 'shop.ticketmaster.it',
                'scheme': 'https',
                'path': f'/richiesta-cambio-nominativo.html?idOrder={self.order_id}',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'upgrade-insecure-requests': '1',
                'user-agent': self.session.headers['User-Agent'],
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': f'https://shop.ticketmaster.it/mostra-ordine.html?idOrder={self.order_id}',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
            }
        )

        soup = BeautifulSoup(markup=r.text, features='lxml')

        return r

    def cambio_nominativo(self):

        r = self.session.post(
            url='https://shop.ticketmaster.it/richiesta-cambio-nominativo.html',
            headers={
                'method': 'POST',
                'authority': 'shop.ticketmaster.it',
                'scheme': 'https',
                'path': '/richiesta-cambio-nominativo.html',
                'content-length': '',
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
                'referer': f'https://shop.ticketmaster.it/richiesta-cambio-nominativo.html?idOrder={self.order_id}',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
            }
        )