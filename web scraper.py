import re
from pathlib import Path

html = Path("readthrough.htm").read_text(encoding="utf-8", errors="ignore")

pattern = re.compile(r'href=["\'](https?://(?:www\.)?x\.com/[^\s"\'<>)\]}]+)["\']', re.IGNORECASE)
links = [m.group(1) for m in pattern.finditer(html)]

print("\n".join(dict.fromkeys(links)))
