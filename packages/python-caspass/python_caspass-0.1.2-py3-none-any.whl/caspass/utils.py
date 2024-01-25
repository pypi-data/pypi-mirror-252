from http.cookiejar import Cookie

def set_cookies(cookies, cookiejar):
    for cookie in cookies:
        # https://github.com/python/cpython/blob/3.8/Lib/http/cookiejar.py#L736
        ck = Cookie(None,
                    cookie["name"],
                    cookie["value"],
                    cookie.get("port", None),
                    cookie.get("port", None) is not None,
                    cookie["domain"],
                    True,
                    cookie["domain"][0] == ".",
                    cookie['path'],
                    True,
                    cookie["secure"],
                    cookie.get('expiry', None),
                    False,
                    None,
                    None,
                    [],
                    None
        )
        cookiejar.set_cookie(ck)
