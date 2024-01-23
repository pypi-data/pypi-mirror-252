from typing import Generator

from chatfaq_sdk.api.knowledge_items import KnowledgeItem


class DataSourceParser:
    def __init__(self, data_source):
        self.data_source = data_source

    def parse(self) -> Generator[KnowledgeItem]:
        raise NotImplementedError()
