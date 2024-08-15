from typing import Dict, List, Tuple


from OfficelyTestTeam2.stream_handler import StreamHandler
from langchain_cohere import ChatCohere

from .llm import LLM



from typing import Dict, List, Tuple




class CohereLLM(LLM):
    streaming:bool = True

    @property
    def base(self):
        callbacks = []
        if self.tokenizer:
            self.tokenizer.model = self.model
            callbacks.append(self.tokenizer)
        is_answer = False
        if self.g:
            callbacks.append(StreamHandler(gen=self.g, with_final=False))
            is_answer = self.g.is_answer

        return ChatCohere(
            model=self.model, 
            temperature=self.temperature, 
            streaming=is_answer and self.streaming,
            callbacks=callbacks,

        )

    
    
    def with_schema(self, prompt:List[Tuple[str, str]], schema:Dict, name:str):
        self.streaming = False
        try:
            cohere_schema = {
                'title': schema['name'],
                'description': schema['description'],
                'properties': schema['parameters']['properties'],
            }
            return self.base.with_structured_output(cohere_schema).with_config({"run_name":name}).invoke(prompt)
        except Exception as e:
            print(e)
            raise e
        

    
   