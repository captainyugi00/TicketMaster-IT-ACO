import dragontls, csv, threading, logging, settings, time

from ticketmaster import (
    TicketMasterLogin,
    TicketMasterProduct,
    TicketMasterCheckout
)

from captcha_solver import (
    init_autosolve
)

from checkouts import (
    add_checkout,
    check_if_checked_out
)

config = settings.get_config()

print('Initiating AYCD')

init_autosolve(
    client_key=config['aycd_client_key'],
    access_token=config['aycd_access_token'], 
    api_key=config['aycd_api_key']
)

def task_flow(task_id, username, password, profile, url, ticket_quantity, ticket_type):

    logged_in = False

    session = dragontls.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

    tprod = TicketMasterProduct(
        session=session, 
        url=url, 
        ticket_quantity=ticket_quantity, 
        ticket_type=ticket_type.strip(), 
        max_price=30000, 
        task_id=task_id
    )

    while True:
        product_response = tprod.get_product()

        if product_response == 0:
            time.sleep(5)
            continue

        if not logged_in:
            login = TicketMasterLogin(
                session=session, 
                username=username, 
                password=password, 
                task_id=task_id
            )

            login_url = None

            while True:
                login_response = tprod.get_login_url(product_response=str(product_response.text))

                if login_response == 0:
                    continue
                else:
                    login_url = login_response.url
                    break

            #while True:
            #    if login.get_login() == 0:
            #        continue
            #    break

            while True:
                if login.post_login(referer=login_url) == 0:
                    continue

                break

            logged_in = True

        if tprod.select_tickets(product_response=str(product_response.text)) == 0:
            time.sleep(5)
            continue

        break

    while True:
        atc_response = tprod.add_to_cart()
    
        if atc_response == 0:
            continue

        break

    tcheckout = TicketMasterCheckout(session=session, task_id=task_id, profile=profile)

    if session.confirm_nominative == True:
        while True:
            conf_nominative = tcheckout.confirm_nominative()

            if conf_nominative == 0:
                continue

            break

    while True:
        conf_terms = tcheckout.confirm_terms()

        if conf_terms == 0:
            continue

        break

    if check_if_checked_out(username, profile['firstName'], profile['lastName']) == url:
        logging.info(f'Max checkouts reached for {profile["firstName"]} {profile["lastName"]}')
        return 1

    while True:
        str_payment = tcheckout.stripe_payment()

        if str_payment in [0, 11]:
            continue

        break

    while True:
        str_totals = tcheckout.get_stripe_totals()

        if str_totals == 0:
            continue

        break

    while True:
        str_data_step_0 = tcheckout.get_stripe_data_step_0()

        if str_data_step_0 == 0:
            continue

        break

    while True:
        p_method = tcheckout.submit_payment_method()

        if p_method == 0:
            continue

        break

    while True:
        s_order = tcheckout.submit_order()

        if s_order == 0:
            continue
        elif s_order == 1:
            add_checkout(username, profile['firstName'], profile['lastName'], url)
        elif s_order == 111:
            add_checkout(username, profile['firstName'], profile['lastName'], url)

            while True:
                if tcheckout.submit_3d_secure() == 0:
                    continue
                else:
                    break

        break

with open('tasks.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            t = threading.Thread(
                target=task_flow,
                args=[
                    f'TicketMaster-{line_count}', # Task ID
                    row[1], # Task Username
                    row[2], # Task Password
                    {
                        'firstName': row[3].split('|'),
                        'lastName': row[4].split('|'),
                        'email': row[5],
                        'card_number': row[6],
                        'card_cvv': row[7],
                        'card_month_expiration': row[8],
                        'card_year_expiration': row[9]
                    },
                    row[0], # Task URL
                    row[11], # Task Ticket(s) Quantity
                    row[10], # Task Ticket(s) Type
                ]
            )

            t.start()

            line_count += 1
