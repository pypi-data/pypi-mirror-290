import dataclasses
from zodchy import codex


@dataclasses.dataclass
class HttpEvent(codex.cqea.ResponseEvent):
    def get_content(self) -> dict | None:
        data = dataclasses.asdict(self)
        return {
            'data': data or None
        }

    def get_status_code(self) -> int:
        return 200
