checkouts = {}

def check_if_checked_out(username, first_name, last_name):

    global checkouts

    if checkouts.get(username, None) is None:
        return 0

    if checkouts[username].get(f'{first_name} {last_name}', None) is not None:
        return checkouts[username].get(f'{first_name} {last_name}', None)
    else:
        return 0

def add_checkout(username, first_name, last_name, order_response):

    global checkouts

    if checkouts.get(username, None) is None:
        checkouts[username] = {}

    if isinstance(first_name, list) and isinstance(last_name, list):
        n = 0
        for _ in first_name:
            checkouts[username][f'{first_name[n]} {last_name[n]}'] = order_response
            n += 1
    else:
        checkouts[username][f'{first_name} {last_name}'] = order_response
