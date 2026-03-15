import requests
import concurrent.futures
a = {
    1:2,2:3
}
a.

data = [{
  "firstName": "admin",
  "lastName": "admin",
  "email": "admin@admin.com",
  "phone": "9698443248",
  "password": "dev@1234"
},{
  "firstName": "Sylvia",
  "lastName": "Kincla",
  "email": "skincla0@reuters.com",
  "phone": "9698443248",
  "password": "zX2|YLf{c.q7\\enl"
}, {
  "firstName": "Kendrick",
  "lastName": "Shercliff",
  "email": "kshercliff1@stumbleupon.com",
  "phone": "5847084949",
  "password": "xY4{WQA/NY>W{u"
}, {
  "firstName": "Dirk",
  "lastName": "Haseley",
  "email": "dhaseley2@sourceforge.net",
  "phone": "5357786245",
  "password": "jR2,j2oL"
}, {
  "firstName": "Rooney",
  "lastName": "Pagitt",
  "email": "rpagitt3@ebay.co.uk",
  "phone": "5793482096",
  "password": "kF9>\"@gI5#L}v"
}, {
  "firstName": "Onida",
  "lastName": "Trotton",
  "email": "otrotton4@nhs.uk",
  "phone": "6322991655",
  "password": "vB6@?|jDZ\"b(a"
}, {
  "firstName": "Sheree",
  "lastName": "Paule",
  "email": "spaule5@si.edu",
  "phone": "7499770686",
  "password": "wU9@7Y3Ig}xK"
}, {
  "firstName": "Celine",
  "lastName": "Knighton",
  "email": "cknighton6@paypal.com",
  "phone": "7207641143",
  "password": "cZ5`X@7z77zz}P"
}, {
  "firstName": "Clem",
  "lastName": "Wile",
  "email": "cwile7@ning.com",
  "phone": "7728556124",
  "password": "kA1&(0@iYL,/lZz_"
}, {
  "firstName": "Millicent",
  "lastName": "Pavitt",
  "email": "mpavitt8@macromedia.com",
  "phone": "2734218178",
  "password": "kK1/D@<BrU|J~<R4"
}, {
  "firstName": "Der",
  "lastName": "Roarty",
  "email": "droarty9@liveinternet.ru",
  "phone": "6279267593",
  "password": "mA1.VSwr_N?S}t9!"
}]

url = 'http://localhost:5135/User/register'

def send_post(user_data):
    try:
        response = requests.post(url, json=user_data)
        print(f"Sent {user_data['firstName']}: {response.json()}\n")
    except Exception as e:
        print(f"Error sending {user_data['firstName']}: {e}")

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(send_post, data)