from typing import Tuple

def paginate(page: int | None, size: int | None, max_size: int = 100) -> Tuple[int, int]:
    """Sanitize page & size providing defaults and an upper bound."""
    p = page or 1
    s = size or 10
    if p < 1:
        p = 1
    if s < 1:
        s = 1
    if s > max_size:
        s = max_size
    return p, s
