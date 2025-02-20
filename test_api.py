import requests

url = "http://127.0.0.1:8000/api/explain/"
data = {"text": "Quantum computing leverages superposition and entanglement..."}

try:
    response = requests.post(url, json=data)
    print(response.json())
except requests.exceptions.ConnectionError:
    print("Could not connect to the server.")
