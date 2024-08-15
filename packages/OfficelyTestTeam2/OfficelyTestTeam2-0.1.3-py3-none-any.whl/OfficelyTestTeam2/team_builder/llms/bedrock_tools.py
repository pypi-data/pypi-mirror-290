import json
from operator import itemgetter
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Type,
    Union,
    cast,
    Callable
)

from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models import LanguageModelInput

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    BaseMessageChunk,
    SystemMessage,
)

from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from langchain_community.chat_models.bedrock import BedrockChat, ChatPromptAdapter
from typing import Tuple
import defusedxml.ElementTree as DET

from langchain_anthropic.chat_models import convert_to_anthropic_tool, _format_messages

from langchain_core.runnables import (
    Runnable,
    RunnableMap,
    RunnablePassthrough,
)

from typing import Any, List, Optional, Type, TypedDict, cast

from typing import Any, List, Optional, Type, TypedDict, cast

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import BaseGenerationOutputParser
from langchain_core.outputs import ChatGeneration, Generation
from langchain_core.pydantic_v1 import BaseModel


class _ToolCall(TypedDict):
    name: str
    args: dict
    id: str
    index: int


class ToolsOutputParser(BaseGenerationOutputParser):
    first_tool_only: bool = False
    args_only: bool = False
    pydantic_schemas: Optional[List[Type[BaseModel]]] = None

    class Config:
        extra = "forbid"

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        """Parse a list of candidate model Generations into a specific format.

        Args:
            result: A list of Generations to be parsed. The Generations are assumed
                to be different candidate outputs for a single model input.

        Returns:
            Structured output.
        """
        if not result or not isinstance(result[0], ChatGeneration):
            return None if self.first_tool_only else []
        tool_calls: List = _extract_tool_calls(result[0].message)
        if self.pydantic_schemas:
            tool_calls = [self._pydantic_parse(tc) for tc in tool_calls]
        elif self.args_only:
            tool_calls = [tc["args"] for tc in tool_calls]
        else:
            pass

        if self.first_tool_only:
            return tool_calls[0] if tool_calls else None
        else:
            return tool_calls

    def _pydantic_parse(self, tool_call: _ToolCall) -> BaseModel:
        cls_ = {schema.__name__: schema for schema in self.pydantic_schemas or []}[
            tool_call["name"]
        ]
        return cls_(**tool_call["args"])


def _extract_tool_calls(msg: BaseMessage) -> List[_ToolCall]:
    if isinstance(msg.content, str):
        return []
    tool_calls = []
    for i, block in enumerate(cast(List[dict], msg.content)):
        if block["type"] != "tool_use":
            continue
        tool_calls.append(
            _ToolCall(name=block["name"], args=block["input"], id=block["id"], index=i)
        )
    return tool_calls



SYSTEM_PROMPT_FORMAT = """In this environment you have access to a set of tools you can use to answer the user's question.

You may call them like this:
<function_calls>
<invoke>
<tool_name>$TOOL_NAME</tool_name>
<parameters>
<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>
...
</parameters>
</invoke>
</function_calls>

Here are the tools available:
<tools>
{formatted_tools}
</tools>"""  # noqa: E501

TOOL_FORMAT = """<tool_description>
<tool_name>{tool_name}</tool_name>
<description>{tool_description}</description>
<parameters>
{formatted_parameters}
</parameters>
</tool_description>"""

TOOL_PARAMETER_FORMAT = """<parameter>
<name>{parameter_name}</name>
<type>{parameter_type}</type>
<description>{parameter_description}</description>
</parameter>"""


def _get_type(parameter: Dict[str, Any]) -> str:
    if "type" in parameter:
        return parameter["type"]
    if "anyOf" in parameter:
        return json.dumps({"anyOf": parameter["anyOf"]})
    if "allOf" in parameter:
        return json.dumps({"allOf": parameter["allOf"]})
    return json.dumps(parameter)


