import asyncio
from typing import Any, Union, AsyncIterable

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from dbcc.base import TableEngine

mongo = None


def remove_id(payload: dict):
    if "_id" in payload:
        del payload["_id"]


class MongoTableEngine(TableEngine):
    db: Any = None
    collection: Any = None

    def __init__(
        self,
        url: str,
        db_name: str,
        collection_name: str = None,
        mongo_duplicate_id: bool = True,
        mock_db_in_mem: bool = False,
        add_short_id: bool = True
    ):
        super().__init__(url, db_name, collection_name)
        global mongo

        if not mongo:
            if not mock_db_in_mem:
                mongo = AsyncIOMotorClient(
                    url, connect=False, uuidRepresentation="standard"
                )
                mongo.get_io_loop = asyncio.get_event_loop
            else:
                from mongomock_motor import AsyncMongoMockClient

                mongo = AsyncMongoMockClient(url, connect=False)
                mongo.get_io_loop = asyncio.get_event_loop
        self.db = mongo[self.db_name]
        if collection_name:
            self.collection = self.db[collection_name]
        self.mongo_duplicate_id = mongo_duplicate_id
        self.add_short_id = add_short_id

    def __getitem__(self, key):
        return MongoTableEngine(self.url, self.db_name, key)

    async def find_batch(
        self,
        pattern: dict = None,
        skip: int = None,
        limit: int = None,
        sort: list = None,
        projection: dict = None,
    ) -> list:
        return [
            entity
            async for entity in self.find_batch_raw(
                pattern, skip, limit, sort, projection
            )
        ]

    def find_batch_raw(
        self,
        pattern: dict = None,
        skip: int = None,
        limit: int = None,
        sort: list = None,
        projection: dict = None,
    ) -> AsyncIterable:
        routine = self.collection.find(pattern, projection)
        if sort:
            routine = routine.sort(sort)
        if limit:
            routine = routine.limit(limit)
        if skip:
            routine = routine.skip(skip)
        return routine

    async def count(self, pattern: dict = None):
        return await self.collection.count_documents(pattern)

    async def create(self, entry: dict, add_short_id: bool | None = None) -> dict:
        inserted_id = ObjectId((await self.collection.insert_one(entry)).inserted_id)
        update_payload = {}
        if self.mongo_duplicate_id:
            update_payload["id"] = inserted_id
            entry["id"] = inserted_id
        if (add_short_id is None and self.add_short_id) or add_short_id:
            update_payload["short_id"] = str(inserted_id)[-6:]
        if update_payload:
            await self.update_by_id(inserted_id, update_payload)
        entry["_id"] = inserted_id
        return entry

    async def update_by_id(self, id: Union[str, ObjectId], payload: dict):
        remove_id(payload)
        return await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": payload}
        )

    async def delete_by_id(self, id: Union[str, ObjectId]):
        await self.collection.delete_one({"_id": ObjectId(id)})

    async def find_single(self, field: str, value: Any, projection: dict = None):
        routine = self.collection.find_one({field: value}, projection)
        return await routine
