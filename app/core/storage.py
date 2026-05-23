"""Simple storage abstraction for annotated images."""

from pathlib import Path


class LocalStorage:
    """Local fallback storage used for development/tests."""

    def __init__(self, root: str = "storage") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, key: str, content: bytes) -> str:
        """Save content and return key."""
        target = self.root / key
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return key

    def read(self, key: str) -> bytes:
        """Read stored object by key."""
        return (self.root / key).read_bytes()


storage = LocalStorage()
