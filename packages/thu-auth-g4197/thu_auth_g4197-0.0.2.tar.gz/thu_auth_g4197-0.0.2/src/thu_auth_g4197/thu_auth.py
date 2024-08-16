from gmssl import sm2
import requests
import re
import gmssl
import binascii

def sm2_encrypt(data):
    pub_key = "04d0c9e1ae89279fe05b435d63e3eba437bf510e09da5f71558974a19dc596724227f08dc2fc6e74bbb9d8b468d4dd5205e9b6793a3bbc48df3fdf219b3ea140e3"
    sm2_crypt = sm2.CryptSM2(public_key=pub_key, private_key="", mode=1)
    enc_bytes = sm2_crypt.encrypt(data.encode())
    enc_hex = "04" + binascii.hexlify(enc_bytes).decode().lower()
    return enc_hex


def auth(auth_url, username, password):
    """
    A simple cross-auth for Tsinghua ID.
    @params:
        auth_url: URL which will be redirected to Tsinghua auth page.
        username: the username of Tsinghua ID
        password: the password of Tsinghua ID
    @return:
        a dict of cookies after authentication
    """
    s = requests.Session()
    s.get(auth_url, allow_redirects=True)  # Tsinghua id system
    res = s.post("https://id.tsinghua.edu.cn/do/off/ui/auth/login/check", data={
        "i_user": username,
        "i_pass": sm2_encrypt(password),
        "i_captcha": "",
        "fingerGenPrint": "",
        "fingerPrint": "f3a0bd61cfc0b8bda7047ef5c2fdbe22"
    })
    redirect_url = re.findall(r'<a href="([\s\S]+?)">直接跳转', res.text)[0]
    s.get(redirect_url, allow_redirects=True)
    return s.cookies.get_dict()
