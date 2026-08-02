from typing import TypeVar, Generic, List, Optional, Any, Dict
from beanie import Document
from pydantic import BaseModel

T = TypeVar("T", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    async def get(self, id: Any) -> Optional[T]:
        return await self.model.get(id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return await self.model.find_all().skip(skip).limit(limit).to_list()

    async def create(self, obj_in: CreateSchemaType | Dict[str, Any]) -> T:
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = self.model(**obj_in.model_dump())
        await db_obj.insert()
        return db_obj

    async def update(self, db_obj: T, obj_in: UpdateSchemaType | Dict[str, Any]) -> T:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        await db_obj.set(update_data)
        return db_obj

    async def remove(self, id: Any) -> Optional[T]:
        db_obj = await self.get(id)
        if db_obj:
            await db_obj.delete()
        return db_obj
