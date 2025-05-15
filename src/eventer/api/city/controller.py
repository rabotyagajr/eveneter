from eventer.models import City
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError
from .schema import CityCreate, CityRead, CityUpdate
from sqlalchemy import select


class CityController:
    @staticmethod
    async def get_one(
        db_session: AsyncSession,
        id: int,
    ) -> Optional[CityRead]:
        result = await db_session.execute(select(City).where(City.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db_session: AsyncSession) -> List[CityRead]:
        result = await db_session.execute(select(City))
        cities = result.scalars().all()        
        return cities if cities else []
    
    @staticmethod
    async def patch_city(
        db_session: AsyncSession, id: int,
        data: CityUpdate,
    ) -> None:
        city = await db_session.get(City, id)
        
        if not city:
            raise ValueError(f"City with ID {id} not found")
        
        update_data = data.model_dump(exclude_unset=True)
        
        if not update_data:
            raise ValueError("No fields provided for update")
        
        for field, value in update_data.items():
            setattr(city, field, value)
        
        try:
            await db_session.commit()
            await db_session.refresh(city)
            return city
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise e
            
    @staticmethod
    async def create_city(
        db_session: AsyncSession,
        data: CityCreate,
    ):
        try:
            new_city = City(
                name=data.name
            )
            db_session.add(new_city)
            await db_session.commit()
            await db_session.refresh(new_city)
            return new_city
        except Exception as e:
            await db_session.rollback()
            
    
    @staticmethod
    async def delete_city(db_session: AsyncSession, city: City) -> None:
        await db_session.delete(city)
        await db_session.commit()