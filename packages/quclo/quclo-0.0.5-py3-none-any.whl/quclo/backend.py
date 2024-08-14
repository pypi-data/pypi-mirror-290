"""Backend module for QuClo."""

from quclo.models import Backend as BackendModel


class Backend:
    """A backend."""

    def __init__(self, name: str):
        """Initialize the backend."""
        assert BackendModel(name=name)
        self.name = name

    def _to_model(self) -> BackendModel:
        """Return the backend model."""
        return BackendModel(name=self.name)
