"""Execution module for QuClo."""

import requests
from quclo.utils import QUCLO_API_URL
from quclo.models import Priority, Execution as ExecutionModel
from quclo.circuit import Circuit
from quclo.backend import Backend


class Execution:
    """An execution."""

    def __init__(
        self,
        circuit: Circuit,
        backend: Backend | None = None,
        priority: Priority | None = None,
    ):
        """Initialize the circuit."""
        assert ExecutionModel(
            circuit=circuit._to_model(),
            backend=backend._to_model() if backend else None,
            priority=priority if priority else None,
        )
        self.circuit = circuit
        self.backend = backend
        self.priority = priority

    def _to_model(self) -> ExecutionModel:
        """Return the execution model."""
        return ExecutionModel(
            circuit=self.circuit._to_model(),
            backend=self.backend._to_model() if self.backend else None,
            priority=self.priority if self.priority else None,
        )

    def run(self) -> dict:
        """Run the circuit."""
        json = self._to_model().model_dump(exclude_none=True)
        return json
