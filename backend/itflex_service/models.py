import sqlalchemy as sa
from sqlalchemy.orm import relationship

from itflex_service.deps import SQLBase


class SQLGroup(SQLBase):

    __tablename__ = "service_group"

    codigo = sa.Column(sa.Integer, primary_key=True)
    def __repr__(self):
        return "Código = '%s'" % (self.codigo)

    @property
    def serialize(self):
        return self.codigo


class SQLCertificate(SQLBase):

    __tablename__ = "service_certificate"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(30))
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.String(255))
    expiration = sa.Column(sa.Integer)
    expirated_at = sa.Column(sa.DateTime)
    created_at = sa.Column(sa.DateTime)
    updated_at = sa.Column(sa.DateTime)

    groups = relationship('SQLGroup', secondary="service_certificate_group")

    def __repr__(self):
        return "ID = '%s', Usuário = '%s', Nome = '%s'" % (self.id, self.username, self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'description': self.description,
            'groups': [group.serialize for group in self.groups],
            'expiration': self.expiration,
            'expirated_at': self.expirated_at.strftime("%Y-%m-%dT%H:%M:%S%z"),
            'created_at': self.created_at.strftime("%Y-%m-%dT%H:%M:%S%z"),
            'updated_at': self.updated_at.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }


class SQLCertificateGroup(SQLBase):

    __tablename__ = "service_certificate_group"

    certificado_id = sa.Column(sa.Integer, sa.ForeignKey('service_certificate.id'), primary_key=True, nullable=False)
    grupo_codigo = sa.Column(sa.Integer, sa.ForeignKey('service_group.codigo'), primary_key=True, nullable=False)

    def __repr__(self):
        return "CertificadoId = '%s', GrupoCodigo = '%s'" % (self.certificado_id, self.grupo_codigo)

