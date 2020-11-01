from sqlalchemy import Column, Integer, String
from application.model.Database.db_setup import Base
from .Abstract import BaseDocument


class CLASS1Collection(Base):
    __tablename__ = "class1"

    id = Column(Integer, primary_key=True)
    number = Column(String)  # Идентификационный номер документа
    imagepath = Column(String)  # Ориг. данные
    district = Column(String)  # Административный округ
    region = Column(String)  # Район
    address = Column(String)  # Адрес
    objectname = Column(String)  # Наименование объекта
    objectpurpose = Column(String)  # Функциональное назначение объекта


class CLASS1Document(BaseDocument):
    __slots__ = ["id", "number", "imagepath", "district", "region", "address", "objectname", "objectpurpose"]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key != "_sa_instance_state":
                setattr(self, key, value)

    @property
    def type_doc(self) -> str:
        return "Свидетельство об утверждении архитектурно-градостроительного решения"

    @property
    def num_doc(self) -> str:
        return self.number if self.number else "Пусто"

    @property
    def date_doc(self) -> int:
        return 1

    @property
    def institution(self) -> str:
        return "Комитет по архитектуре и градостроительству г. Москвы"

    @property
    def class_id(self):
        return "class1"

    def json(self):
        return {'id': self.id,
                'number': self.number,
                'imagepath': self.imagepath,
                'district': self.district,
                'region': self.region,
                'address': self.address,
                'objectname': self.objectname,
                'objectpurpose': self.objectpurpose
                }
