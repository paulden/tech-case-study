import json


def json_presenter(extracted_links):
    """
    Print URLs as a JSON with relative links.
    """
    relative_links = {}
    for url, links in extracted_links.items():
        relative_links[url] = [link.replace(url, '') for link in links]
    print(json.dumps(relative_links))


def stdout_presenter(extracted_links):
    """
    Print URL as a list with full links.
    """
    for links in extracted_links.values():
        [print(link) for link in links]
