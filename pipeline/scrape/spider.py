import scrapy
from typing import Any, Dict, Iterable
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from scrapy import Field, Item

from settings import USER_AGENT

class HockeyResultsItem(Item):
    table = Field()

class HockeyResultsSpider(scrapy.Spider):
    name = "hockey-results-spider"

    def start_requests(self) -> Iterable[Request]:
        yield self.paginated_request()

    def parse(self, response: Response) -> Any:
        soup = BeautifulSoup(response.text, features="lxml")
        hockey_table = soup.find("table")

        if not hockey_table:
            raise ValueError("No table can be found")
        
        yield HockeyResultsItem(
            table=str(hockey_table)
        )
        yield self.paginated_request(response)

    def paginated_request(self, response: Response=None):
        if response is None:
            return Request(
                url="https://www.scrapethissite.com/pages/forms/?per_page=250",
                headers={"User-Agent": USER_AGENT},
                meta={
                    "page": 1
                }
            )
        next_page = int(response.meta["page"]) + 1

        if next_page < 10:
            return Request(
                url=f"https://www.scrapethissite.com/pages/forms/?per_page=250&page_num={next_page}",
                headers={"User-Agent": USER_AGENT},
                meta={
                    "page": next_page
                }
            )
