from scrapy.http import Request, Response
import functools
from bs4 import BeautifulSoup

def parse_html(f):
    @functools.wraps(f)
    def parse(self, response: Response):
        soup = BeautifulSoup(response.text, features="lxml")
        return f(self, response, soup)

    return parse