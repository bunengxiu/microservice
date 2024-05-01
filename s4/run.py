import uvicorn
import httpx
from fastapi import FastAPI

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40004
dapr_port: int = 3500
dapr_url = f'http://localhost:{dapr_port}/v1.0/invoke'
s5_app_id = 's5'
namespace = 'default'
s5_method = 's5'
s5_url = f'{dapr_url}/{s5_app_id}.{namespace}/method/{s5_method}'


@app.get('/s4')
async def s4():
    async with httpx.AsyncClient() as client:
        s5_res = await client.get(url=s5_url, headers={'Content-Type': 'application/json'})
        print(f'get from s5: {s5_res.json()}')
    return {'current_service': 's4', 's5': s5_res.json()}


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
