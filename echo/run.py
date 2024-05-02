import uvicorn
from fastapi import FastAPI

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40006


@app.get('/echo')
async def echo():
    return {'result': 'successful authorization'}


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
