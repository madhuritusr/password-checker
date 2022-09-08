import requests
import hashlib


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Error Fetching: {response.status_code}, check the API and try again!")
    return response


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_chars, tail = sha1password[:5], sha1password[5:]
    response2 = request_api_data(first5_chars)
    return get_password_leaks_count(response2, tail)


with open("./password.txt", "r") as password_file:
    password = password_file.read()
count = pwned_api_check(password)
if count:
    print(f"{password} was found {count} times...You should probably change it")

else:
    print(f"{password} was NOT found. Carry On!")
