import datetime

from beanie import Document
from pydantic import BaseModel as PydanticBaseModel


class PydanticBase(PydanticBaseModel):
    created_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
    updated_at: datetime.datetime = datetime.datetime.now(datetime.UTC)
    deleted_at: datetime.datetime | None = None
    is_deleted: bool = False
    version: int = 1


class BeanieBase(Document):
    async def insert(self, *args, **kwargs):
        self.created_at = datetime.datetime.now(datetime.UTC)
        self.updated_at = datetime.datetime.now(datetime.UTC)
        return await super().insert(*args, **kwargs)

    async def delete(self, soft_delete=True, *args, **kwargs):
        if soft_delete:
            self.is_deleted = True
            self.deleted_at = datetime.datetime.now(datetime.UTC)
            return await self.save(*args, **kwargs)

    @classmethod
    async def get(cls, *args, **kwargs):
        return await super().get(*args, **kwargs)

    @classmethod
    async def get_one(cls, *args, **kwargs):
        return await super().find_one(*args, **kwargs)

    @classmethod
    async def list(
        cls, paginate: bool = True, page: int = 1, size: int = 10, *args, **kwargs
    ):
        if paginate:
            skip = (page - 1) * size
            return await super().find(*args, **kwargs).skip(skip).limit(size).to_list()
        else:
            return await super().find(*args, **kwargs).to_list()


class BaseModel(PydanticBase, BeanieBase):
    class Settings:
        is_abstract = True
