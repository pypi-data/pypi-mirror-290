from typing import List, Type

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from singularity.config import MongoConfig
from singularity.db.mongo.model import BaseModel
from singularity.exceptions import ConfigError


class Mongo:
    def __init__(self) -> None:
        self.client = None

    async def init(self) -> None:
        config = MongoConfig()

        if config.MONGO_DB and config.MONGO_URI:
            self.client = AsyncIOMotorClient(config.MONGO_URI)
            await init_beanie(
                database=self.client[config.MONGO_DB],
                document_models=self.get_document_models(),
            )
        else:
            raise ConfigError("MONGO_DB and MONGO_URI must be set in the config")
        return None

    def get_all_subclasses(self, cls: Type) -> List[Type]:
        subclasses = []
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
            subclasses.extend(self.get_all_subclasses(subclass))
        return subclasses

    def get_document_models(self) -> List[Type[Document]]:
        return [
            model
            for model in self.get_all_subclasses(BaseModel)
            if issubclass(model, Document)
        ]
