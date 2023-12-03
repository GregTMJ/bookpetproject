from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.configs import get_session
from src.users.models import User
from src.users.schemas import CreateUser, UpdateUser, UserDetails

user_router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


@user_router.get("/", response_model=list[UserDetails], status_code=200)
async def get_all_users(
    offset: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    q = await session.execute(select(User).limit(limit).offset(offset))
    return q.scalars()


@user_router.post("/", response_model=UserDetails, status_code=201)
async def create_user(user: CreateUser, session: AsyncSession = Depends(get_session)):
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    await session.flush()
    return new_user


@user_router.get("/{user_id}", response_model=UserDetails, status_code=200)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.patch("/{user_id}", response_model=UserDetails, status_code=200)
async def update_user(
    user_id: int, user_update: UpdateUser, session: AsyncSession = Depends(get_session)
):
    q = await session.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print("my next step")
    user_data = user_update.model_dump(exclude_unset=True)
    print(user.name)
    for key, value in user_data.items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    await session.flush()
    return user


@user_router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    q = await session.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()
    await session.flush()
    return
