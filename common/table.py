import sqlite3
from cachetools.func import ttl_cache
from itertools import chain
from enum import Enum
from typing import TypedDict, Optional, List

from settings import SQLITE_DATABASE, SQLITE_TABLE

SQLITE_MAX_ARGS = 999

class HockeyTeamResultsDict(TypedDict):
    TeamName: str
    Year: int
    Wins: int
    Losses: int
    OTLosses: Optional[int]
    WinPercent: float
    GoalsFor: int
    GoalsAgainst: int

class HockeyTeamResults:
    def create_table(self):
        conn = sqlite3.connect(f"/db/{SQLITE_DATABASE}.db")
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {SQLITE_TABLE} (
                TeamName TEXT NOT NULL,
                Year INT NOT NULL,
                Wins INT NOT NULL,
                Losses INT NOT NULL,
                OTLosses INT NULL,
                WinPct INT NOT NULL,
                GoalsFor INT NOT NULL,
                GoalsAgainst INT NOT NULL,

                PRIMARY KEY(TeamName, Year)
            )
        """).fetchall()
        conn.close()

    def insert_data(self, data: List[HockeyTeamResultsDict]) -> None:
        args_per_item = len(data[0])
        item_values_str = "(" + ", ".join(["?" for _ in range(args_per_item)]) + ")"
        batch_size = SQLITE_MAX_ARGS // args_per_item

        conn = sqlite3.connect(f"/db/{SQLITE_DATABASE}.db")
        conn.execute("BEGIN TRANSACTION")
        for i in range(0, len(data), batch_size):
            data_to_insert = data[i:i+batch_size]
            batch_values_str = ", ".join([item_values_str for _ in range(len(data_to_insert))])
            conn.execute(f"""
                INSERT INTO {SQLITE_TABLE} (
                    TeamName,
                    Year,
                    Wins,
                    Losses,
                    OTLosses,
                    WinPct,
                    GoalsFor,
                    GoalsAgainst
                ) VALUES {batch_values_str}
            """,
            *list(chain(*[
                (
                    item["TeamName"],
                    item["Year"],
                    item["Wins"],
                    item["Losses"],
                    item["OTLosses"],
                    item["WinPercent"],
                    item["GoalsFor"],
                    item["GoalsAgainst"],
                )
                for item in data_to_insert
            ]))).fetchall()
        conn.commit()
        conn.close()


    @ttl_cache(maxsize=1, ttl=5)
    def get_data(self) -> List[HockeyTeamResultsDict]:
        conn = sqlite3.connect(f"/db/{SQLITE_DATABASE}.db")
        data = conn.execute(f"""
            SELECT
                TeamName,
                Year,
                Wins,
                Losses,
                OTLosses,
                WinPct,
                GoalsFor,
                GoalsAgainst
            FROM {SQLITE_TABLE}
        """).fetchall()
        conn.close()
        return [
            {
                "TeamName": item[0],
                "Year": item[1],
                "Wins": item[2],
                "Losses": item[3],
                "OTLosses": item[4],
                "WinPct": item[5],
                "GoalsFor": item[6],
                "GoalsAgainst": item[7],
            }
            for item in data
        ]