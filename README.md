# Sites Monitoring Utility

Site availability and domain expirity checker.

Script gets list of urls from file and outputs status of each url:

* *unknown* if site not registered
* *ok* if site returns '200 OK' status 
* *error* if site returns any another status

Also script checks 'Expiration Date' and print yes if domain expires during 1 month, , otherwise it prints "no".

# How to Install

Python 3 should be already installed. 

Script use [requests](https://pypi.org/project/requests/2.21.0/) and [python-whois](https://pypi.org/project/python-whois/0.7.1/). Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# Quickstart

Example of script launch on Linux, Python 3.5:

```bash

$ python check_sites_health.py urls.txt
URL                         STATUS EXPIRE
http://newrobinson111.ru    unknown
htt://lihe.ru               error  no
http://bitcoinme.ru         ok     no
http://bookday.ru           ok     yes
...[skipped]...

```

Use in Windows similarly.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
