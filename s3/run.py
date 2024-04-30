import uvicorn
from fastapi import FastAPI

app: FastAPI = FastAPI()
host = '0.0.0.0'
port = 40003


@app.get('/s3')
async def s3():
    return {'current_service': 's3', 'result': 'micro service 3'}


if __name__ == '__main__':
    uvicorn.run('run:app',
                host=host,
                port=port
                )
