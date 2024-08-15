import threading
from typing import Dict, List, Optional, Tuple

from officely.generator import ThreadedGenerator
from team_builder.graph import Edge, Graph
from team_builder.llms.tokenizer import Tokenizer, get_team_tokenizer_callback
import re

from team_builder.nodes.factory import factory_node
from team_builder.nodes.interface import IHistory, InputItem
import json

def run(
        team: Dict,
        verbose:bool,
        chat_history: List[IHistory],
        query: str,
        g: Optional[ThreadedGenerator] = None,
    ) -> str:
        try:
            team_res = None

            tokenizer = Tokenizer()
            with get_team_tokenizer_callback(tokenizer) as cb:
                team_res = run_team(chat_history, query, team, g, verbose, tokenizer)
                if verbose and g and cb.data:
                    g.send(f"\n\n<pre>{cb}</pre>")
        except Exception as e:  # This will catch other types of exceptions
            err_msg = str(e) if verbose else "there is error in agent, please try again."
            if bool(g):
                g.send(err_msg)
            else:
                return err_msg
            if not verbose:
               raise e

        finally:
            if bool(g):
                full_answer = re.sub(r'<(code|pre).*?>.*?</\1>', '', g.full_answer, flags=re.DOTALL).strip()
                if not full_answer and g.team and team_res:
                    g.send(str(team_res))
                g.close()
            
        return str(team_res)

            
def run_team(
            chat_history, 
            query, 
            team:Dict,
            g:Optional[ThreadedGenerator]=None, 
            verbose:bool=False,
            tokenizer:Optional[Tokenizer]=None
        )->str: 

        if g:
            g.team = True
        if not chat_history:
            return team["settings"]["startMessage"]

        nodes = [factory_node(node['data']['type'], **node['data'], ) for node in team['nodes'] if node['type'] == 'workflow']
        edges = [Edge(source=edge['source'], target=edge['target']) for edge in team['edges'] if edge['type'] == 'workflow']

        graph = Graph(nodes=nodes, edges=edges, g=g, verbose=verbose, tokenizer=tokenizer)
        res = graph.run(query, chat_history)
        return res


def arun(team:Dict, verbose:bool, chat_history:List, query: str):
    try:
        g = ThreadedGenerator()
        threading.Thread(target=run, args=(team, verbose, chat_history, query)).start()
        return g
    except Exception as e:
        raise e


def stream_response(team:Dict, verbose:bool, chat_history:List, query: str):
        try:
            ai_response = arun(team, verbose, chat_history, query)
            def generate():
                try:
                    for item in ai_response:  # Iterate over the ThreadedGenerator instance
                        yield json.dumps(item, ensure_ascii=False) + "\n"

                except Exception as e:
                    print(f"Stream Response: {e}")
                    replay = "there is error in agent, please try again."
                    yield json.dumps(replay, ensure_ascii=False) + "\n"
            return generate()

        except Exception as e:
            raise e