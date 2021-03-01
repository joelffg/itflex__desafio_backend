from itflex.deps import SetupDeps

from .certificates.api import register_routes as certificates_routes
from .certificates.repo import SQLCertificatesRepo
from .certificates.use_cases import CertificatesUseCases


def setup(deps: SetupDeps, scopes):  # noqa

    certificates_repo = SQLCertificatesRepo(deps.sessionmaker)
    certificates_use_cases = CertificatesUseCases(certificates_repo)
    certificates_routes(deps.app, certificates_use_cases)

