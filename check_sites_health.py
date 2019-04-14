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


def get_domains_info(urls4check):
    return [
        {
            'url': checked_url,
            'status': is_server_respond_with_ok(checked_url),
            'expdate': get_domain_expiration_date(checked_url)
        }
        for checked_url in urls4check]


def print_domains_info(domains_info, limit):
    url_max_len = len(max([d['url'] for d in domains_info], key=len))
    print('{} STATUS EXPIRE'.format('URL'.ljust(url_max_len)))
    for domain_info in domains_info:
        if domain_info['expdate'] is None:
            days_remaining_message = 'unknown'
        else:
            days_remaining = (domain_info['expdate'] - datetime.datetime.now()).days
            days_remaining_message = 'yes' if days_remaining <= limit else 'no'
        print('{} {} {}'.format(
            domain_info['url'].ljust(url_max_len),
            'ok    ' if domain_info['status'] else 'error ',
            days_remaining_message
        ))


if __name__ == '__main__':
    args = get_cmdline_args()
    urls4check = load_urls4check(args.urls_file_path)
    if not urls4check:
        exit('incorrect file with urls')
    domains_info = get_domains_info(urls4check)
    print_domains_info(domains_info, args.limit)
