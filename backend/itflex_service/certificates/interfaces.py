from abc import ABC, abstractmethod
from typing import List

from itflex.common.response import ItemResp, ItemsResp
from itflex_service.entities import Certificate
from itflex_service.certificates.requests import (
    GetCertificateById,
    GetCertificates,
    PostCertificate,
    PutCertificateById,
    DeleteCertificateById
)


class ICertificatesRepo(ABC):
    @abstractmethod
    def insert_certificate(self, certificate: Certificate) -> ItemResp:
        raise NotImplementedError

    @abstractmethod
    def update_certificate(
        self,
        id: int,
        certificate: Certificate
    ) -> ItemResp:
        raise NotImplementedError

    @abstractmethod
    def delete_certificate(
        self, id: int
    ) -> ItemResp:
        raise NotImplementedError

    @abstractmethod
    def get_certificates(
        self, username: str = None, name: str = None, sort: List = []
    ) -> ItemsResp:
        raise NotImplementedError

    @abstractmethod
    def get_certificate_by_id(
        self, id: int
    ) -> ItemResp:
        raise NotImplementedError

class ICertificatesUseCases(ABC):
    @abstractmethod
    def __init__(self, repo: ICertificatesRepo):
        raise NotImplementedError

    @abstractmethod
    def post_certificate(self, req: PostCertificate) -> ItemResp:
        raise NotImplementedError

    @abstractmethod
    def put_certificate(self, req: PutCertificateById) -> ItemResp:
        raise NotImplementedError

    @abstractmethod
    def delete_certificate(self, req: DeleteCertificateById) -> ItemResp:
        raise NotImplementedError

    @abstractmethod
    def get_certificates(self, req: GetCertificates) -> ItemsResp:
        raise NotImplementedError

    @abstractmethod
    def get_certificate_by_id(
        self, req: GetCertificateById
    ) -> ItemResp:
        raise NotImplementedError


