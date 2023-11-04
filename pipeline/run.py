from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from common import HockeyTeamResults
from pipeline.consume.kafka_to_db import push_to_sqlite

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl("hockey-results-spider")
    process.start()
    
    HockeyTeamResults().create_table()
    push_to_sqlite()