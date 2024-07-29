from time import sleep
import httpx


class Tempgmail:
    def __init__(self):
        self.link = "https://22.do/zh"
        self.client = httpx.Client()
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'

    def generate(self):
        result = httpx.post(f"{self.link}/mailbox/generate", headers={'User-Agent': self.ua}, data={'type': 'Gmail'})
        return result.json()["data"]["address"]["email"]

    def mailbox(self, mail):
        self.client.post(f"{self.link}/mailbox", headers={'User-Agent': self.ua}, data={'mail': mail, 'Gmail': 'on'})

    def wait_mail(self):
        while True:
            result = self.client.get(f"{self.link}/mailbox/check", headers={'User-Agent': self.ua}).json()
            if result['action'] == "OK":
                from_mail = result['Msg'][0]['from']
                msgid = result['Msg'][0]['mailId']
                return from_mail, msgid
            print("正在等待邮件")
            sleep(2)

    def html_text(self, msgid):
        return self.client.get(f"{self.link}/content/{msgid}/html", headers={'User-Agent': 'Mozilla/5.0'})


tempgmail = Tempgmail()
mail = tempgmail.generate()
print(mail)
tempgmail.mailbox(mail)
from_mail, msgid = tempgmail.wait_mail()
print(tempgmail.html_text(msgid))
