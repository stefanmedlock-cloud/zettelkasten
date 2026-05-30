import sys
import argparse
import asyncio
from zettelkasten.core import Zettelkasten
from zettelkasten.server import ZettelkastenServer
from zettelkasten.web import ZettelkastenWebServer

def main():
    parser = argparse.ArgumentParser(description="Zettelkasten Kommandozeilen-Schnittstelle")
    parser.add_argument("--db", help="Pfad zur Datenbankdatei")
    parser.add_argument("--backend", default="json", choices=["json", "sqlite", "network"], help="Backend-Typ")
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="Setzt ein Key-Value Paar")
    set_parser.add_argument("key", help="Key Name")
    set_parser.add_argument("value", help="Wert zum Speichern")
    set_parser.add_argument("--ttl", type=int, help="Lebensdauer (TTL) in Sekunden")

    get_parser = subparsers.add_parser("get", help="Gibt den Wert eines Keys zurück")
    get_parser.add_argument("key", help="Key Name")

    del_parser = subparsers.add_parser("delete", help="Löscht einen Key")
    del_parser.add_argument("key", help="Key Name")

    subparsers.add_parser("keys", help="Listet alle Keys auf")

    server_parser = subparsers.add_parser("run-server", help="Startet den Zettelkasten TCP-Datenbankserver")
    server_parser.add_argument("--host", default="localhost", help="Server Hostname")
    server_parser.add_argument("--port", type=int, default=8080, help="Server Port")
    server_parser.add_argument("--web-port", type=int, help="Optionaler Web-Dashboard Port")
    server_parser.add_argument("--role", choices=["master", "replica"], help="Replikations-Rolle")
    server_parser.add_argument("--master-addr", help="Adresse des Masters bei Replica-Rolle")

    args = parser.parse_args()

    if args.command == "run-server":
        server = ZettelkastenServer(args.host, args.port, args.db, backend=args.backend, role=args.role, master_addr=args.master_addr)
        if args.web_port:
            web_server = ZettelkastenWebServer(server.db, args.host, args.web_port)
            async def run_both():
                await asyncio.gather(server.start(), web_server.start())
            try:
                asyncio.run(run_both())
            except KeyboardInterrupt:
                print("Server gestoppt.")
        else:
            try:
                asyncio.run(server.start())
            except KeyboardInterrupt:
                print("Server gestoppt.")
        return

    db = Zettelkasten(args.db, backend=args.backend)

    if args.command == "set":
        db.set(args.key, args.value, ttl=args.ttl)
        print(f"Key '{args.key}' erfolgreich gesetzt.")
    elif args.command == "get":
        val = db.get(args.key)
        if val is None:
            print("Key nicht gefunden.")
            sys.exit(1)
        print(val)
    elif args.command == "delete":
        deleted = db.delete(args.key)
        if deleted:
            print(f"Key '{args.key}' gelöscht.")
        else:
            print(f"Key '{args.key}' nicht gefunden.")
            sys.exit(1)
    elif args.command == "keys":
        keys = db.keys()
        for k in keys:
            print(k)

if __name__ == "__main__":
    main()
