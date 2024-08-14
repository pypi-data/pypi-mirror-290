"""Circuit module for QuClo."""

from quclo.models import Circuit as CircuitModel


class Circuit:
    """A circuit."""

    def __init__(self, data: str):
        """Initialize the circuit."""
        assert CircuitModel(data=data)
        self.data = data

    def _to_model(self) -> CircuitModel:
        """Return the circuit model."""
        return CircuitModel(data=self.data)

    @staticmethod
    def create(data: str) -> "Circuit":
        """Create a new circuit."""
        circuit = Circuit(data=data)
        # todo submit circuit to API
        return circuit

    @staticmethod
    def get(id: str) -> "Circuit":
        """Get a circuit by ID."""
        # todo get circuit from API
        return Circuit(data='include "stdgates.inc";')

    @staticmethod
    def run(
        data: str | None,
        id: str | None,
    ) -> dict:
        """Run the circuit."""
        if data and id:
            raise ValueError("Cannot specify both data and ID")
        if not data and not id:
            raise ValueError("Either data or ID is required")
        if data:
            return {"data": data}
        return {"id": id}
