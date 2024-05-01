import uvicorn
import httpx
from fastapi import FastAPI

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40002
dapr_port: int = 3500
dapr_url = f'http://localhost:{dapr_port}/v1.0/invoke'
s4_app_id = 's4'
namespace = 'default'
s4_method = 's4'
s4_url = f'{dapr_url}/{s4_app_id}.{namespace}/method/{s4_method}'


@app.get('/s2')
async def s2():
    async with httpx.AsyncClient() as client:
        s4_res = await client.get(url=s4_url, headers={'Content-Type': 'application/json'})
        print(f'get from s4: {s4_res.json()}')
    return {'current_service': 's2', 's4': s4_res.json()}


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
