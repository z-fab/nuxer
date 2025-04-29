from datetime import datetime
from typing import Any


def notion_time_to_datetime(notion_time: str | None) -> datetime | None:
    if notion_time is None:
        return None
    return datetime.fromisoformat(notion_time.replace("T", " ").replace("Z", ""))


def notion_rich_text_to_markdown(rich_text: list[dict[str, Any]]) -> str:
    md_parts: list[str] = []

    for block in rich_text:
        # texto puro
        txt: str = block.get("plain_text", "")
        # link (Notion pode usar href ou text.link.url)
        link_info: dict[str, Any] | None = block.get("text", {}).get("link")
        href: str | None = block.get("href") or (link_info.get("url") if link_info else None)
        if href:
            txt = f"[{txt}]({href})"

        anns: dict[str, Any] = block.get("annotations", {})

        # code em primeiro para não interferir nas marcações de estilo
        if anns.get("code"):
            txt = f"`{txt}`"
        if anns.get("bold"):
            txt = f"**{txt}**"
        if anns.get("italic"):
            txt = f"*{txt}*"
        if anns.get("strikethrough"):
            txt = f"~~{txt}~~"

        md_parts.append(txt)

    return "".join(md_parts)
