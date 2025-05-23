import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Integer, String, Float, UUID, Boolean, Column, Table
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
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    tokens: Mapped[list["Token"]] = relationship(
        "Token",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
    advertisements: Mapped[list["Advertisement"]] = relationship(
        "Advertisement",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
        lazy="selectin"
    )

    @property
    def to_dict(self):
        return {"id": self.id, "username": self.username}


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="advertisements", lazy="selectin")

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

class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True,
                                             nullable=False, server_default=func.gen_random_uuid())
    creation_time: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="tokens", lazy="selectin")

    @property
    def to_dict(self):
        return {
            "token": self.token,
        }


class Right(Base):
    __tablename__ = "rights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    read: Mapped[bool] = mapped_column(Boolean, nullable=False)
    create: Mapped[bool] = mapped_column(Boolean, nullable=False)
    change: Mapped[bool] = mapped_column(Boolean, nullable=False)
    delete: Mapped[bool] = mapped_column(Boolean, nullable=False)

    roles: Mapped[list["Role"]] = relationship(
        secondary="roles_rights", back_populates="rights", lazy="selectin"
    )

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    rights: Mapped[list["Right"]] = relationship(
        secondary="roles_rights", back_populates="roles", lazy="selectin"
    )
    users: Mapped[list["User"]] = relationship(
        secondary="user_roles", back_populates="roles", lazy="selectin"
    )


roles_rights = Table(
    "roles_rights",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("right_id", Integer, ForeignKey("rights.id")),
)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)



ORM_OBJ_USR = User
ORM_OBJ_USR_CLS = type[ORM_OBJ_USR]

ORM_OBJ = Advertisement | Token
ORM_OBJ_CLS = type[Advertisement] | type[Token]

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()