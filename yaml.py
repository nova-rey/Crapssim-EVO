from __future__ import annotations

import json
from typing import IO, Any, Optional


def safe_dump(data: Any, stream: Optional[IO[str]] = None, **kwargs: Any) -> str:
    text = json.dumps(data, **kwargs)
    if stream is None:
        return text
    stream.write(text)
    return text


def safe_load(stream: Any) -> Any:
    if hasattr(stream, "read"):
        content = stream.read()
    else:
        content = stream
    if content is None or content == "":
        return None
    return json.loads(content)
