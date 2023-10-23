import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def html_to_markdown(url, start_dom_node_selector):
    response = requests.get(url)
    html_content = response.text
    
    
    soup = BeautifulSoup(html_content, 'html.parser')
    start_dom_node = soup.select_one(start_dom_node_selector)
    html_content = str(start_dom_node)
    markdown_content = md(html_content)
    return markdown_content
