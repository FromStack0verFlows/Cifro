from application.model.Classes.Abstract import BaseDocument
from application.model.Classes.CLASS1Collection import *
from application.model.Database.db_setup import session
from flask import request


def init(collection) -> BaseDocument:
    if isinstance(collection, CLASS1Collection):
        return CLASS1Document(**vars(collection))


def session_closure(function):
    def wrapper(self, *args):
        session.close()
        return function(self)

    return wrapper


class GlobalApplicationModel:

    def __init__(self):
        self.__collections: [Base] = [CLASS1Collection]
        self.__documents: [BaseDocument] = self.__fetch_documents()
        self.__documentsForDashboard: [BaseDocument] = self.__documentsPagination()

    @session_closure
    def __fetch_documents(self) -> [BaseDocument]:
        return [init(collection) for document in self.__collections for collection in session.query(document).all()]

    def __documentsPagination(self):
        page = request.args.get("page")
        if page and int(page):
            self.__current_page = int(page)
        else:
            self.__current_page = 1
        self.__pages = self.count // 8 + 1
        return self.__documents[0:8] if self.current_page == 1 else self.__documents[
                                                                    self.current_page * 8:self.current_page * 8 + 8]

    @property
    def count(self) -> int:
        return len(self.__documents)

    @property
    def documents(self) -> [BaseDocument]:
        return self.__documents

    @property
    def documentsWithPagination(self):
        return self.__documentsForDashboard

    @property
    def categories(self) -> [str]:
        return list(set([category.type_doc for category in self.__documents]))

    @property
    def pages(self) -> int:
        return self.__pages

    @property
    def current_page(self) -> int:
        return self.__current_page
