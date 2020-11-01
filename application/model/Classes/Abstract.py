from abc import abstractmethod, ABC


class BaseDocument(ABC):
    """
     BaseDocument - шаблон для все документов в соответсвии п5.2.1
     Общие атрибуты к определению для всех типов документов: Тип документа,
     Номер, Дата, Выдавший орган.
    """

    @property
    @abstractmethod
    def type_doc(self) -> None: pass

    @property
    @abstractmethod
    def num_doc(self) -> None: pass

    @property
    @abstractmethod
    def date_doc(self) -> None: pass

    @property
    @abstractmethod
    def institution(self) -> None: pass

    @property
    @abstractmethod
    def class_id(self) -> None: pass
