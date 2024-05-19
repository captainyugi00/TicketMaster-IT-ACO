from autosolveclient import AutoSolve
import json
import time
import logging

auto_solve = None
aycd_tokens = {}

def aycd_response(json_response):

    global aycd_tokens

    json_response = json.loads(json_response)
    aycd_tokens[json_response['taskId']] = json_response['token']

def init_autosolve(client_key, access_token, api_key):

    global auto_solve

    auto_solve_factory = AutoSolve({
        "access_token": access_token,
        "api_key": api_key,
        "client_key": client_key,
        "debug": False,
        "should_alert_on_cancel": True
    })

    auto_solve = auto_solve_factory.get_instance()

    # Initializes all connections, is not blocking
    auto_solve.init()

    # Blocking, to ensure init is completed. Not necessary if send is not called until
    # later
    auto_solve.initialized()

    # The handle functions are created by you to handle events however you like.
    auto_solve.emitter.on('AutoSolveResponse', aycd_response)

def send_to_autosolve(message):

    logging.info('Sending to AYCD')

    global auto_solve, aycd_tokens

    task_id = message['taskId']

    auto_solve.send_token_request(message)

    while str(task_id) not in aycd_tokens:
        logging.info('Waiting for captcha...')
        time.sleep(1)
        continue

    solved_captcha = aycd_tokens[str(task_id)]

    aycd_tokens.pop(task_id)

    return solved_captcha
