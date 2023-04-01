# Singing RSA

> 2023-04-1, author: [medic](https://github.com/aljazmedic)

## Show why it is a bad idea to let user control what RSA signs
 The solution is to get public key `(n,e)`. Then get the data you want to get the signature of: `x`.
 Pick arbitrary number `a`, coprime with n. Let's say `a = 2`. Then calculate `x' = x * (a^e) (mod n)`.
 Submit `x'` to the server, and it will return `s' = s * a (mod n)`. Now you can calculate `s = s' * a^-1 (mod n)`.
 That is the signature of `x`.

## Running
 - Copy .env.example to .env and fill in the values
 - Run `docker-compose up -d`

## Solution
Look at solution script [sol.py](sol.py).
Notes: on windows you need to do `pip install pycryptodome`, on linux `pip install pycrypto`.