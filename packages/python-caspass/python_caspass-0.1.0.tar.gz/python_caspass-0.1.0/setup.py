# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caspass']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.2,<0.0.3',
 'httpx>=0.26.0,<0.27.0',
 'playwright>=1.32.1,<2.0.0',
 'python-decouple>=3.8,<4.0']

setup_kwargs = {
    'name': 'python-caspass',
    'version': '0.1.0',
    'description': '',
    'long_description': '# CASPass - Login through Central Authentification Systems\n\n## Motivation\n\nWhen you write a web scraper, Central Authentification Systems are often\ndifficult to get through. Most of them use a lot of Javascript and protection\nmechanisms, so it\'s complex to automate. Moreover, you need to understand a\ncompletely different logic, which is useless with respect to the website you\nwant to scrap.\n\nThe chosen approach for `CASPass` is to avoid completely to understand the CAS\nlogic and to rely on a full browser, namely\n[Playwright](https://github.com/Microsoft/playwright-python), to authenticate.\nThis a semi-automatic process since you need to manually enter your credentials,\non the login page you are used to work with. But it\'s only needed one time,\n`CASPass` save all the cookies into a file which can be used by a traditional\nscrapper library (like [requests](https://requests.readthedocs.io/) or\n[httpx](https://github.com/encode/httpx)).\n\nObviously this semi-automatic approach is not usable in a fully non-interactive\ncontext, like a CI/CD system. However, it has many advantages:\n\n- no need to understand the CAS,\n- no need to bother with Captcha,\n- no complex logic to understand,\n- moreover, most of the authentication tokens stored in cookies have a pretty\n  long duration, so you will only have to manually log in from time to time.\n\n`CASPass` works also without a CAS: when the login process is full of\nJavascript, Captcha or other security checks and too complex to automate, just\nuse this module to authenticate and then perform the scraping with a more\nefficient tool.\n\n## Usage\n\nThe `CASPass` constructor expects two arguments:\n\n- a list of URL leading to the login page (you may need to provide multiple\n  links in order to satisfy the security checks)\n- the success URL, reached after successful login (it indicates the login\n  process is terminated)\n\n``` python\nfrom caspass import CASPass\n\ncas = CASPass([url, url_login], url_success)\ncas.login()\ncas.save("cookies.txt")\n```\n\nSee `examples/` for some complete examples.\n\n# Licence\n\nGPLv3+\n',
    'author': 'Olivier Schwander',
    'author_email': 'olivier.schwander@chadok.info',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
