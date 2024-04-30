import os
import requests
import time

dapr_port = os.environ.get("DAPR_HTTP_PORT", 3500)
dapr_url = f'http://localhost:{dapr_port}/v1.0/invoke'
app_id = 'web'
namespace = 'microservice'
method = 'microservice'
url = f'{dapr_url}/{app_id}.{namespace}/method/{method}'


n = 0
while True:

    # load micro service
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    print("HTTP %d => %s" % (response.status_code, response.content.decode("utf-8")), flush=True)

    time.sleep(1)
