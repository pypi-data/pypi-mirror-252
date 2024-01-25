from http.cookiejar import MozillaCookieJar

from playwright.sync_api import sync_playwright

from .utils import set_cookies

class CASPass:
    def __init__(self, login_urls, success_url):
        self._login_urls  = login_urls
        self._success_url = success_url
    
    def login(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context();
            page = context.new_page()

            for url in self._login_urls:
                page.goto(url)

            page.wait_for_url(self._success_url)
            cookielist = context.cookies()

            browser.close()

        self._cookiejar = MozillaCookieJar()
        set_cookies(cookielist, self._cookiejar)

    def save(self, path):
        self._cookiejar.save(path)
