import uvicorn
import httpx
from fastapi import FastAPI, Request

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40000
dapr_port: int = 3500
namespace = 'default'
dapr_url = f'http://localhost:{dapr_port}/v1.0/invoke'
state_url = f'http://localhost:{dapr_port}/v1.0/state/statestore'
publish_url = f'http://localhost:{dapr_port}/v1.0/publish/pubsub'
input_bindings_url = f'http://localhost:{dapr_port}/v1.0/bindings/bindings'
s1_app_id = 's1'
s2_app_id = 's2'
s1_method = 's1'
s2_method = 's2'
s1_url = f'{dapr_url}/{s1_app_id}.{namespace}/method/{s1_method}'
s2_url = f'{dapr_url}/{s2_app_id}.{namespace}/method/{s2_method}'


@app.get('/microservice')
async def microservice():
    async with httpx.AsyncClient() as client:
        s1_res = await client.get(url=s1_url, headers={'Content-Type': 'application/json'})
        print(f'get from s1: {s1_res.json()}')
    async with httpx.AsyncClient() as client:
        s2_res = await client.get(url=s2_url, headers={'Content-Type': 'application/json'})
        print(f'get from s2: {s2_res.json()}')
    return {'current_service': 'web', 's1': s1_res.json(), 's2': s2_res.json()}


@app.post('/neworder')
async def neworder(order_info: dict):
    async with httpx.AsyncClient() as client:
        state = [{'key': 'order', 'value': order_info}]
        state_res = await client.post(url=state_url, json=state)
        print(f'status code: {state_res.status_code}')
    return {'current_service': 'web', 'status code': state_res.status_code}


@app.get('/order')
async def order():
    async with httpx.AsyncClient() as client:
        state_res = await client.get(url=f'{state_url}/order')
        print(f'status code: {state_res.status_code}')
        try:
            print(f'get from state: {state_res.json()}')
        except Exception as e:
            print(e)
    return {'current_service': 'web', 'order': state_res.json()}


@app.post('/publish')
async def publish(message: dict):
    async with httpx.AsyncClient() as client:
        print(f'publish message: {message}')
        pub_res = await client.post(url=f'{publish_url}/orders', json=message)
        print(f'publish, status code: {pub_res.status_code}')
    return {'current_service': 'web', 'publish status code': pub_res.status_code}


@app.get('/dapr/subscribe')
async def subscribe():
    subscriptions = [{'pubsubname': 'pubsub', 'topic': 'orders', 'route': 'orders'}]
    print(f"subscribe message: {subscriptions}", flush=True)
    return subscriptions


@app.post('/orders')
async def order_subscribe(request: Request):
    message = await request.json()
    print(f"Received message {message}", flush=True)
    return {'success': True, 'received message info': message}


@app.post('/input-bindings')
async def input_bindings(payload: dict):
    async with httpx.AsyncClient() as client:
        print(f'input bindings: {payload}')
        input_res = await client.post(url=input_bindings_url, json=payload)
        print(f'input bindings, status code: {input_res.status_code}')
    return {'current_service': 'web', 'input bindings status code': input_res.status_code}


@app.post('/bindings')
async def out_bindings(request: Request):
    payload = await request.json()
    print(f"out bindings, Received payload {payload}", flush=True)
    return {'current_service': 'web', 'received payload info': payload}


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
