import uvicorn
import httpx
from fastapi import FastAPI

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40000
dapr_port: int = 3500
dapr_url = f'http://localhost:{dapr_port}/v1.0/invoke'
s1_app_id = 's1'
s2_app_id = 's2'
namespace = 'microservice'
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


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
