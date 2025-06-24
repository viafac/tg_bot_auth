import uuid

from sqlalchemy import ForeignKey, String, Boolean, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class Permissions(Base):
    __tablename__ = "permissions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class RolePermissions(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )
    permission_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )


class TelegramUsers(Base):
    __tablename__ = 'telegram_users'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[str] = mapped_column(String(20), unique=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class Employers(Base):
    __tablename__ = 'employers'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime,  server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime,  server_default=func.now())


class AppUsers(Base):
    __tablename__ = 'app_users'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telegram_users.id", ondelete="CASCADE"),
        nullable=False, unique=True
    )
    employer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("employers.id", ondelete="CASCADE"),
        nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_seen: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class AppUsersHistory(Base):
    __tablename__ = 'app_users_history'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    telegram_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("telegram_users.id", ondelete="CASCADE"),
        nullable=False,
    )
    employer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("employers.id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    last_seen:   Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    created_at:  Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at:  Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    changed_at:  Mapped[DateTime] = mapped_column(DateTime,  server_default=func.now())

    changed_by_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app_users.id", ondelete="CASCADE"),
        nullable=False,
    )
