class ZettelkastenError(Exception):
    """Basisklasse für alle Exceptions in Zettelkasten."""
    pass

class KeyNotFoundError(ZettelkastenError):
    """Wird geworfen, wenn ein abgefragter Schlüssel nicht existiert."""
    def __init__(self, key: str):
        super().__init__(f"Schlüssel '{key}' wurde in der Datenbank nicht gefunden.")
        self.key = key

class StorageCorruptedError(ZettelkastenError):
    """Wird geworfen, wenn die Speicherdatei nicht gelesen werden kann."""
    pass

class LockTimeoutError(ZettelkastenError):
    """Wird geworfen, wenn eine Dateisperre nicht erlangt werden kann."""
    pass
