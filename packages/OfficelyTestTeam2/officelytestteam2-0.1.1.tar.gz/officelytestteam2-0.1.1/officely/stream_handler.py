from typing import Any, List
from dataclasses import dataclass, field
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from officely.generator import ThreadedGenerator

DEFAULT_ANSWER_PREFIX_TOKENS = ["Final", "Answer", ":"]


@dataclass
class StreamHandler(StreamingStdOutCallbackHandler):
    gen: ThreadedGenerator
    with_final: bool
    answer_reached: bool = field(default=False, init=False)
    answer_prefix_tokens: List[str] = field(default_factory=lambda: DEFAULT_ANSWER_PREFIX_TOKENS)
    last_tokens: List[str] = field(default_factory=list, init=False)
    last_tokens_stripped: List[str] = field(default_factory=list, init=False)


    def __post_init__(self):
        super().__init__()


    def on_new_token(self, token: str) -> None:
        if self.with_final:
            self.final_stream(token)
        else:
            self.gen.send(token)
            
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        if self.gen.team:
            if self.gen.is_answer:
                self.on_new_token(token)
        else:
            self.on_new_token(token)



    def append_to_last_tokens(self, token: str) -> None:
        self.last_tokens.append(token)
        self.last_tokens_stripped.append(token.strip())
        if len(self.last_tokens) > len(self.answer_prefix_tokens):
            self.last_tokens.pop(0)
            self.last_tokens_stripped.pop(0)

    def check_if_answer_reached(self) -> bool:
        return self.last_tokens_stripped == self.answer_prefix_tokens

    def final_stream(self, token:str):
        """Stream the final answer."""
        self.append_to_last_tokens(token)
        
        if not self.answer_reached:
            self.answer_reached = self.check_if_answer_reached()
            if self.answer_reached:
                return
            

        if self.answer_reached:
            self.gen.send(token)

    def on_chat_model_start(
        self,
        serialized,
        messages,
        **kwargs,
    ) -> None:
        """Run when LLM starts running."""
        self.answer_reached = False



    # def on_chat_model_start(
    #     self,
    #     serialized,
    #     messages,
    #     **kwargs,
    # ) -> None:
    #     """Run when LLM starts running."""
    #     self.model = kwargs["invocation_params"]["model"]
    #     self.gen.total_tokens_input += self.get_tokens_received(messages[0][0].content)