import os
import argparse
import requests
import whois
import datetime


def get_cmdline_args():
    parser = argparse.ArgumentParser(
        description='Site availability checker'
    )
    parser.add_argument(
        'urls_file_path',
        help='path for file with urls'
    )
    return parser.parse_args()


def load_urls4check(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as url_file:
        return url_file.read().splitlines()


def is_server_respond_with_200(url):
    try:
        response = requests.get(url)
    except(requests.exceptions.RequestException):
        return False
    return response.status_code == 200


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    return domain_info.expiration_date


if __name__ == '__main__':
    args = get_cmdline_args()
    urls4check = load_urls4check(args.urls_file_path)
    if not urls4check:
        exit('incorrect file with urls')
        
    url_max_len = len(max(urls4check, key=len))
    print('{} STATUS EXPIRE'.format('URL'.ljust(url_max_len)))
    for checked_url in urls4check:
        domain_expdate = get_domain_expiration_date(checked_url)
        if domain_expdate is None:
            print('{} unregistered'.format(checked_url.ljust(url_max_len)))
            continue
        days_remaining = (domain_expdate - datetime.datetime.now()).days
        print('{} {} {}'.format(
            checked_url.ljust(url_max_len),
            'ok    ' if is_server_respond_with_200(checked_url) else 'error ',
            'yes' if days_remaining < 31 else 'no'
        ))
