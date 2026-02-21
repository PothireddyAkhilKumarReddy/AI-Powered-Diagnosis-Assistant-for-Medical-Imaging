import requests
try:
    with open('test.png', 'rb') as f:
        print(requests.post('http://localhost:5003/api/predict', files={'image': ('test.png', f)}).json())
except Exception as e:
    print("Predict failed:", repr(e))
