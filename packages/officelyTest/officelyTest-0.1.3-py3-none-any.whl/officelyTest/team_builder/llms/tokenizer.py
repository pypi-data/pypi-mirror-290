from langchain_cohere import ChatCohere
from pydantic.v1 import BaseModel, Field
from typing import Any, Dict , Generator, List, Optional, Tuple, Union
from tiktoken import encoding_for_model
from contextlib import contextmanager
from contextvars import ContextVar
from langchain_core.tracers.context import register_configure_hook
from langchain_community.utilities.anthropic import get_num_tokens_anthropic
from langchain.schema import LLMResult
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.callbacks.openai_info import get_openai_token_cost_for_model
from langchain_core.language_models.base import _get_token_ids_default_method
from team_builder.llms.enums import LLMType
from langchain_google_genai import ChatGoogleGenerativeAI



MODEL_COST_PER_1K_INPUT_TOKENS = {
    LLMType.MISTRAL_7B:0.00015,
    LLMType.MISTRAL_8X7B:0.00045,
    LLMType.MISTRAL_LARGE:0.008,
    LLMType.MISTRAL_SMALL:0.001,
    LLMType.LLAMA3_8B:0.0004,
    LLMType.LLAMA3_70B:0.00265,
    LLMType.COMMAND_R_PLUS:0.0030,
    LLMType.COMMAND_R:0.0005,
    LLMType.COMMAND:0.0015,
    LLMType.COMMAND_LIGHT:0.0003,
    LLMType.GEMINI_1_5_PRO: 0.0035
}

MODEL_COST_PER_1K_OUTPUT_TOKENS = {
    LLMType.MISTRAL_7B:0.0002,
    LLMType.MISTRAL_8X7B:0.0007,
    LLMType.MISTRAL_LARGE:0.024,
    LLMType.MISTRAL_SMALL:0.003,
    LLMType.LLAMA3_8B:0.0006,
    LLMType.LLAMA3_70B:0.0035,
    LLMType.COMMAND_R_PLUS:0.0150,
    LLMType.COMMAND_R:0.0015,
    LLMType.COMMAND:0.0020,
    LLMType.COMMAND_LIGHT:0.0006,
    LLMType.GEMINI_1_5_PRO: 0.0105
}


ANTH_MODEL_COST_PER_1K_INPUT_TOKENS = {
    "anthropic.claude-instant-v1": 0.0008,
    "anthropic.claude-v2": 0.008,
    "anthropic.claude-v2:1": 0.008,
    "anthropic.claude-3-sonnet-20240229-v1:0": 0.003,
    "anthropic.claude-3-haiku-20240307-v1:0": 0.00025,
    "anthropic.claude-3-5-sonnet-20240620-v1:0": 0.003,
}

ANTH_MODEL_COST_PER_1K_OUTPUT_TOKENS = {
    "anthropic.claude-instant-v1": 0.0024,
    "anthropic.claude-v2": 0.024,
    "anthropic.claude-v2:1": 0.024,
    "anthropic.claude-3-sonnet-20240229-v1:0": 0.015,
    "anthropic.claude-3-haiku-20240307-v1:0": 0.00125,
    "anthropic.claude-3-5-sonnet-20240620-v1:0": 0.015,
}


def _get_anthropic_claude_token_cost(
    prompt_tokens: int, completion_tokens: int, model_id: Union[str, None]
) -> float:
    """Get the cost of tokens for the Claude model."""
    if model_id not in ANTH_MODEL_COST_PER_1K_INPUT_TOKENS:
        raise ValueError(
            f"Unknown model: {model_id}. Please provide a valid Anthropic model name."
            "Known models are: " + ", ".join(ANTH_MODEL_COST_PER_1K_INPUT_TOKENS.keys())
        )
    return (prompt_tokens / 1000) * ANTH_MODEL_COST_PER_1K_INPUT_TOKENS[model_id] + (
        completion_tokens / 1000
    ) * ANTH_MODEL_COST_PER_1K_OUTPUT_TOKENS[model_id]


def _token_cost(
    prompt_tokens: int, completion_tokens: int, model_id: LLMType
) -> float:
    """Get the cost of tokens for the Claude model."""
    if model_id not in MODEL_COST_PER_1K_INPUT_TOKENS:
        # raise ValueError(
        #     f"Unknown model: {model_id}. Please provide a valid model name."
        #     "Known models are: " + ", ".join(MODEL_COST_PER_1K_INPUT_TOKENS.keys())
        # )
        return 0
    return (prompt_tokens / 1000) * MODEL_COST_PER_1K_INPUT_TOKENS[model_id] + (
        completion_tokens / 1000
    ) * MODEL_COST_PER_1K_OUTPUT_TOKENS[model_id]





class ITokenizer(BaseModel):
    successful_requests:int = 0
    total_tokens_input:int = 0
    total_tokens_output:int = 0
    total_cost:float = 0.0  

class ITokensData(BaseModel):
    model:LLMType
    outputs:int
    inputs:int


