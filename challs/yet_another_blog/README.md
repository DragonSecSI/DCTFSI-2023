# Yet another blog

> 2023-03-30, author: [medic](https://github.com/aljazmedic)

## Demonstrate JWT algorithm confusion attack
 Get public key from certificate of https, and use it with `alg: HS256` header to inject yourself to becoma admin user.

## Running
 - Copy .env.example to .env and fill in the values
 - Populate certs/ with the `cert.pem` and `key.pem`
 - Run `docker-compose up -d`

## TODO!
 - remove testing from package.json

### Self signed certificate
 `openssl req -new -newkey rsa:2048 -days 365 -nodes -sha256 -x509 -keyout key.pem -out cert.pem`