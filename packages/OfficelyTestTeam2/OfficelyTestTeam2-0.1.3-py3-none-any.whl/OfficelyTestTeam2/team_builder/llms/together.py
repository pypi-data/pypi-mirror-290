from typing import Dict, List, Tuple

from langchain_together import ChatTogether

from OfficelyTestTeam2.stream_handler import StreamHandler
import requests
from .llm import LLM
import os




class TogtherLLM(LLM):
    togther_model:str


    streaming:bool = True

    @property
    def base(self):


        callbacks = []
        if self.tokenizer:
            self.tokenizer.model = self.togther_model #type:ignore
            callbacks.append(self.tokenizer)
        is_answer = False
        if self.g:
            callbacks.append(StreamHandler(gen=self.g, with_final=False))
            is_answer = self.g.is_answer

        return ChatTogether(
            model=self.togther_model, 
            temperature=self.temperature, 
            streaming=is_answer and self.streaming,
            callbacks=callbacks,
        )

    
    
    def with_schema(self, prompt:List[Tuple[str, str]], schema:Dict, name:str):
        pass
        # self.streaming = False
        # return self.base.with_structured_output(schema).with_config({"run_name":name}).invoke(prompt)

    @staticmethod
    def get_models_list():
        try:
            url = "https://api.together.xyz/v1/models"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {os.environ['TOGETHER_API_KEY']}"
            }

            response = requests.get(url, headers=headers).json()

            _list = [{"label":x['display_name'], "value":x['id']} for x in response if x['type'] == 'chat']
            sorted_list = sorted(_list, key=lambda x: x['label'])
            return sorted_list
        except Exception as e:
            raise e




    

