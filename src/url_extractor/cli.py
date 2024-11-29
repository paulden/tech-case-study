#!/usr/bin/env python

import click

from extract_links import extract_links
from presenters import stdout_presenter, json_presenter


@click.command()
@click.option('-u', '--url', "urls", required=True, multiple=True, type=str,
              help='URL where links should be extracted (multiple selection is allowed)')
@click.option('-o', '--output', required=True, type=click.Choice(['stdout', 'json']),
              help='Expected output type')
def main(urls, output):
    """
    CLI built using click using official documentation: https://click.palletsprojects.com/en/stable/
    """
    extracted_links = {}
    for url in urls:
        extracted_links[url] = extract_links(url)
    if output == 'stdout':
        stdout_presenter(extracted_links)
    elif output == 'json':
        json_presenter(extracted_links)


if __name__ == '__main__':
    main()
