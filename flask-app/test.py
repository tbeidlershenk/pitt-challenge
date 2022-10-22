import requests
import sys
 
path = sys.argv[1]
resp = requests.post("http://localhost:5000/predict",
                   files={'file': open(path, 'rb')})
print(resp.text)
