import os
import json
from zettelkasten.core import Zettelkasten

db_path = "/tmp/lambda_zettel.db"
db = Zettelkasten(db_path, backend="sqlite")

def lambda_handler(event, context):
    query_params = event.get("queryStringParameters") or {}
    cmd = query_params.get("cmd")
    key = query_params.get("key")
    val = query_params.get("val")
    
    res = {"status": "ok"}
    if cmd == "set" and key:
        db.set(key, val)
    elif cmd == "get" and key:
        res["val"] = db.get(key)
    elif cmd == "delete" and key:
        res["deleted"] = db.delete(key)
    elif cmd == "keys":
        res["keys"] = db.keys()
    else:
        res = {"status": "error", "message": "Falsche Parameter"}

    return {
        "statusCode": 200,
        "body": json.dumps(res),
        "headers": {
            "Content-Type": "application/json"
        }
    }
