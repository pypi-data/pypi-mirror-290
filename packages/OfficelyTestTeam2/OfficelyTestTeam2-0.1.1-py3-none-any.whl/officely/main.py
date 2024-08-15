
import json
from typing import List
from officely.run import run

from team_builder.nodes.enums import MessageType
from team_builder.nodes.interface import IHistory

from OfficelyTestTeam1 import team



def get_team(path:str)->dict:
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    team = get_team("team.json")
    verbose = True
    chat_history:List[IHistory] = []

    while True:
        query = input("User: ")
        res = run(team, verbose, chat_history, query)
        chat_history.append(IHistory(text=query, type=MessageType.INBOUND))
        chat_history.append(IHistory(text=res, type=MessageType.OUTBOUND))
        print(f"AI:{res}")