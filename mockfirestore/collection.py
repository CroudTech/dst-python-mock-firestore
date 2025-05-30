import warnings
from typing import Any, List, Optional, Iterable, Dict, Tuple, Sequence, Union
from google.cloud.firestore_v1.base_query import FieldFilter, And, Or

from mockfirestore import AlreadyExists
from mockfirestore._helpers import (
    generate_random_string,
    Store,
    get_by_path,
    set_by_path,
    Timestamp,
)
from mockfirestore.query import Query
from mockfirestore.document import DocumentReference, DocumentSnapshot


class CollectionReference:
    def __init__(
        self, data: Store, path: List[str], parent: Optional[DocumentReference] = None
    ) -> None:
        self._data = data
        self._path = path
        self.parent = parent

        # The collection ID is the last of the elements.
        self.id = self._path[-1]

    def document(self, document_id: Optional[str] = None) -> DocumentReference:
        collection = get_by_path(self._data, self._path)
        if document_id is None:
            document_id = generate_random_string()
        new_path = self._path + [document_id]
        if document_id not in collection:
            set_by_path(self._data, new_path, {})
        return DocumentReference(self._data, new_path, parent=self)

    def get(self) -> Iterable[DocumentSnapshot]:
        warnings.warn(
            "Collection.get is deprecated, please use Collection.stream",
            category=DeprecationWarning,
        )
        return self.stream()

    def add(
        self, document_data: Dict, document_id: str = None
    ) -> Tuple[Timestamp, DocumentReference]:
        if document_id is None:
            document_id = document_data.get("id", generate_random_string())
        collection = get_by_path(self._data, self._path)
        new_path = self._path + [document_id]
        if document_id in collection:
            raise AlreadyExists("Document already exists: {}".format(new_path))
        doc_ref = DocumentReference(self._data, new_path, parent=self)
        doc_ref.set(document_data)
        timestamp = Timestamp.from_now()
        return timestamp, doc_ref

    def where(
        self,
        field: Optional[str] = None,
        op: Optional[str] = None,
        value: Optional[Any] = None,
        filter: Union[FieldFilter, And, Or, None] = None,
    ) -> Query:
        if filter is None and (field is None or op is None or value is None):
            raise ValueError(
                "field, op, and value must be provided (or a FieldFilter instance)"
            )
        if filter is None:
            filter = FieldFilter(field, op, value)
        query = Query(self, field_filter=filter)
        return query

    def order_by(self, key: str, direction: Optional[str] = None) -> Query:
        query = Query(self, orders=[(key, direction)])
        return query

    def limit(self, limit_amount: Optional[int]) -> Query:
        if not isinstance(limit_amount, (int, type(None))):
            raise TypeError(
                f"TypeError: Cannot set google.protobuf.Int32Value.value to {limit_amount}:"
                f" {limit_amount} has type {type(limit_amount)},"
                f" but expected one of: ({int},) for field Int32Value.value"
            )
        query = Query(self, limit=limit_amount)
        return query

    def offset(self, offset: int) -> Query:
        query = Query(self, offset=offset)
        return query

    def start_at(
        self, document_fields_or_snapshot: Union[dict, DocumentSnapshot]
    ) -> Query:
        query = Query(self, start_at=(document_fields_or_snapshot, True))
        return query

    def start_after(
        self, document_fields_or_snapshot: Union[dict, DocumentSnapshot]
    ) -> Query:
        query = Query(self, start_at=(document_fields_or_snapshot, False))
        return query

    def end_at(
        self, document_fields_or_snapshot: Union[dict, DocumentSnapshot]
    ) -> Query:
        query = Query(self, end_at=(document_fields_or_snapshot, True))
        return query

    def end_before(
        self, document_fields_or_snapshot: Union[dict, DocumentSnapshot]
    ) -> Query:
        query = Query(self, end_at=(document_fields_or_snapshot, False))
        return query

    def list_documents(
        self, page_size: Optional[int] = None
    ) -> Sequence[DocumentReference]:
        docs = []
        for key in get_by_path(self._data, self._path):
            docs.append(self.document(key))
        return docs

    def stream(self, transaction=None) -> Iterable[DocumentSnapshot]:
        for key in sorted(get_by_path(self._data, self._path)):
            doc_snapshot = self.document(key).get()
            yield doc_snapshot


# Taken from https://github.com/ainbr/python-mock-firestore/blob/a02dd24e770cc1eafe21a862b055fe833e6f1f48/mockfirestore/collection.py
class CollectionGroupReference(CollectionReference):
    def recursive_reference(
        self, path: List[str]
    ) -> Union[DocumentReference, CollectionReference]:
        if len(path) == 1:
            return CollectionReference(self._data, path)
        else:
            if len(path) % 2 == 0:
                return DocumentReference(
                    self._data, path, parent=self.recursive_reference(path[:-1])
                )
            else:
                return CollectionReference(
                    self._data, path, parent=self.recursive_reference(path[:-1])
                )

    def document(
        self, document_id: Optional[str] = None, path: List[str] = None
    ) -> DocumentReference:
        if path is None:
            path = self._path
        collection = get_by_path(self._data, path)
        if document_id is None:
            document_id = generate_random_string()
        # new_path = self._path + [document_id]
        ret = self.recursive_reference(path)
        return ret

    def get(self) -> Iterable[DocumentSnapshot]:
        warnings.warn(
            "Collection.get is deprecated, please use Collection.stream",
            category=DeprecationWarning,
        )
        return self.stream()

    def stream(self, transaction=None) -> Iterable[DocumentSnapshot]:
        for path in self._path:
            doc_snapshot = self.document(path[-1], path).get()
            yield doc_snapshot
