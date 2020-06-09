import time

import requests

from config import config
from os import environ as env

from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def email_notification(text, enabled=config.EMAIL_NOTIFICATION):
    if not enabled:
        return

    message = Mail(
        from_email=config.SENDER,
        to_emails=config.EMAIL,
        subject='Manning Book sale!',
        html_content='{}'.format(text)
    )
    try:
        sg = SendGridAPIClient(env.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


class BookWatchDog:

    def __init__(self, url):
        self.url = url

    def get_page(self):
        resp = requests.get(self.url)
        if resp.status_code == 200:
            return resp.text

        return None

    def get_item(self):
        content = self.get_page()
        if not content:
            return None
        bs = BeautifulSoup(content, 'html.parser')
        book_name = bs.find('title').text.strip()
        book_price = bs.findAll('span', class_='pull-right price')[0].text.strip()

        return book_name, book_price


if __name__ == '__main__':
    for book_url, max_price in config.books:
        scraper = BookWatchDog(book_url)
        book, price = scraper.get_item()
        if price:
            price = float(price.replace('$', ''))
            msg = '{}: {}'.format(book, price)
            print(msg)
            if price <= max_price:
                email_notification(msg)
        time.sleep(5)
