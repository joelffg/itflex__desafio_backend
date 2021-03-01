from itflex.common.response import (
    ErrorTypes,
    FieldError,
    ItemResp,
    ItemsResp,
    Status,
)
from itflex_service.certificates.interfaces import (
    ICertificatesUseCases,
    ICertificatesRepo
)
from itflex_service.certificates.requests import (
#    GetCertificateById,
    GetCertificates,
    PostCertificate,
    PutCertificateById,
    DeleteCertificateById
)
from itflex_service.entities import Certificate



class CertificatesUseCases(ICertificatesUseCases):
    def __init__(self, repo: ICertificatesRepo):
        self.repo = repo

    def post_certificate(self, req: Certificate) -> ItemResp:
        certificate = Certificate(
            id = req.get('id', None),
            username = req.get('username', None),
            name = req.get('name', None),
            description = req.get('description', None),
            expiration = req.get('expiration', None),
            expirated_at = req.get('expirated_at', None),
            created_at = req.get('created_at', None),
            updated_at = req.get('updated_at', None),
            groups = req.get('groups', [])
        )
        return self.repo.insert_certificate(certificate)

    def put_certificate(self, id, req: Certificate) -> ItemResp:
        certificate = Certificate(
            id = req.get('id', None),
            username = req.get('username', None),
            name = req.get('name', None),
            description = req.get('description', None),
            expiration = req.get('expiration', None),
            expirated_at = req.get('expirated_at', None),
            created_at = req.get('created_at', None),
            updated_at = req.get('updated_at', None),
            groups = req.get('groups', [])
        )

        return self.repo.update_certificate(id, certificate)

    def delete_certificate(self, id) -> ItemResp:
        return self.repo.delete_certificate(id)

    def get_certificates(self, name, username, sort) -> ItemResp:
        return self.repo.get_certificates(name=name, username=username, sort=sort)

    def get_certificate_by_id(
        self, id 
    ) -> ItemResp:
        return self.repo.get_certificate_by_id(id)