def get_system_message(tools: List[Dict]) -> str:
    tools_data: List[Dict] = [
        {
            "tool_name": tool["name"],
            "tool_description": tool["description"],
            "formatted_parameters": "\n".join(
                [
                    TOOL_PARAMETER_FORMAT.format(
                        parameter_name=name,
                        parameter_type=_get_type(parameter),
                        parameter_description=parameter.get("description"),
                    )
                    for name, parameter in tool["parameters"]["properties"].items()
                ]
            ),
        }
        for tool in tools
    ]
    tools_formatted = "\n".join(
        [
            TOOL_FORMAT.format(
                tool_name=tool["tool_name"],
                tool_description=tool["tool_description"],
                formatted_parameters=tool["formatted_parameters"],
            )
            for tool in tools_data
        ]
    )
    return SYSTEM_PROMPT_FORMAT.format(formatted_tools=tools_formatted)


def _xml_to_dict(t: Any) -> Union[str, Dict[str, Any]]:
    # Base case: If the element has no children, return its text or an empty string.
    if len(t) == 0:
        return t.text or ""

    # Recursive case: The element has children. Convert them into a dictionary.
    d: Dict[str, Any] = {}
    for child in t:
        if child.tag not in d:
            d[child.tag] = _xml_to_dict(child)
        else:
            # Handle multiple children with the same tag
            if not isinstance(d[child.tag], list):
                d[child.tag] = [d[child.tag]]  # Convert existing entry into a list
            d[child.tag].append(_xml_to_dict(child))
    return d


def _xml_to_function_call(invoke: Any, tools: List[Dict]) -> Dict[str, Any]:
    name = invoke.find("tool_name").text
    arguments = _xml_to_dict(invoke.find("parameters"))

    # make list elements in arguments actually lists
    filtered_tools = [tool for tool in tools if tool["name"] == name]
    if len(filtered_tools) > 0 and not isinstance(arguments, str):
        tool = filtered_tools[0]
        for key, value in arguments.items():
            if key in tool["parameters"]["properties"]:
                if "type" in tool["parameters"]["properties"][key]:
                    if tool["parameters"]["properties"][key][
                        "type"
                    ] == "array" and not isinstance(value, list):
                        arguments[key] = [value]
                    if (
                        tool["parameters"]["properties"][key]["type"] != "object"
                        and isinstance(value, dict)
                        and len(value.keys()) == 1
                    ):
                        arguments[key] = list(value.values())[0]

    return {
        "function": {
            "name": name,
            "arguments": json.dumps(arguments),
        },
        "type": "function",
    }


def _xml_to_tool_calls(elem: Any, tools: List[Dict]) -> List[Dict[str, Any]]:
    """
    Convert an XML element and its children into a dictionary of dictionaries.
    """
    invokes = elem.findall("invoke")

    return [_xml_to_function_call(invoke, tools) for invoke in invokes]


