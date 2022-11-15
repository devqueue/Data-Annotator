import requests
import os

PATH = ''
API_ENDPOINT = '/uploadapi'
FILES = os.listdir(PATH)
PATHS = []

for file in FILES:
    tmp = os.path.join(PATH, file)
    PATHS.append(tmp)

# sending requests
for file in PATHS:
    print(f"[INFO]: Uploading: {file}")
    file_ob = {'file_name': open(file, 'rb')}
    r = requests.post(API_ENDPOINT, files=file_ob)
    print(r.status_code)
    print(r.content)

#\14DG0804_WES_MDL.xlsx