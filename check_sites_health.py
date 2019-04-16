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
    parser.add_argument(
        '--limit',
        type=int,
        default=31,
        help='checking period in days'
    )
    return parser.parse_args()


def load_urls4check(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as url_file:
        return url_file.read().splitlines()


def is_server_respond_with_ok(url):
    try:
        response = requests.get(url)
    except(requests.exceptions.RequestException):
        return False
    return response.ok


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    return domain_info.expiration_date


def get_domains_info(urls4check, limit):
    return [
        {
            'url': checked_url,
            'status': is_server_respond_with_ok(checked_url),
            'expired': is_domain_expired(
                get_domain_expiration_date(checked_url),
                limit
            )
        }
        for checked_url in urls4check]


def is_domain_expired(expdate, limit):
    if isinstance(expdate, list):
        try:
            expdate = min(expdate)
        except TypeError:
            return None
    if isinstance(expdate, datetime.datetime):
        days_remaining = (expdate - datetime.datetime.now()).days
        if days_remaining is not None:
            return days_remaining <= limit


def print_domains_info(domains_info):
    url_max_len = len(max(
        [domain_info['url'] for domain_info in domains_info],
        key=len
    ))
    print('{} STATUS EXPIRE'.format('URL'.ljust(url_max_len)))
    for domain_info in domains_info:
        print('{} {} {}'.format(
            domain_info['url'].ljust(url_max_len),
            'ok    ' if domain_info['status'] else 'error ',
            'unknown' if domain_info['expired'] is None else 'yes' if domain_info['expired'] else 'no'
        ))


if __name__ == '__main__':
    args = get_cmdline_args()
    urls4check = load_urls4check(args.urls_file_path)
    if not urls4check:
        exit('incorrect file with urls')
    domains_info = get_domains_info(urls4check, args.limit)
    print_domains_info(domains_info)
