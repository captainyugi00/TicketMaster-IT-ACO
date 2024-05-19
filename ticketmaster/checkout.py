import json, base64
from urllib.parse import quote
from logs import TaskLogger

class TicketMasterCheckout:

    def __init__(self, session, task_id, profile) -> None:
        self.session = session
        self.task_id = task_id
        self.profile = profile

        self.task_id = task_id
        self.logger = TaskLogger(self.task_id)

        self.stripe_key = 'pk_live_51GxVbaHDyd0PPPQWTAzwaPI1k6Wp2aGDNVDdC2eCccHy2TTJsYARv90dvfACEcLE1uKpONCukVgV71D13I0vCTRJ001nOkYsMZ'

    def confirm_nominative(self):

        self.logger.status('Confirming nominative...')

        n = 0

        for id in self.session.confirm_nominative_data:
            if 'FirstName' in str(id):
                self.session.confirm_nominative_data[id] = self.profile['firstName'][n]
                n += 1

        n = 0

        for id in self.session.confirm_nominative_data:
            if 'LastName' in str(id):
                self.session.confirm_nominative_data[id] = self.profile['lastName'][n]
                n += 1

        try:
            r = self.session.post(
                url='https://shop.ticketmaster.it/checkout.html',
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': '/checkout.html',
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
                    'referer': 'https://shop.ticketmaster.it/checkout.html',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data=self.session.confirm_nominative_data
            )
        except Exception as e:
            self.logger.error(f'Exception on nominative confirmation: {e}. Retrying...')
            return 0

        return r

    def confirm_terms(self):

        self.logger.status('Checking out...')

        try:
            r = self.session.post(
                url='https://shop.ticketmaster.it/checkout.html',
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': '/checkout.html',
                    'content-length': '48',
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
                    'referer': 'https://shop.ticketmaster.it/checkout.html',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'applicationTermsAndConditions': '80',
                    'doSave': 'Conferma'
                }
            )
        except Exception as e:
            self.logger.error(f'Exception on terms confirmation: {e}. Retrying...')
            return 0

        return r

    def paypal_payment(self):

        self.logger.status('Paying with PayPal...')

        try:
            r = self.session.post(
                url='https://shop.ticketmaster.it/checkout.html',
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': '/checkout.html',
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
                    'referer': 'https://shop.ticketmaster.it/checkout.html',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'idOrderReservation': '',
                    'spUrlRedirect': 'show-payment_sc_92.html',
                    'PaymentInfo.cdPaymentGateway': 'PP_WWW',
                    'PaymentInfo.cdPaymentType': 'WP',
                    'PaymentInfo.isReservation': 'false',
                    'PaymentInfo.dhReservationExpire': '',
                    'doPayment': 'paga'
                },
                allow_redirects=True,
                show_redirects=True
            )
        except Exception as e:
            self.logger.error(f'Exception on PayPal submit: {e}. Retrying...')
            return 0

        self.logger.success('Successfully checked out!')

        return r
    
    def stripe_payment(self):

        self.logger.status('Paying with Stripe...')

        try:
            r = self.session.post(
                url='https://shop.ticketmaster.it/checkout.html',
                headers={
                    'method': 'POST',
                    'authority': 'shop.ticketmaster.it',
                    'scheme': 'https',
                    'path': '/checkout.html',
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
                    'referer': 'https://shop.ticketmaster.it/checkout.html',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'idOrderReservation': '',
                    'spUrlRedirect': 'show-payment_sc_92.html',
                    'PaymentInfo.cdPaymentGateway': 'STRIPE_CK_WWW',
                    'PaymentInfo.cdPaymentType': 'WP',
                    'PaymentInfo.isReservation': 'false',
                    'PaymentInfo.dhReservationExpire': '',
                    'doPayment': 'paga'
                },
                allow_redirects=True,
                show_redirects=True
            )
        except Exception as e:
            self.logger.error(f'Exception on Stripe submit: {e}. Retrying...')
            return 0

        try:
            self.stripe_url = r.url
            self.stripe_id = self.stripe_url.split('/pay/')[1].split('#')[0]

            if 'stripe' not in self.stripe_url:
                raise Exception('No Stripe detected')
        except:
            self.logger.warning('No Stripe session detected!')
            return 11

        return

    def get_stripe_data_step_0(self):

        data = {
            "v2": 2,
            "id": "29b7b478293918f57d526ad873c82a56",
            "t": 5.9,
            "tag": "4.5.42",
            "src": "js",
            "a": {
               "a": {
                  "v": "true",
                  "t": 0.6
               },
               "b": {
                  "v": "false",
                  "t": 0
               },
               "c": {
                  "v": "it-IT,it,en",
                  "t": 0
               },
               "d": {
                  "v": "MacIntel",
                  "t": 0
               },
               "e": {
                  "v": "PDF Viewer,internal-pdf-viewer,application/pdf,pdf++text/pdf,pdf, Chrome PDF Viewer,internal-pdf-viewer,application/pdf,pdf++text/pdf,pdf, Chromium PDF Viewer,internal-pdf-viewer,application/pdf,pdf++text/pdf,pdf, Microsoft Edge PDF Viewer,internal-pdf-viewer,application/pdf,pdf++text/pdf,pdf, WebKit built-in PDF,internal-pdf-viewer,application/pdf,pdf++text/pdf,pdf",
                  "t": 11.6
               },
               "f": {
                  "v": "1440w_814h_30d_2r",
                  "t": 0
               },
               "g": {
                  "v": "2",
                  "t": 0
               },
               "h": {
                  "v": "false",
                  "t": 12.8
               },
               "i": {
                  "v": "sessionStorage-enabled, localStorage-enabled",
                  "t": 13.8
               },
               "j": {
                  "v": "0100111100000000100000111100000000000010001000010111111",
                  "t": 477.9,
                  "at": 201.1
               },
               "k": {
                  "v": "",
                  "t": 0
               },
               "l": {
                  "v": self.session.headers['User-Agent'],
                  "t": 0
               },
               "m": {
                  "v": "",
                  "t": 0
               },
               "n": {
                  "v": "false",
                  "t": 294.1,
                  "at": 0.4
               },
               "o": {
                  "v": "360a4fccbb41a205c8d0199ada2f23bb",
                  "t": 232.9
               }
            },
            "b": {
                "a": "https://nzFdN-YHifp5P4jww1g5PB9gL5ke3lzMs2l5_LTmcKQ.6gpw9ZlXZLcTbP-ecjHtvCbFFySpXAFZudRv-rokQAo.NPjjFT_Lh9FNQi_kBI8nRg-sEU-ptogcIXM6XDolWjQ/",
                "b": "https://checkout.stripe.com/Ua5uAajr5DEq7upD01WGZm63DnCUP7aun5KMz4VCZk0/5ABuRyQi_LoWhrUY3adDzZW5_IcRxcyH5Cu6cCX4iyc#3hnsbP3QoMT3XYFJMSoI8658wPBWW1tKY_W6lwipiIw",
                "c": "DIcp1H04_maTmrJWtQDnRwjjKL8ap0KG74LB0LrAVvQ",
                "d": "NA",
                "e": "NA",
                "f": False,
                "g": True,
                "h": True,
                "i": [
                    "location"
                ],
                "j": [

                ],
                "n": 2426.9000000001397,
                "u": "checkout.stripe.com",
                "v": "shop.ticketmaster.it"
            },
            "h": "15b9d8ad3b6aaa7cd5ec"
        }

        self.request_6(data)

    def request_6(self, data):

        json_data = json.dumps(data)
        urlencoded_data = quote(json_data)
        encoded_data = base64.b64encode(urlencoded_data.encode('utf-8'))

        try:
            r = self.session.post(
                url='https://m.stripe.com/6',
                headers={
                    'method': 'POST',
                    'authority': 'm.stripe.com',
                    'scheme': 'https',
                    'path': '/6',
                    'content-length': '',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': self.session.headers['User-Agent'],
                    'sec-ch-ua-platform': '"macOS"',
                    'content-type': 'text/plain;charset=UTF-8',
                    'accept': '*/*',
                    'origin': 'https://m.stripe.network',
                    'sec-fetch-site': 'cross-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://m.stripe.network/',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data=encoded_data.decode('utf-8')
            )
        except Exception as e:
            self.logger.error(f'Exception on Stripe data retrieval: {e}. Retrying...')
            return 0

        try:
            self.muid = r.json()['muid']
            self.guid = r.json()['guid']
            self.sid = r.json()['sid']
        except Exception as e:
            self.logger.error(f'Exception on Stripe data retrieval: {e}. Retrying...')
            return 0

        return 1

    def get_stripe_totals(self):

        try:
            r = self.session.post(
                url=f'https://api.stripe.com/v1/payment_pages/{self.stripe_id}/init',
                headers={
                    'method': 'POST',
                    'authority': 'api.stripe.com',
                    'scheme': 'https',
                    'path': f'/v1/payment_pages/{self.stripe_id}/init',
                    'content-length': '',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'accept': 'application/json',
                    'content-type': 'application/x-www-form-urlencoded',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': self.session.headers['User-Agent'],
                    'sec-ch-ua-platform': '"macOS"',
                    'origin': 'https://checkout.stripe.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://checkout.stripe.com/',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'key': self.stripe_key,
                    'eid': 'NA',
                    'browser_locale': 'it-IT',
                    'redirect_type': 'url',
                }
            )
        except Exception as e:
            self.logger.error(f'Exception on Stripe totals retrieval: {e}. Retrying...')
            return 0

        try:
            self.total = r.json()['line_item_group']['total']
            self.last_total = r.json()['line_item_group']['line_items'][-1]['subtotal']
        except Exception as e:
            self.logger.error(f'Exception on Stripe totals retrieval: {e}. Retrying...')
            return 0

        return 1

    def submit_payment_method(self):

        try:
            r = self.session.post(
                url='https://api.stripe.com/v1/payment_methods',
                headers={
                    'method': 'POST',
                    'authority': 'api.stripe.com',
                    'scheme': 'https',
                    'path': '/v1/payment_methods',
                    'content-length': '',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'accept': 'application/json',
                    'content-type': 'application/x-www-form-urlencoded',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': self.session.headers['User-Agent'],
                    'sec-ch-ua-platform': '"macOS"',
                    'origin': 'https://checkout.stripe.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://checkout.stripe.com/',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'type': 'card',
                    'card[number]': self.profile['card_number'],
                    'card[cvc]': self.profile['card_cvv'],
                    'card[exp_month]': self.profile['card_month_expiration'],
                    'card[exp_year]': self.profile['card_year_expiration'],
                    'billing_details[name]': f'{self.profile["firstName"]} {self.profile["lastName"]}',
                    'billing_details[email]': self.profile['email'],
                    'billing_details[address][country]': 'IT',
                    'guid': self.guid,
                    'muid': self.muid,
                    'sid': self.sid,
                    'key': self.stripe_key,
                    'payment_user_agent': 'stripe.js/1f3998f34; stripe-js-v3/1f3998f34; checkout'
                }
            )
        except Exception as e:
            self.logger.error(f'Exception on Stripe payment method submit: {e}. Retrying...')
            return 0

        try:
            self.payment_method_id = r.json()['id']
        except Exception as e:
            self.logger.error(f'Exception on Stripe payment method submit: {e}. Retrying...')
            return 0

    def submit_order(self):

        try:
            r = self.session.post(
                url=f'https://api.stripe.com/v1/payment_pages/{self.stripe_id}/confirm',
                headers={
                    'method': 'POST',
                    'authority': 'api.stripe.com',
                    'scheme': 'https',
                    'path': f'/v1/payment_pages/{self.stripe_id}/confirm',
                    'content-length': '',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'accept': 'application/json',
                    'content-type': 'application/x-www-form-urlencoded',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': self.session.headers['User-Agent'],
                    'sec-ch-ua-platform': '"macOS"',
                    'origin': 'https://checkout.stripe.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://checkout.stripe.com/',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'eid': 'NA',
                    'payment_method': self.payment_method_id,
                    'expected_amount': str(self.total),
                    'last_displayed_line_item_group_details[subtotal]': str(self.last_total),
                    'last_displayed_line_item_group_details[total_exclusive_tax]': '0',
                    'last_displayed_line_item_group_details[total_inclusive_tax]': '0',
                    'last_displayed_line_item_group_details[total_discount_amount]': '0',
                    'last_displayed_line_item_group_details[shipping_rate_amount]': '0',
                    'expected_payment_method_type': 'card',
                    'key': self.stripe_key,
                }
            )
        except Exception as e:
            self.logger.error(f'Exception on Stripe order submit: {e}. Retrying...')
            return 0

        try:
            #success_url = r.json()['success_url']
            if r.json()['payment_intent'].get('next_action', None) != None:
                self.logger.warning('Checkout requires 3D Secure!')
                self.secure_src = r.json()['payment_intent']['next_action']['use_stripe_sdk']['three_d_secure_2_source']
                return 111
            else:
                self.logger.success('Successfully checked out!')
                return 1
        except:
            self.logger.error('Checkout failed!')
            return 11

    def submit_3d_secure(self):

        self.logger.status('Submitting 3D Secure...')

        browser = {
            "fingerprintAttempted": False,
            "fingerprintData": None,
            "challengeWindowSize": None,
            "threeDSCompInd": "Y",
            "browserJavaEnabled": False,
            "browserJavascriptEnabled": True,
            "browserLanguage": "it-IT",
            "browserColorDepth" :"30",
            "browserScreenHeight": "900",
            "browserScreenWidth": "1440",
            "browserTZ": "-120",
            "browserUserAgent": self.session.headers['User-Agent']
        }

        try:
            r = self.session.post(
                url='https://api.stripe.com/v1/3ds2/authenticate',
                headers={
                    'method': 'POST',
                    'authority': 'api.stripe.com',
                    'scheme': 'https',
                    'path': '/v1/3ds2/authenticate',
                    'content-length': '',
                    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                    'accept': 'application/json',
                    'content-type': 'application/x-www-form-urlencoded',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': self.session.headers['User-Agent'],
                    'sec-ch-ua-platform': '"macOS"',
                    'origin': 'https://js.stripe.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://js.stripe.com/',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'it-IT,it;q=0.9,en;q=0.8',
                },
                data={
                    'source': self.secure_src,
                    'browser': json.dumps(browser),
                    'one_click_authn_device_support[hosted]': 'false',
                    'one_click_authn_device_support[same_origin_frame]': 'false',
                    'one_click_authn_device_support[spc_eligible]': 'true',
                    'one_click_authn_device_support[webauthn_eligible]': 'true',
                    'one_click_authn_device_support[publickey_credentials_get_allowed]': 'true',
                    'key': self.stripe_key
                }
            )
        except Exception as e:
            self.logger.error(f'Exception on Stripe 3D Secure submit: {e}. Retrying...')
            return 0

        self.logger.success(f'3D Secure State: {r.json().get("state")}')

        return 1