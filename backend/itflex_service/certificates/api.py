from typing import List

from flask import Flask, request as http_req

from itflex.common.http import API, HttpResp, dump_errors, http_status 
from itflex_service.certificates.interfaces import ICertificatesUseCases
from itflex_service.entities import Certificate


def certificate_to_json(certificate: Certificate):
    if certificate:
        return certificate.serialize
    return dump_errors(certificate)


def certificates_to_json(certificates: List[Certificate]):
    return [certificate_to_json(certificate) for certificate in certificates]


class CertificateListAPI(API):
    def __init__(self, certificates_use_cases: ICertificatesUseCases):
        super().__init__()
        self.uc = certificates_use_cases

    def get(self) -> HttpResp:
        sort= http_req.args.getlist("sort[]")
        username = http_req.args.get("username")
        name = http_req.args.get("name")

        resp = self.uc.get_certificates(sort=sort, username=username, name=name)

        if resp.ok:
            data = {"certificates": certificates_to_json(resp.items)}
        else:
            data = dump_errors(resp.errors)
        return data, resp.status


class CertificateAPI(API):
    def __init__(self, certificates_use_cases: ICertificatesUseCases):
        super().__init__()
        self.uc = certificates_use_cases

    def get(self, id: str) -> HttpResp:
        resp = self.uc.get_certificate_by_id(id=id)
        if resp.ok:
            data = certificate_to_json(resp.item)
        else:
            data = dump_errors(resp.errors)

        return data, resp.status

    def post(self) -> HttpResp:
        certificate_json = http_req.json
        resp = self.uc.post_certificate(req=certificate_json)
        
        if resp.ok:
            data = certificate_to_json(resp.item)
        else:
            data = dump_errors(resp.errors)
        
        return data, http_status(resp.status)

    def put(self, id: str) -> HttpResp:
        certificate_json = http_req.json
        resp = self.uc.put_certificate(id=id, req=certificate_json)

        if resp.ok:
            data = certificate_to_json(resp.item)
        else:
            data = dump_errors(resp.errors)

        return data, resp.status

    def delete(self, id: str) -> HttpResp:
        resp = self.uc.delete_certificate(id=id)

        if resp.ok:
            data = certificate_to_json(resp.item)
        else:
            data = dump_errors(resp.errors)

        return data, resp.status



def register_routes(app: Flask, certificates_use_cases: ICertificatesUseCases):
    certificates_list_api = CertificateListAPI(certificates_use_cases)
    certificate_api = CertificateAPI(certificates_use_cases)

    app.add_url_rule(
        "/api/service/certificates",
        "service.certificates.list",
        certificates_list_api,
        methods=certificates_list_api.methods,
    )
    app.add_url_rule(
        "/api/service/certificate/<string:id>",
        "service.certificates.single",
        certificate_api,
        methods=certificate_api.methods.remove('POST'),
    )
    app.add_url_rule(
        "/api/service/certificate/",
        "service.certificates.post",
        certificate_api.post,
        methods=["POST"]
    )

