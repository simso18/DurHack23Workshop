import scrapy
from typing import Any, Dict, Iterable
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from .utils import parse_html
from .items import ExampleItem

class ExampleSpider(scrapy.Spider):
    name = "example-spider"

    def start_requests(self) -> Iterable[Request]:
        yield paginated_request()

    @parse_html
    def parse(self, response: Response, data: Dict) -> Any:
        yield ExampleItem(data=data)
        yield paginated_request(response)



def paginated_request(response: Response=None):
    if response is None:
        return Request(
            url="https://www.scrapethissite.com/pages/forms/",
            meta={
                "page": 1
            }
        )
    next_page = int(response.meta["page"]) + 1
    return Request(
        url=f"https://www.scrapethissite.com/pages/forms/?page_num={next_page}",
        meta={
            "page": next_page
        }
    )
