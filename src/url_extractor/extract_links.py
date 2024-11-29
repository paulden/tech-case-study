import requests
from bs4 import BeautifulSoup


def extract_links(url: str) -> list[str]:
    """
    Retrieve the list of links found in the HTML code from a URL,
    filtering out links from other websites.
    We do not de-duplicate links since we consider it useful information to know the link is mentioned
    multiple times, but in Python that could be easily changed using a `list(set(extracted_links))`
    """
    all_links = get_all_links_from_html(url)
    extracted_links = []
    for link in all_links:
        if is_relative(link):
            extracted_links.append(get_full_link(link, url))
        elif is_own_domain(link, url):
            extracted_links.append(link)
    return extracted_links


def get_all_links_from_html(url: str) -> list[str]:
    """
    Fetch HTML from a URL and return all links found in it, assuming
    all links are found <a> tags under the href field.
    Source: https://beautiful-soup-4.readthedocs.io/en/latest/
    """
    response = requests.get(url)
    if response.status_code > 299:
        raise ConnectionError(f"Call to URL {url} returned a status code > 299")
    html = BeautifulSoup(response.text, 'html.parser')
    return [link.get('href') for link in html.find_all('a') if isinstance(link.get('href'), str)]


def get_full_link(link: str, url: str) -> str:
    """
    Form the full link from the base URL and the relative link.
    Depending on the href, we need to add the / or keep the existent one.
    """
    return f"{url}{link}" if link.startswith('/') else f"{url}/{link}"


def is_relative(link: str) -> bool:
    """
    A link is considered relative if it does not start with http and if it
    does not contain an @ (for instance when we have a mailto:contact@example.com).
    """
    return not link.startswith('http') and not '@' in link


def is_own_domain(link: str, url: str) -> bool:
    """
    If the href is a full URL and contains the base URL, it is considered valid.
    """
    return url in link
