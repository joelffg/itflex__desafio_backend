from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, scoped_session, sessionmaker as SessionMaker

from itflex.common.response import ItemResp, ItemsResp, Resp, Status
from itflex.sqlalchemy2 import SQLBase
from itflex_service.entities import Certificate
from itflex_service.models import SQLCertificate, SQLCertificateGroup, SQLGroup
from itflex_service.certificates.interfaces import ICertificatesRepo


def make_certificates_filters(
        name: str, username: str
) -> List:
    filters = []

    if name:
        filters.append(SQLCertificate.name == name)
    if username:
        filters.append(SQLCertificate.username == username)

    return filters

class SQLCertificatesRepo(ICertificatesRepo):
    def __init__(self, sessionmaker: SessionMaker):
        self.sessionmaker = sessionmaker
        session = scoped_session(sessionmaker)
        SQLBase.metadata.create_all(bind=session.get_bind())
        try:
            grupo_adm = SQLGroup(codigo = 1)
            grupo_comercial = SQLGroup(codigo = 15)
            grupo_rh = SQLGroup(codigo = 30)
            session.add(grupo_adm)
            session.add(grupo_comercial)
            session.add(grupo_rh)
            session.commit()
        except Exception as e:
            pass


    #@autosession
    def insert_certificate(
        self, certificate: Certificate
    ) -> ItemResp:
        session = scoped_session(self.sessionmaker)
        db_certificate = certificate_to_db(certificate)
        session.add(db_certificate)
        for group in certificate.groups:
            new_certificado_grupo = SQLCertificateGroup(
                certificado_id = db_certificate.id,
                grupo_codigo = group
            )
            session.add(new_certificado_grupo)
        try:
            session.commit()
            return self.get_certificate_by_id(certificate.id)
        except Exception as e:
            session.rollback()
            return Resp(status=409, errors=[])

    #@autosession
    def update_certificate(
        self,
        id: int,
        certificate: Certificate,
    ) -> ItemResp:
        self.delete_certificate(id)
        certificate.id = id
        return self.insert_certificate(certificate)

    #@autosession
    def delete_certificate(
        self,
        id: int,
    ) -> ItemResp:
        session = scoped_session(self.sessionmaker)
        db_certificate = session.query(SQLCertificate).get(id)
        session.query(SQLCertificateGroup).filter_by(certificado_id=id).delete()
        session.delete(db_certificate)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()

        return ItemResp()

    #@autosession
    def get_certificates(
        self,
        name: str = None,
        username: str = None,
        sort: List = [],
    ) -> ItemResp:
        session = scoped_session(self.sessionmaker)
        db_certificates = session.query(SQLCertificate).filter(
            *make_certificates_filters(name, username)
        ).order_by(*sort).all()

        #certificates = [
        #    db_to_certificate(db_certificate) for db_certificate in db_certificates
        #]

        return ItemsResp(items=db_certificates)

    #@autosession
    def get_certificate_by_id(
        self,
        id: int = None,
    ) -> ItemResp:
        session = scoped_session(self.sessionmaker)
        db_certificate = session.query(SQLCertificate).get(id)
        
        return ItemResp(item=db_certificate)

def certificate_to_db(certificate: Certificate) -> SQLCertificate:
    return SQLCertificate(
        id = certificate.id,
        username = certificate.username,
        name = certificate.name,
        description = certificate.description,
        expiration = certificate.expiration,
        expirated_at = certificate.expirated_at,
        created_at = certificate.created_at,
        updated_at = certificate.updated_at
    )

