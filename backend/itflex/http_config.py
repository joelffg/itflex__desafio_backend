from importlib import import_module

from flask import Flask
from flask_socketio import SocketIO

from itflex.config import APPS, DEBUG, set_audit_modules, set_scopes
from itflex.deps import setup_deps

try:
    # Werkzeug 0.15 and newer
    from werkzeug.middleware.proxy_fix import ProxyFix
except ImportError:
    # older releases
    from werkzeug.contrib.fixers import ProxyFix


def import_modules(apps):
    modules = []
    for app in sorted(set(apps)):
        module = import_module(app)
        modules.append(module)

    return modules


def setup_app(apps=None) -> Flask:
    if apps is None:
        apps = APPS

    modules = import_modules(apps)

    app = Flask("itflex")
    app.config["MAX_CONTENT_LENGTH"] = 30 * 1024 * 1024 * 1024
    app.wsgi_app = ProxyFix(app.wsgi_app)
    socketio = SocketIO(app)
    deps = setup_deps(app, socketio)

    scopes = []
    audit_modules = []
    for module in modules:
        deps_mod = import_module(module.__name__ + ".deps")
        try:
            get_scopes = deps_mod.get_scopes
            scopes.extend(get_scopes())
        except AttributeError:
            pass

        try:
            get_audit_module = deps_mod.get_audit_module
            audit_modules.append(get_audit_module())
        except AttributeError:
            pass

    set_scopes(scopes)
    set_audit_modules(audit_modules)

    for module in modules:
        if hasattr(module, "setup"):
            setup = module.setup
        else:
            setup_mod = import_module(module.__name__ + ".setup")
            setup = setup_mod.setup

        before_start = setup(deps, scopes)
        if before_start:
            before_start()

    app.debug = DEBUG

    return app, socketio

