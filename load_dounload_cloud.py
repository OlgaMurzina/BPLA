import json
from random import uniform
import requests

username = 'olmur'
token = ''
path = '/home/olmur/quadrocopter'
content2 = {  'vx': uniform(0, 3),
              'vy': uniform(0, 3),
              'vz': uniform(0, 3)}
content = json.dumps(content2)

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{path}/sensor.in'.format(
        username=username, path=path ),
        headers={'Authorization': 'Token {token}'.format(token=token)},
        files = {'content': content}
)

if response.status_code in [200, 201]:
    print('File uploaded')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

response = requests.get('https://www.pythonanywhere.com/api/v0/user/{username}/files/path{path}/sensor.in'.format(
        username=username,
        path=path ),
        headers={'Authorization': 'Token {token}'.format(token=token)})

try:
    file1 = response
    content1 = json.loads(file1.content)

    if content1 == content2:
        print("Файлы идентичны")
    else:
        print("Файлы имеют различия")

except Exception as e:
    print(e)
