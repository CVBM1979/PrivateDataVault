import requests

# Tente acessar a página inicial do servidor
try:
    response = requests.get('http://127.0.0.1:5000')
    print(f"Index page response: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Failed to access index page: {e}")

# Tente acessar o endpoint /get_token
try:
    response = requests.get('http://127.0.0.1:5000/get_token')
    print(f"Get token response: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Failed to access get_token endpoint: {e}")