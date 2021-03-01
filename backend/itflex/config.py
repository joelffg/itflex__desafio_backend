import logging
import socket
from configparser import ConfigParser
from os import environ, path
from urllib.parse import quote as urlquote

logger = logging.getLogger("thrift.transport.TSocket")
logger.disabled = True

CONFIG_PATH = "/etc/itflex/service.conf"
CONFIG_SECTION = "service"

TOKEN_SECRET = "test-secret"
TOKEN_REFRESH_TOKEN_EXP = 30 * 24 * 60 * 60
TOKEN_ACCESS_TOKEN_EXP = 5 * 60
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 5000
VERBOSE = 0

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "itflex"
MYSQL_USER = "itflex"
MYSQL_PASSWORD = "itflex-pass"

DHCP_DDNS_IP = "127.0.0.1"
DHCP_DDNS_PORT = 53001

BACKEND_SENTRY_URL = (
    "https://3040acd582e84d8997508d5e64e317c6@sentry.itflex.com.br/6"
)
FRONTEND_SENTRY_URL = (
    "https://3040acd582e84d8997508d5e64e317c6@sentry.itflex.com.br/6"
)
FRONTEND_MATOMO_URL = "https://matomo.itflex.com.br"
FRONTEND_SITE_ID = 2
CUSTOMER = None

AWS_S3_BUCKET_NAME = "itflex-client-backup-production"

DEBUG = bool(int(environ.get("DEBUG", 0)))

SERVER_NAME = socket.gethostname()

APPS = [
    "itflex_auth",
    "itflex_auth_sources",
    "itflex_backups",
    "itflex_openvpn",
    "itflex_networks",
    "itflex_ipsec",
    "itflex_dhcp",
    "itflex_dbc",
    "itflex_diagnostics",
    "itflex_dns_resolver",
    "itflex_firewall",
    "itflex_system",
    "itflex_net_charts",
    "itflex_logs",
    "itflex_email",
    "itflex_audit",
    "itflex_cluster",
    "itflex_sdwan",
    "itflex_alert",
    "itflex_historic",
    "itflex_sso",
    "itflex_webfilter",
    "itflex_monitoring",
    "itflex_virtualization",
]

if path.exists(CONFIG_PATH):
    config = ConfigParser()
    config.read(CONFIG_PATH)

    TOKEN_SECRET = config.get(
        CONFIG_SECTION, "token_secret", fallback=TOKEN_SECRET
    )
    HTTP_HOST = config.get(CONFIG_SECTION, "http_host", fallback=HTTP_HOST)
    HTTP_PORT = int(
        config.get(CONFIG_SECTION, "http_port", fallback=HTTP_PORT)
    )
    VERBOSE = int(config.get(CONFIG_SECTION, "verbose", fallback=VERBOSE))

    MYSQL_HOST = config.get(CONFIG_SECTION, "mysql_host", fallback=MYSQL_HOST)
    MYSQL_PORT = config.get(CONFIG_SECTION, "mysql_port", fallback=MYSQL_PORT)
    MYSQL_DATABASE = config.get(
        CONFIG_SECTION, "mysql_db", fallback=MYSQL_DATABASE
    )
    MYSQL_USER = config.get(CONFIG_SECTION, "mysql_user", fallback=MYSQL_USER)
    MYSQL_PASSWORD = config.get(
        CONFIG_SECTION, "mysql_password", fallback=MYSQL_PASSWORD
    )

    DHCP_DDNS_IP = config.get(
        CONFIG_SECTION, "dhcp_ddns_ip", fallback=DHCP_DDNS_IP
    )
    DHCP_DDNS_PORT = config.get(
        CONFIG_SECTION, "dhcp_ddns_port", fallback=DHCP_DDNS_PORT
    )

    AWS_S3_BUCKET_NAME = config.get(
        CONFIG_SECTION, "aws_s3_bucket_name", fallback=AWS_S3_BUCKET_NAME
    )

    CUSTOMER = config.get(CONFIG_SECTION, "customer", fallback=CUSTOMER)

    APPS = config.get(CONFIG_SECTION, "itflex_apps", fallback=APPS)
    if type(APPS) == str:
        APPS = APPS.split(",")
else:
    TOKEN_SECRET = environ.get("TOKEN_SECRET", TOKEN_SECRET)
    HTTP_HOST = environ.get("HTTP_HOST", HTTP_HOST)
    HTTP_PORT = int(environ.get("HTTP_PORT", HTTP_PORT))
    VERBOSE = int(environ.get("VERBOSE", VERBOSE))

    MYSQL_HOST = environ.get("MYSQL_HOST", MYSQL_HOST)
    MYSQL_PORT = int(environ.get("MYSQL_PORT", MYSQL_PORT))
    MYSQL_DATABASE = environ.get("MYSQL_DATABASE", MYSQL_DATABASE)
    MYSQL_USER = environ.get("MYSQL_USER", MYSQL_USER)
    MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD", MYSQL_PASSWORD)

    DHCP_DDNS_IP = environ.get("DHCP_DDNS_IP", DHCP_DDNS_IP)
    DHCP_DDNS_PORT = int(environ.get("DHCP_DDNS_PORT", DHCP_DDNS_PORT))

    CUSTOMER = environ.get("CUSTOMER", CUSTOMER)

    APPS = environ.get("APPS", APPS)
    if type(APPS) == str:
        APPS = APPS.split(",")


MYSQL_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    MYSQL_USER,
    urlquote(MYSQL_PASSWORD),
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
)

MYSQL_URL = environ.get("MYSQL_URL", MYSQL_URL)

SCOPES = None
AUDIT_MODULES = None


def set_scopes(scopes):
    global SCOPES
    SCOPES = scopes


def set_audit_modules(modules):
    global AUDIT_MODULES
    AUDIT_MODULES = modules


def get_scopes():
    return SCOPES


def get_audit_modules():
    return AUDIT_MODULES

