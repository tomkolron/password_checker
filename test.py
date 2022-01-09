import requests
req = requests.get('https://api.pwnedpasswords.com/range/f9a4c')
print(req.text)