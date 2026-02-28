import requests

ACCOUNT_ID = "39b9286657afb3df954710a73a503db2"
NAMESPACE_ID = "a7f575cdaed04a8ebab08cabaf421005"
API_TOKEN = "t3LCXkymK3jdt5oXPrBdEO1oIRTUKkBLvGxUWvCE"

with open("brain.json", "rb") as f:
    data = f.read()

url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/storage/kv/namespaces/{NAMESPACE_ID}/values/brain"

response = requests.put(
    url,
    headers={"Authorization": f"Bearer {API_TOKEN}"},
    data=data
)

print(response.status_code, response.json())
