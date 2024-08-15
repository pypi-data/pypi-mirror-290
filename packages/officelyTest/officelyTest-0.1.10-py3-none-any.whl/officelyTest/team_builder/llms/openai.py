from typing import Dict, List, Tuple
from langchain_openai import ChatOpenAI
from pydantic import model_validator

from officelyTest.CustomException import MissingEnvKeys
from officelyTest.stream_handler import StreamHandler
from .llm import LLM
import os





class OpenAILLM(LLM):
    streaming:bool = True



    @property
    def base(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise MissingEnvKeys("Environment variable 'OPENAI_API_KEY' is required but not set.")
        callbacks = []
        if self.tokenizer:
            self.tokenizer.model = self.model
            callbacks.append(self.tokenizer)
        is_answer = False
        if self.g:
            callbacks.append(StreamHandler(gen=self.g, with_final=False))
            is_answer = self.g.is_answer

        return ChatOpenAI(
            model=self.model, 
            temperature=self.temperature, 
            streaming=is_answer and self.streaming, 
            callbacks=callbacks
        )
    
    def with_schema(self, prompt:List[Tuple[str, str]], schema:Dict, name:str):
        self.streaming = False
        return self.base.with_structured_output(schema).with_config({"run_name":name}).invoke(prompt)
    
