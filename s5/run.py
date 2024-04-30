import uvicorn
from fastapi import FastAPI

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40005


@app.get('/s5')
async def s5():
    return {'current_service': 's5', 'result': 'micro service 5'}


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
