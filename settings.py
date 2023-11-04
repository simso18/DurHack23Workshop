SQLITE_DATABASE = "HockeyTeams"
SQLITE_TABLE = "Results"

KAFKA_CONFIGS = {"bootstrap.servers": "localhost:9092"}
KAFKA_TOPIC = "hockey-team-results"

# for scrapy
USER_AGENT = "Python/3. Scrapy/2.11"
DOWNLOAD_DELAY = 1  # 1 second in between requests
ITEM_PIPELINES = {"src.scrape.kafka_pipeline": 0}