class Tokenizer(BaseModel,BaseCallbackHandler):
    model:Optional[LLMType] = None
    data:Dict[LLMType, ITokenizer] = {}
    last_token_input:int = Field(default=0, init_var=False)



    @property
    def Tokens_data(self) -> List[ITokensData]:
        tokens_data = []
        for model_key, tokenizer in self.data.items():
            prompts_tokens = tokenizer.total_tokens_input
            completion_tokens = tokenizer.total_tokens_output
            tokens_data.append(ITokensData(model=model_key, outputs=completion_tokens, inputs=prompts_tokens))
        return tokens_data
    
    def __str__(self) -> str:
        result = []
        for model_key, tokenizer in self.data.items():
            if model_key == LLMType.AZURE:
                continue
            prompts_tokens = tokenizer.total_tokens_input
            completion_tokens = tokenizer.total_tokens_output
            total_cost = self.calculate_cost(model_key, prompts_tokens, completion_tokens) #type: ignore
            self.data[model_key].total_cost = total_cost
            result.append(
                f"Model: {model_key.name if isinstance(model_key, LLMType) else model_key}\n"
                f"  Successful requests: {tokenizer.successful_requests}\n"
                f"  Total tokens input: {prompts_tokens}\n"
                f"  Total tokens output: {completion_tokens}\n"
                f"  Total cost: ${total_cost}\n"
            )
        result.append(f"Officely AI Fee: $0.01")
        result.append(f"Total Cost: ${0.01 + sum([tokenizer.total_cost for tokenizer in self.data.values()])}")
        return "\n".join(result)
    

    def start(self, content:str):
        if self.model is None:
            return
        if self.model not in self.data.keys():
            self.data[self.model] = ITokenizer()
        self.last_token_input = self.get_tokens_received(content=content)
        self.data[self.model].total_tokens_input += self.last_token_input

    def on_llm_start(self, serialized: Dict[str, Any],prompts: List[str], **kwarg):
        self.start(" ".join(prompts))
    
    def on_chat_model_start(self, serialized, messages, **kwargs):
        """Run when a chat model starts running."""
        def content(content:list | str):
            if isinstance(content, str):
                return content
            string = ""
            for x in content:
                if isinstance(x, str):
                    string += x
                if isinstance(x, dict) and x['type'] == "text": 
                    string += x['text']
            return string

        content_str = " ".join([content(x.content) for x in messages[0]])
        self.start(content_str)

    
    def get_tokens_received(self, content:Optional[str]=None, response:Any=None):
        """Get the number of tokens received in a message."""
        if response:
            message = response.generations[0][0].text
        else: 
            message = content
        num = 0
        if self.model.startswith("gpt"): #type: ignore
            if response and response.llm_output and "token_usage" in response.llm_output:
                token_usage = response.llm_output["token_usage"]
                num, _ = self.token_usage(token_usage)
            else:
                tiktoken = encoding_for_model(self.model) #type: ignore
                num = len(tiktoken.encode(message)) #type: ignore
        elif self.model.startswith("anthropic"): #type: ignore
            if response and response.llm_output and "usage" in response.llm_output:
                token_usage = response.llm_output["usage"]
                num, _ = self.token_usage(token_usage)
            else:
                num = get_num_tokens_anthropic(message)#type: ignore
        elif self.model.startswith("command"): #type: ignore
            num = ChatCohere(model=self.model).get_num_tokens(message) #type: ignore
        elif self.model.startswith("gemini"):    #type: ignore
            num = ChatGoogleGenerativeAI(model=self.model).get_num_tokens(message) #type: ignore
        else:
            num = len(_get_token_ids_default_method(message)) #type: ignore
        return num    
    
    def calculate_cost(self, model:LLMType, prompt_token:int, completion_tokens:bool):
        """Calculate the cost of tokens for a model."""
        cost = 0
        if model.startswith("gpt"):
            cost = get_openai_token_cost_for_model(model.value, prompt_token, False) + get_openai_token_cost_for_model(model.value, completion_tokens, True)
        elif model.startswith("anthropic"):
            cost =  _get_anthropic_claude_token_cost(prompt_token, completion_tokens, model.value)
        else:
            cost = _token_cost(prompt_token, completion_tokens, model)  
        return cost

    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.data[self.model].successful_requests += 1 #type: ignore
        self.data[self.model].total_tokens_output += self.get_tokens_received(response=response) #type: ignore


    def token_usage(self, token_usage:Dict[str, int]) -> Tuple[int, int]:
        completion_tokens = token_usage.get("completion_tokens", 0)
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        if prompt_tokens:
            self.data[self.model].total_tokens_input -= self.last_token_input #type: ignore
            self.data[self.model].total_tokens_input += prompt_tokens #type: ignore
        return completion_tokens, prompt_tokens

    

tokenizer_callback_var: ContextVar[Optional[Tokenizer]] = ContextVar(
    "get_tokenizer_callback", default=None
)

register_configure_hook(tokenizer_callback_var, True)

    
@contextmanager
def get_team_tokenizer_callback(tokenizer: Tokenizer) -> Generator[Tokenizer, None, None]:
    """Context manager for managing a tokenizer callback.
    
    This is used to expose token and cost information from a tokenizer,
    typically used in NLP models.

    Args:
        tokenizer (Tokenizer): The tokenizer to be managed.

    Yields:
        Tokenizer: The managed tokenizer.
    """
    tokenizer_callback_var.set(tokenizer)
    try:
        yield tokenizer
    finally:
        tokenizer_callback_var.set(None)