# CASPass - Login through Central Authentification Systems

## Motivation

When you write a web scraper, Central Authentification Systems are often
difficult to get through. Most of them use a lot of Javascript and protection
mechanisms, so it's complex to automate. Moreover, you need to understand a
completely different logic, which is useless with respect to the website you
want to scrap.

The chosen approach for `CASPass` is to avoid completely to understand the CAS
logic and to rely on a full browser, namely
[Playwright](https://github.com/Microsoft/playwright-python), to authenticate.
This a semi-automatic process since you need to manually enter your credentials,
on the login page you are used to work with. But it's only needed one time,
`CASPass` save all the cookies into a file which can be used by a traditional
scrapper library (like [requests](https://requests.readthedocs.io/) or
[httpx](https://github.com/encode/httpx)).

Obviously this semi-automatic approach is not usable in a fully non-interactive
context, like a CI/CD system. However, it has many advantages:

- no need to understand the CAS,
- no need to bother with Captcha,
- no complex logic to understand,
- moreover, most of the authentication tokens stored in cookies have a pretty
  long duration, so you will only have to manually log in from time to time.

`CASPass` works also without a CAS: when the login process is full of
Javascript, Captcha or other security checks and too complex to automate, just
use this module to authenticate and then perform the scraping with a more
efficient tool.

## Usage

The `CASPass` constructor expects two arguments:

- a list of URL leading to the login page (you may need to provide multiple
  links in order to satisfy the security checks)
- the success URL, reached after successful login (it indicates the login
  process is terminated)

``` python
from caspass import CASPass

cas = CASPass([url, url_login], url_success)
cas.login()
cas.save("cookies.txt")
```

See `examples/` for some complete examples.

# Licence

GPLv3+