class BedrockTools(BedrockChat):

    _xmllib: Any = Field(default=DET)


    def bind_tools(
        self,
        tools: Sequence[Union[Dict[str, Any], Type[BaseModel], Callable, BaseTool]],
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        """Bind tool-like objects to this chat model.

        Args:
            tools: A list of tool definitions to bind to this chat model.
                Can be  a dictionary, pydantic model, callable, or BaseTool. Pydantic
                models, callables, and BaseTools will be automatically converted to
                their schema dictionary representation.
            **kwargs: Any additional parameters to bind.
        """
        formatted_tools = [convert_to_anthropic_tool(tool) for tool in tools]
        return self.bind(tools=formatted_tools, **kwargs)

    def with_structured_output(
        self,
        schema: Union[Dict, Type[BaseModel]],
        *,
        include_raw: bool = False,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, Union[Dict, BaseModel]]:
        llm = self.bind_tools([schema])
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            output_parser = ToolsOutputParser(
                first_tool_only=True, pydantic_schemas=[schema]
            )
        else:
            output_parser = ToolsOutputParser(first_tool_only=True, args_only=True)

        if include_raw:
            parser_assign = RunnablePassthrough.assign(
                parsed=itemgetter("raw") | output_parser, parsing_error=lambda _: None
            )
            parser_none = RunnablePassthrough.assign(parsed=lambda _: None)
            parser_with_fallback = parser_assign.with_fallbacks(
                [parser_none], exception_key="parsing_error"
            )
            return RunnableMap(raw=llm) | parser_with_fallback
        else:
            return llm | output_parser

    def _format_params(
        self,
        *,
        messages: List[BaseMessage],
        **kwargs: Any,
    ) -> Tuple[Optional[str], Union[List[Dict], str]]:
        tools: List[Dict] = kwargs.get("tools", None)
        # experimental tools are sent in as part of system prompt, so if
        # both are set, turn system prompt into tools + system prompt (tools first)
        if tools:
            tool_system = get_system_message(tools)

            if messages[0].type == "system":
                sys_content = messages[0].content
                new_sys_content = f"{tool_system}\n\n{sys_content}"
                messages = [SystemMessage(content=new_sys_content), *messages[1:]]
            else:
                messages = [SystemMessage(content=tool_system), *messages]

        provider = self._get_provider()
        if provider == 'anthropic':
            return ChatPromptAdapter.format_messages(provider, messages)
        return None, ChatPromptAdapter.convert_messages_to_prompt(provider, messages)

        #return super()._format_params(messages=messages, stop=stop, **kwargs)

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        # streaming not supported for functions
        result = self._generate(
            messages=messages, stop=stop, run_manager=run_manager, **kwargs
        )
        to_yield = result.generations[0]
        chunk = ChatGenerationChunk(
            message=cast(BaseMessageChunk, to_yield.message),
            generation_info=to_yield.generation_info,
        )
        if run_manager:
            run_manager.on_llm_new_token(
                cast(str, to_yield.message.content), chunk=chunk
            )
        yield chunk

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        # streaming not supported for functions
        result = await self._agenerate(
            messages=messages, stop=stop, run_manager=run_manager, **kwargs
        )
        to_yield = result.generations[0]
        chunk = ChatGenerationChunk(
            message=cast(BaseMessageChunk, to_yield.message),
            generation_info=to_yield.generation_info,
        )
        if run_manager:
            await run_manager.on_llm_new_token(
                cast(str, to_yield.message.content), chunk=chunk
            )
        yield chunk

    # def _format_output(self, text: Any, **kwargs: Any) -> ChatResult:
    #     """Format the output of the model, parsing xml as a tool call."""
    #     #text = data.content[0].text
    #     tools = kwargs.get("tools", None)

    #     additional_kwargs: Dict[str, Any] = {}

    #     if tools:
    #         # parse out the xml from the text
    #         try:
    #             # get everything between <function_calls> and </function_calls>
    #             start = text.find("<function_calls>")
    #             end = text.find("</function_calls>") + len("</function_calls>")
    #             xml_text = text[start:end]

    #             xml = DET.fromstring(xml_text)
    #             additional_kwargs["tool_calls"] = _xml_to_tool_calls(xml, tools)
    #             text = ""
    #         except Exception:
    #             pass

    #     return ChatResult(
    #         generations=[
    #             ChatGeneration(
    #                 message=AIMessage(content=text, additional_kwargs=additional_kwargs)
    #             )
    #         ],
    #         #llm_output=data,
    #     )

    def _format_output(self, text: Any, additional_kwargs: Any) -> ChatResult:
        #data_dict = data.model_dump()
        # content = data_dict["content"]
        # llm_output = {
        #     k: v for k, v in data_dict.items() if k not in ("content", "role", "type")
        # }
        # if len(content) == 1 and content[0]["type"] == "text":
        #     msg = AIMessage(content=content[0]["text"])
        # else:
        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(content=text, additional_kwargs=additional_kwargs)
                )
            ],
            #llm_output=data,
        )
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        completion = ""

        if self.streaming:
            for chunk in self._stream(messages, stop, run_manager, **kwargs):
                completion += chunk.text
        else:
            system = None
            formatted_messages:Optional[List[Dict]] = None
            prompt:Optional[str]= None
            params: Dict[str, Any] = {**kwargs}
            system, formatted_messages = _format_messages(messages)
            # if not system:
            #     prompt = str(messages_prompt)
            # else:
            #     assert isinstance(messages_prompt, list), "messages_prompt must be a list of BaseMessage"
            #     formatted_messages = messages_prompt
            
            if stop:
                params["stop_sequences"] = stop

            completion = self._prepare_input_and_invoke(
                prompt=None,
                stop=stop,
                run_manager=run_manager,
                system=system,
                messages=formatted_messages,
                **params,
            )

        
        return self._format_output(completion[0], params)


def _tools_in_params(params: dict) -> bool:
    return "tools" in params or (
        "extra_body" in params and params["extra_body"].get("tools")
    )

