import requests
from bs4 import BeautifulSoup
from models.elements import PageElements

def extract_elements(url: str) -> PageElements:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headings = [tag.get_text(strip=True) for tag in soup.find_all(['h1', 'h2', 'h3'])]
    buttons = [{'text': b.get_text(strip=True), 'action': b.get('onclick')} for b in soup.find_all('button')]
    links = [{'text': l.get_text(strip=True), 'href': l.get('href')} for l in soup.find_all('a')]
    inputs = [{'name': i.get('name'), 'type': i.get('type')} for i in soup.find_all('input')]
    forms = [f.get('action') for f in soup.find_all('form')]

    return PageElements(
        headings=headings,
        buttons=buttons,
        links=links,
        inputs=inputs,
        forms=forms
    )
