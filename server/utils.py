from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.request import urlopen
import re

# if it's server side rendered you don't need playwright to scrape you can directly use urllib
def plain_html_scrape():
    link = ""
    f = urlopen(link)
    content = f.read()
    return content

# if client side rendered, requires playwright to execute javascript to get content of the page
def js_scrape():
    with sync_playwright() as pw:
        # create browser instance
        browser = pw.chromium.launch(
            # Headless mode so it doesn't open a GUI
            headless=True,
        )
        # create context
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # go to url
        page.goto("")
        # get HTML
        return page.content()

def chunk_text(text):
    # divide text into chunk sizes
    CHUNK_SIZE = 100
    all_tokens = text.split()
    i = 0
    all_chunks = []

    while i < len(all_tokens):
        each_chunk = []
        if len(all_tokens) - i >= CHUNK_SIZE:
            each_chunk = all_tokens[i:i+CHUNK_SIZE]
        else:
            each_chunk = all_tokens[i:]
        all_chunks.append(" ".join(each_chunk))
        # add an overlap to retain semantic meaning
        i += CHUNK_SIZE - 25

    return all_chunks

# takes HTML of a webpage, converts into a list of chunks that can then me upserted into vector DB
def HTMLtoText(json_body):
    
    content = json_body["body"]
    
    soup = BeautifulSoup(content, 'html.parser')

    # Remove noisy tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    for tag in soup.find_all(["nav", "footer"]):
        tag.decompose()
    
    text = soup.get_text()
    # remove any long whitespaces with a singular whitespace
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    all_chunks = chunk_text(text)
    all_chunks.append(json_body["title"])
    all_chunks.append(json_body["notes"])

    return all_chunks

content = ""
all = chunk_text(content)