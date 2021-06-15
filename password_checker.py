import requests
import hashlib


#check the head of the hashed password in password checker
#return list of mmatching complete hashes
def request_api(hashed):
    url = "https://api.pwnedpasswords.com/range/" + hashed

    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError("Connection Error")
    return res
#check list of complete hashed passwords with tail of own hash
#if they match, the password has alreadby been expossd
def read_response(hashes, hashes_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for hash, count in hashes:
        if hash == hashes_to_check:
            return f"Your password has been exposed {count} times"
    return "Your password has never been exposed"


#get hashed password 
#divide the hash in 2 parts, head(first_5) and tail
#input the head in the password checker
def check_api(password):
    hashed_pass = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first_5, tail = hashed_pass[:5], hashed_pass[5:]
    response = request_api(first_5)
    return read_response(response, tail)


#Input passwords to check
def main():
    passwords = input("Input password/s to check ").split()
    for password in passwords:
        print(check_api(password))

main()
