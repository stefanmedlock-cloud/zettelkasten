from zettelkasten.contrib.fastapi import init_db, get_db

def test_fastapi_contrib():
    db = init_db()
    generator = get_db()
    db_yielded = next(generator)
    assert db_yielded == db
