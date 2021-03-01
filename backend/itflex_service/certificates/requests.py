from itflex_service.entities import Certificate
from formencode import Schema, validators


class GetCertificateById(Schema):
    id = validators.Int()


class PostCertificate(Certificate):
    pass

class PutCertificateById(Schema):
    id = validators.Int()
    certificate = Certificate()


class DeleteCertificateById(Schema):
    id = validators.Int()


class GetCertificates(Schema):
    name = validators.String()
    username = validators.String()
    sorts = validators.String()

