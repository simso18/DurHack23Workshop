from confluent_kafka import Consumer, KafkaError
import json
from bs4 import BeautifulSoup
from typing import List

from settings import KAFKA_CONFIGS, KAFKA_TOPIC
from common import HockeyTeamResults, HockeyTeamResultsDict

def ele_has_class(ele: element, cls: str) -> bool:
    if ele.attrs:
        classes = ele.attrs.get("class")
        if classes and cls in classes:
            return True
        return False 

def parse_table(soup: BeautifulSoup) -> List[HockeyTeamResultsDict]:
    headers = [" ".join(x.get_text(separator=' ').split()) for x in soup.find_all("th")]
    rows = []
    formatted_rows = []
    for body in soup.find_all("tbody"):
        for row in body.find_all("tr"):
            if ele_has_class(row, "total_row"):
                continue
            rows.append(x.text.strip() for x in row.find_all("td"))
    teams = [dict(zip(headers,row)) for row in rows]

    for team in teams:
        formatted_rows.append({
            "TeamName":team["Team Name"],
            "Year":team["Year"],
            "Wins":team["Wins"],
            "Losses":team["Losses"],
            "OTLosses":team["OT Losses"] if team["OT Losses"] != '' else None ,
            "WinPercent":team["Win %"],
            "GoalsFor":team["Goals For (GF)"],
            "GoalsAgainst":team["Goals Against (GA)"]
            }

        )

    return formatted_rows 

def push_to_sqlite():
    consumer = Consumer({
        "bootstrap.servers": KAFKA_CONFIGS["bootstrap.servers"],
        "group.id": "sqlite",
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([KAFKA_TOPIC])
    hockey_team_results = HockeyTeamResults()

    data = []
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            # No more messages
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        consumed_data = json.loads(msg.value().decode("utf-8"))
        hockey_table = BeautifulSoup(consumed_data["table"], "lxml") 
        formatted_rows: List[HockeyTeamResultsDict] = parse_table(hockey_table)
        hockey_team_results.insert_data(formatted_rows)

    consumer.close()