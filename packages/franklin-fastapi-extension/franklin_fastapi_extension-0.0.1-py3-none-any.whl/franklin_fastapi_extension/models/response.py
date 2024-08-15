from dataclasses import dataclass, asdict


@dataclass
class Response:
    node: any
    errors: list

    def __init__(self, node=None, errors=None):
        self.node = node
        self.errors = errors

    def dict(self):
        return asdict(self)
