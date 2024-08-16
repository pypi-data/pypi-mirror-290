from typing import Optional

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output

from . import bot


class SearchBotRetriever(Runnable):
    def __init__(self, b: bot.SearchBot):
        self.b = b

    def retrieve(self, query: str):
        return self.b.search(query)

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output:
        return self.retrieve(input)
