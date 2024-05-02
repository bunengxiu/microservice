import os
import requests
import time

dapr_port = os.environ.get("DAPR_HTTP_PORT", 3500)
dapr_url = f'http://localhost:{dapr_port}/v1.0/invoke'


def microservice(ul):
    # load micro service
    response = requests.get(ul, headers={'Content-Type': 'application/json'})
    print("HTTP %d => %s" % (response.status_code, response.content.decode("utf-8")), flush=True)


def neworder(nu, ul):
    message = {"orderId": nu}
    print(f'url: {ul}, order: {message}')
    response = requests.post(ul, json=message, headers={'Content-Type': 'application/json'})
    print("HTTP %d => %s" % (response.status_code, response.content.decode("utf-8")), flush=True)


def order(ul):
    print(f'url: {ul}')
    response = requests.get(ul, headers={'Content-Type': 'application/json'})
    print("HTTP %d => %s" % (response.status_code, response.content.decode("utf-8")), flush=True)


def publish(nu, ul):
    message = {"orderId": nu}
    print(f'publish message, url: {ul}, message: {message}')
    response = requests.post(ul, json=message, headers={'Content-Type': 'application/json'})
    print("HTTP %d => %s" % (response.status_code, response.content.decode("utf-8")), flush=True)


def input_bindings(nu, ul):
    payload = {"data": {"orderId": nu}, 'operation': 'create'}
    print(f'input bindings url: {ul}, data: {payload}')
    response = requests.post(ul, json=payload, headers={'Content-Type': 'application/json'})
    print("HTTP %d => %s" % (response.status_code, response.content.decode("utf-8")), flush=True)


n = 0
while True:
    n += 1
    app_id = 'web'
    namespace = 'default'

    # load micro service
    method = 'microservice'
    url = f'{dapr_url}/{app_id}.{namespace}/method/{method}'
    microservice(url)

    # load neworder
    method = 'neworder'
    url = f'{dapr_url}/{app_id}.{namespace}/method/{method}'
    neworder(n, url)

    # load order
    method = 'order'
    url = f'{dapr_url}/{app_id}.{namespace}/method/{method}'
    order(url)

    # publish message
    method = 'publish'
    url = f'{dapr_url}/{app_id}.{namespace}/method/{method}'
    publish(n, url)

    # publish message
    method = 'input-bindings'
    url = f'{dapr_url}/{app_id}.{namespace}/method/{method}'
    input_bindings(n, url)

    time.sleep(1)
