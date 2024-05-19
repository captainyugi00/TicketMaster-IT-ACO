import random
from bs4 import BeautifulSoup
from captcha_solver import send_to_autosolve
from logs import TaskLogger

from queueit import (
    TicketMasterQueue
)

RECAPTCHA_SITE_KEY = '6LdRiPAUAAAAALA6dKXjZK8h9y8kCaiGwtyqdkD9'
INCAPSULA_SITE_KEY = '6Ld38BkUAAAAAPATwit3FXvga1PI6iVTb6zgXw62'

class TicketMasterProduct:

    def __init__(self, session, url, ticket_quantity, ticket_type, max_price, task_id) -> None:
        self.session = session
        self.url = url

        self.tickets = None
        self.selected_ticket = None
        self.selected_ticket_type = None
        self.user_quantity = int(ticket_quantity)
        self.ticket_type = ticket_type
        self.max_price = max_price

        self.task_id = task_id
        self.logger = TaskLogger(self.task_id)

    def get_product(self):

        self.logger.status('Checking stock...')

        try:
            r = self.session.get(
                url=self.url,
                headers={
                    'method': 'GET',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': self.url.split('shop.ticketmaster.it')[1],
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
                    #"x-queueit-ajaxpageurl" : self.url,
                    'referer': 'https://www.ticketmaster.it/',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                #allow_redirects=False
            )
        except Exception as e:
            self.logger.error(f'Exception on Stock Check: {e}. Retrying...')
            return 0

        soup = BeautifulSoup(markup=r.text, features='lxml')
        product_id = None

        try:
            product_id = soup.find(name='input', attrs={'name': 'idProduct'})['value']
        except:
            pass

        if 'queue' not in r.url:
            if product_id == None:
                try:
                    try:
                        incapsula_id = 'https://shop.ticketmaster.it' + soup.find(name='script', attrs={'type': 'text/javascript'})['src']
                    except:
                        incapsula_id = 'https://shop.ticketmaster.it' + soup.find(name='iframe', attrs={'id': 'main-iframe'})['src']

                    self.logger.status('Solving Incapsula Captcha...')

                    recaptcha_key = send_to_autosolve(
                        {
                            "taskId": f'task{random.randint(11111111, 999999999999999999)}',
                            "url": incapsula_id,
                            "siteKey": INCAPSULA_SITE_KEY,
                            "version": "0"
                        }
                    )

                    self.session.post(
                        url=incapsula_id,#.split('?')[0],# + 'cts=' + incapsula_value + 'SWCGHOEL=v2',
                        headers={
                            'method': 'POST',
                            'authority': 'shop.ticketmaster.it',
                            'scheme': 'https',
                            'path': incapsula_id.split('?')[1],# + 'cts=' + incapsula_value + 'SWCGHOEL=v2',
                            'content-length': '',
                            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                            'sec-ch-ua-mobile': '?0',
                            'user-agent': self.session.headers['User-Agent'],
                            'sec-ch-ua-platform': '"macOS"',
                            'content-type': 'application/x-www-form-urlencoded',
                            'accept': '*/*',
                            'origin': 'https://shop.ticketmaster.it',
                            'sec-fetch-site': 'same-origin',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-dest': 'empty',
                            'referer': incapsula_id,
                            'accept-encoding': 'gzip, deflate, br',
                            'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                        },
                        data={
                            'g-recaptcha-response': recaptcha_key,
                        }
                    )

                    return 0
                except Exception as e:
                    pass

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

    def get_login_url(self, product_response:str):

        soup = BeautifulSoup(markup=product_response, features='lxml')

        try:
            product_id = soup.find(name='input', attrs={'name': 'idProduct'})['value']
        except:
            self.logger.warning('Cannot retrieve product info...')
            return 0

        try:
            return self.session.post(
                url=self.url,
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': self.url.split('shop.ticketmaster.it')[1],
                    'content-length': '',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
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
                    'referer': self.url,
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'idProduct': product_id,
                    'cdFilter': '',
                    'cdCard': '',
                    'cdSection': '',
                    'isToCheckout': 'true',
                    'doLoginOrRegister': 'Accedi o Registrati'
                },
                show_redirects=True
            )
        except Exception as e:
            self.logger.error(f'Exception on Login URL Retrieving: {e}. Retrying...')
            return 0

    def select_tickets(self, product_response:str):

        soup = BeautifulSoup(markup=product_response, features='lxml')

        try:
            self.form_data = soup.find(name='form', attrs={'name': 'showProductForm'}).find_all(name='input')
            self.product_id = soup.find(name='input', attrs={'name': 'idProduct'})['value']
            title = soup.find(name='h1', attrs={'class': 'text_h3 bold margin-bottom'}).text
        except:
            self.logger.warning('Cannot retrieve product info...')
            return 0

        try:
            tickets = soup.find(name='tbody', attrs={'id': 'item'}).find_all(name='tr')
        except:
            self.logger.warning(f'No ticket selected for: "{title}", retrying...')
            return 0

        self.tickets = []

        for ticket in tickets:
            ticket_soup = BeautifulSoup(markup=str(ticket), features='lxml')

            try:
                ticket_type = ticket_soup.find(name='h3').text
                self.tickets.append(
                    {
                        'id': ticket_soup.find(name='select')['id'],
                        'type': ticket_type,
                    }
                )
            except:
                continue

            try:
                price = int(str(ticket_soup.find(name='td', attrs={'align': 'right'}).text).split(',')[0].replace('"', ''))

                if price > self.max_price:
                    continue

                max_quantity = ticket_soup.find(name='select')['qtqtymax']

                if self.ticket_type.lower() != 'any' and self.ticket_type.lower() in ticket_type.lower() and self.selected_ticket == None:
                    self.selected_ticket = ticket_soup.find(name='select')['id']
                    self.selected_ticket_type = ticket_type
                    if int(self.user_quantity) > int(max_quantity):
                        self.user_quantity = int(max_quantity)
                elif self.ticket_type.lower() == 'any' and self.selected_ticket == None:
                    self.selected_ticket = ticket_soup.find(name='select')['id']
                    self.selected_ticket_type = ticket_type
                    if int(self.user_quantity) > int(max_quantity):
                        self.user_quantity = int(max_quantity)
            except:
                pass

        if self.selected_ticket == None and self.tickets != []:
            selected_ticket_data = random.choice(self.tickets)
            self.selected_ticket = selected_ticket_data['id']
            self.selected_ticket_type = selected_ticket_data['type']
        elif self.selected_ticket == None and self.tickets == []:
            self.logger.warning(f'No ticket selected for: "{title}", retrying...')
            return 0

        self.logger.success(f'Successfully selected {self.user_quantity} ticket(s): "{self.selected_ticket_type}"')

        return 1

    def add_to_cart(self):

        data = {
            'idProduct': self.product_id,
            'cdCard': '',
            'cdSection': '',
            'idProductItemSel': '',
            'isToCheckout': 'true',
            'cdDelivery': 'TM_eTicket',
            'doAddToBasket': "Procedi con l'ordine"
        }

        for value in self.form_data:
            value_soup = BeautifulSoup(markup=str(value), features='lxml')

            try:
                data[value_soup.find(name='input')['name']] = value_soup.find(name='input')['value']
            except:
                try:
                    data[value_soup.find(name='input')['name']] = ''
                except:
                    pass

        data.update({'cdDelivery': 'TM_eTicket'})

        self.logger.status('Solving Captcha...')
        recaptcha_key = send_to_autosolve(
            {
                "taskId": f'task{random.randint(11111111, 999999999999999999)}',
                "url": self.url,
                "siteKey": RECAPTCHA_SITE_KEY,
                "version": "0"
            }
        )

        data.update({'g-recaptcha-response': recaptcha_key})

        for ticket in self.tickets:
            if self.selected_ticket == ticket['id']:
                data[ticket['id']] = str(self.user_quantity)
            else:
                data[ticket['id']] = ''

        self.logger.status('Adding to cart...')

        try:
            r = self.session.post(
                url=self.url,
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': self.url.split('shop.ticketmaster.it')[1],
                    'content-length': '',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
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
                    'referer': self.url,
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data=data,
                show_redirects=True
            )
        except Exception as e:
            self.logger.error(f'Exception on ATC: {e}. Retrying...')
            return 0

        error = ['null']

        try:
            soup = BeautifulSoup(markup=r.text, features='lxml')

            error_list = soup.find(name='ol', attrs={'class': 'errors'}).find_all(name='li')
            error = []

            for error_a in error_list:
                if 'attenzione!' in str(error_a.text).lower():
                    continue

                error.append(str(error_a.text).replace('\n', ' ').strip())
        except:
            pass

        if r.url == self.url:
            self.logger.warning(f'Add to cart failed: {" ".join(error)}')
            self.user_quantity -= 1
            return 0

        elif 'checkout' not in r.url and 'login' not in r.url.lower():
            self.logger.warning(f'Add to cart failed: {" ".join(error)}')
            self.user_quantity -= 1
            return 0

        elif 'checkout' not in r.url and 'login' in r.url.lower():
            self.logger.warning(f'Add to cart failed: NEED LOGIN')
            self.user_quantity -= 1
            return 0

        try:
            soup = BeautifulSoup(markup=r.text, features='lxml')

            confirm_nominative = {
                'idBsk': soup.find(name='input', attrs={'name': 'idBsk'})['value']
            }

            full_nominative_data = soup.find_all(name='tr', attrs={'class': 'registrantReguired tr-1'})

            for nominative_data in full_nominative_data:
                nominative_soup = BeautifulSoup(markup=str(nominative_data), features='lxml')
                nominative_data_2 = nominative_soup.find(name='div', attrs={'class': 'col-2-1'}).find_all(name='input')

                for id in nominative_data_2:
                    nominative_data_soup = BeautifulSoup(markup=str(id), features='lxml')

                    try:
                        confirm_nominative[nominative_data_soup.find(name='input')['name']] = nominative_data_soup.find(name='input')['value']
                    except:
                        try:
                            confirm_nominative[nominative_data_soup.find(name='input')['name']] = ''
                        except:
                            pass

            if 'doSaveRegistrant' not in confirm_nominative:
                confirm_nominative.update({'doSaveRegistrant': 'Conferma nominativo'})

            self.session.confirm_nominative = True
            self.session.confirm_nominative_data = confirm_nominative
        except:
            self.session.confirm_nominative = False

        return r
