import asyncio
from abc import abstractmethod
from dataclasses import dataclass
from typing import Coroutine, Generic, TypeVar


class NotInstantiated:
    """Класс для запрета инстанцирования."""

    def __init__(self) -> None:
        raise RuntimeError("Class cannot be instantiated.")


TLib = TypeVar("TLib")


@dataclass(frozen=True, slots=True)
class TypeCapsule(Generic[TLib]):
    """Капсула типа."""

    cls: type[TLib]


class ObjectCapsule(Generic[TLib], NotInstantiated):
    """Капсула объекта."""

    _instance: TLib | None = None
    _type_capsule: TypeCapsule[TLib] | None = None

    @classmethod
    def type_capsule(cls) -> TypeCapsule[TLib]:
        """Капсула типа."""
        if cls._type_capsule is not None:
            return cls._type_capsule
        raise ValueError("Type capsule is not set.")

    @staticmethod
    @abstractmethod
    def _init() -> TLib:
        """Инициализация ресурсов."""
        raise NotImplementedError

    @classmethod
    def instance(cls) -> TLib:
        """Получение инстанса."""
        if cls._instance is None:
            cls._instance = cls._init()
            cls._type_capsule = TypeCapsule(type(cls._instance))
            LibsContainer.register(cls._type_capsule, cls.close())
        return cls._instance  # type: ignore

    _closed = False

    @classmethod
    @abstractmethod
    async def _close(cls) -> None:
        """Обработка закрытия ресурсов."""
        raise NotImplementedError

    @classmethod
    async def close(cls) -> None:
        """Закрытие ресурсов."""
        if cls._instance is not None and not cls._closed:
            cls._closed = True
            await cls._close()


class LibsContainer(Generic[TLib], NotInstantiated):
    """Контейнер для регистрации инстансов."""

    _registry: dict[TypeCapsule[TLib], Coroutine[None, None, None]] = {}

    @classmethod
    def register(cls, lib: TypeCapsule[TLib], coro: Coroutine[None, None, None]) -> None:
        """Регистрация инстанса."""
        if lib in cls._registry:
            raise ValueError(f"Key {lib} already registered.")
        cls._registry[lib] = coro

    @classmethod
    async def shutdown(cls) -> None:
        """Закрытие всех ресурсов."""
        await asyncio.gather(*cls._registry.values(), return_exceptions=False)


__all__ = ["ObjectCapsule", "LibsContainer"]
