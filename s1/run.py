import uvicorn
import httpx
from fastapi import FastAPI

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40001
dapr_port: int = 3500
dapr_url = f'http://localhost:{dapr_port}/v1.0/invoke'
s3_app_id = 's3'
namespace = 'default'
s3_method = 's3'
s3_url = f'{dapr_url}/{s3_app_id}.{namespace}/method/{s3_method}'


@app.get('/s1')
async def s1():
    async with httpx.AsyncClient() as client:
        s3_res = await client.get(url=s3_url, headers={'Content-Type': 'application/json'})
        print(f'get from s3: {s3_res.json()}')
    return {'current_service': 's1', 's3': s3_res.json()}


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
