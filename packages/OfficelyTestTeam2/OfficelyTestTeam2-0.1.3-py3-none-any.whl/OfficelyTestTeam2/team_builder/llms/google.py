
from OfficelyTestTeam2.stream_handler import StreamHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from .llm import LLM
from langchain_core.language_models.chat_models import generate_from_stream
from typing import List, Optional, Sequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai._function_utils import _ToolConfigDict

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from urllib.parse import urlparse

from google.generativeai.types import Tool as GoogleTool  # type: ignore[import]
from google.generativeai.types.content_types import (  # type: ignore[import]
    FunctionDeclarationType,
    ToolDict,
)
from langchain_core.callbacks.manager import (CallbackManagerForLLMRun,)

from langchain_core.messages import (BaseMessage,)


from langchain_core.outputs import ChatResult

from langchain_google_genai._common import (SafetySettingDict,)
from langchain_google_genai._function_utils import ( _ToolConfigDict)




class GoogleGenAI(ChatGoogleGenerativeAI):
    """Create a custom class for GoogleGenAI that can handle streaming."""

    streaming:bool


    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        *,
        tools: Optional[Sequence[Union[ToolDict, GoogleTool]]] = None,
        functions: Optional[Sequence[FunctionDeclarationType]] = None,
        safety_settings: Optional[SafetySettingDict] = None,
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            stream_iter = self._stream(
                    messages, stop=stop, run_manager=run_manager, **kwargs
                )
            return generate_from_stream(stream_iter)
        else:
            return super()._generate(messages, stop=stop, run_manager=run_manager, 
                              tools=tools, 
                              functions=functions,
                               safety_settings=safety_settings,
                               tool_config=tool_config,
                                generation_config=generation_config,
                                **kwargs
                            )


class GoogleLLM(LLM):

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

        return GoogleGenAI( 
            model=self.model, 
            temperature=self.temperature, 
            callbacks=callbacks,
            streaming=is_answer,
            #type: ignore
        ) 

    
    
    def with_schema(self, prompt:List[Tuple[str, str]], schema:Dict, name:str):
        pass

    
   

