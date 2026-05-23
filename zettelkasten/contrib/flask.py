import time
try:
    from flask.sessions import SessionInterface, SessionMixin
except ImportError:
    class SessionInterface: pass
    class SessionMixin: pass

from zettelkasten.core import Zettelkasten

class ZettelkastenSession(dict, SessionMixin):
    pass

class ZettelkastenSessionInterface(SessionInterface):
    def __init__(self, filepath=None, backend="json"):
        self.db = Zettelkasten(filepath, backend=backend)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            import uuid
            sid = str(uuid.uuid4())
            return ZettelkastenSession(sid=sid)
        val = self.db.get(sid)
        if val is not None:
            return ZettelkastenSession(val, sid=sid)
        return ZettelkastenSession(sid=sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            if session.modified:
                self.db.delete(session.sid)
                response.delete_cookie(app.session_cookie_name, domain=domain, path=path)
            return
        expire = self.get_expiration_time(app, session)
        ttl = int(expire.timestamp() - time.time()) if expire else None
        self.db.set(session.sid, dict(session), ttl=ttl)
        response.set_cookie(app.session_cookie_name, session.sid, expires=expire, httponly=True, domain=domain, path=path)
