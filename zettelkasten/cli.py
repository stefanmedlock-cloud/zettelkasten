import sys
import argparse
from zettelkasten.core import Zettelkasten

def main():
    parser = argparse.ArgumentParser(description="Zettelkasten Kommandozeilen-Schnittstelle")
    parser.add_argument("--db", required=True, help="Pfad zur Datenbankdatei")
    parser.add_argument("--backend", default="json", choices=["json", "sqlite"], help="Backend-Typ")
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

    args = parser.parse_args()
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
