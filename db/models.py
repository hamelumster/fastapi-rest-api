from sqlalchemy import ForeignKey, DateTime, func, Integer, String, Float
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import db.Config

engine = create_async_engine(db.Config.PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    advertisements = relationship("Advertisement", back_populates="user")

    @property
    def to_dict(self):
        return {"id": self.id, "username": self.username}


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="advertisements")

    @property
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author": self.user.username if self.user else None,
            "created_at": self.created_at.isoformat(),
        }


ORM_OBJ_USR = User
ORM_OBJ_USR_CLS = type[ORM_OBJ_USR]

ORM_OBJ_ADV = Advertisement
ORM_OBJ_ADV_CLS = type[ORM_OBJ_ADV]

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()