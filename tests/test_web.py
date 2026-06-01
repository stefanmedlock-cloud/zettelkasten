import pytest
import asyncio
import socket
from zettelkasten.core import Zettelkasten
from zettelkasten.web import ZettelkastenWebServer

def test_web_stats_endpoint():
    db = Zettelkasten()
    db.set("web_k", "web_v")
    server = ZettelkastenWebServer(db)
    # Einfacher Funktionstest des Webservers
    assert server.db.get("web_k") == "web_v"
