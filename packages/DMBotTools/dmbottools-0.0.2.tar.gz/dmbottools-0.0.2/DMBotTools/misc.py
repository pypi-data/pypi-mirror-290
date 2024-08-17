from typing import Any


class GlobalClass:
    """
    GlobalClass реализует паттерн Singleton, обеспечивая создание только одного экземпляра класса.
    Это может быть полезно для создания глобальных объектов, доступных из любого места в коде.

    Attributes:
        _instance (Any): Единственный экземпляр класса. Изначально `None`, затем инициализируется первым вызовом `__new__`.
    """

    _instance: Any = None

    def __new__(cls, *args, **kwargs):
        """
        Создает и возвращает единственный экземпляр класса GlobalClass.
        Если экземпляр уже существует, возвращает его.

        Returns:
            GlobalClass: Экземпляр класса GlobalClass.
        """
        if cls._instance is None:
            cls._instance = super(GlobalClass, cls).__new__(cls)
        
        return cls._instance

    def _is_not_initialized(self) -> bool:
        """
        Проверяет, был ли экземпляр класса ранее инициализирован.
        Если инициализация происходит впервые, метод возвращает `True` и устанавливает флаг `_initialized`.
        В последующих вызовах метод возвращает `False`.

        Returns:
            bool: `True`, если экземпляр не был ранее инициализирован, иначе `False`.
        """
        if not hasattr(self, '_initialized'):
            self._initialized = True
            return True
        
        return False
