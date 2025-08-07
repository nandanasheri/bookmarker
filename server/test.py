from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.request import urlopen

# if it's server side rendered you don't need playwright to scrape you can directly use urllib
def plain_html_scrape():
    link = "https://github.com/nandanasheri"
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
        page.goto("https://github.com/nandanasheri")
        # get HTML
        return page.content()

def chunk_text(content):
    soup = BeautifulSoup(content, 'html.parser')
     # Remove noisy tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    for tag in soup.find_all(["nav", "footer"]):
        tag.decompose()
    
    print(soup.get_text())
    
text = js_scrape()
chunk_text(text)