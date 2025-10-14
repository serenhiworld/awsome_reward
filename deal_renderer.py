"""Utilities for selecting and rendering real daily deals."""
from __future__ import annotations

import re
from datetime import datetime
from textwrap import dedent, indent
from typing import Any, Dict, Iterable, List, Sequence, Tuple
from urllib.parse import urlparse

REQUIRED_REAL_DEALS = 6

_BLOCKED_DOMAINS = {
    "latestfreestuff.co.uk",
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "youtube.com",
}

_DEALS_SECTION_PATTERN = re.compile(
    r"[ \t]*<section[^>]*id=[\"']deals[\"'][^>]*>.*?</section>",
    re.IGNORECASE | re.DOTALL,
)
_BENEFITS_SECTION_PATTERN = re.compile(
    r"<section[^>]*id=[\"']benefits[\"'][^>]*>",
    re.IGNORECASE,
)

Deal = Dict[str, Any]


def is_real_deal_link(url: Any) -> bool:
    """Return True when the url is an external, non-blocked link."""
    if not isinstance(url, str):
        return False

    normalized = url.strip()
    if not normalized or not normalized.lower().startswith("http"):
        return False

    hostname = urlparse(normalized).netloc.lower()
    return not any(blocked in hostname for blocked in _BLOCKED_DOMAINS)


def select_real_deals(
    deals: Iterable[Deal],
    required_count: int = REQUIRED_REAL_DEALS,
) -> Tuple[List[Deal], bool, int]:
    """Filter and normalise real deals.

    Returns a tuple ``(selected_deals, meets_requirement, total_real_count)``.
    ``selected_deals`` always contains at most ``required_count`` items.
    """
    real_deals: List[Deal] = []

    for deal in deals or []:
        if not isinstance(deal, dict):
            continue

        link = deal.get("url") or deal.get("claim_url") or deal.get("source_url")
        if not is_real_deal_link(link):
            continue

        normalized = dict(deal)
        normalized["url"] = link.strip()
        real_deals.append(normalized)

    total_real = len(real_deals)
    meets_requirement = total_real >= required_count
    return real_deals[:required_count], meets_requirement, total_real


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _render_deal_item(deal: Deal) -> str:
    title = (deal.get("title_zh") or deal.get("title") or "").strip()
    description = (deal.get("description_zh") or deal.get("description") or "").strip()
    description = _truncate(description, 160)

    url = deal.get("url", "#")
    date = deal.get("date", "")
    image = deal.get("image", "")

    try:
        domain = urlparse(url).netloc or "未知域名"
    except Exception:
        domain = "未知域名"

    image_html = ""
    if image:
        image_html = dedent(
            f"""
            <div class=\"deal-image\">
                <img src=\"{image}\" alt=\"优惠图片\" loading=\"lazy\">
            </div>
            """
        ).strip()

    item_html = dedent(
        f"""
        <div class=\"deal-item featured-deal\">
            <div class=\"deal-badge\">✅ 真实链接</div>
            {image_html if image_html else ''}
            <h3>{title}</h3>
            <p>{description}</p>
            <div class=\"deal-meta\">
                <span class=\"date\">📅 {date}</span>
                <span class=\"domain\">🌐 {domain}</span>
                <a href=\"{url}\" target=\"_blank\" class=\"deal-link btn-primary\">🎁 立即领取</a>
            </div>
        </div>
        """
    ).strip()

    # remove potential blank line placeholder if no image
    item_lines = [line for line in item_html.splitlines() if line.strip()]
    cleaned_item = "\n".join(item_lines)
    return indent(cleaned_item, " " * 20)


def render_deals_section(
    deals: Sequence[Deal],
    timestamp: datetime | None = None,
) -> Tuple[str, Dict[str, Any]]:
    """Render the deals section HTML for the supplied deals."""
    timestamp = timestamp or datetime.now()
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    header_text = f"🎁 今日英国优惠精选 - {len(deals)} 个真实商家优惠"
    update_text = f"🕒 最新更新: {formatted_time} | ✅ 提取真实优惠链接"

    if deals:
        deal_items = [_render_deal_item(deal) for deal in deals]
    else:
        deal_items = [" " * 20 + '<div class="deal-item">暂无最新优惠，敬请关注！</div>']

    items_block = "\n\n".join(deal_items)

    section_lines = [
        "    <section id=\"deals\" class=\"daily-deals\">",
        "        <div class=\"container\">",
        "            <div class=\"daily-deals-section\">",
        f"                <h2>{header_text}</h2>",
        f"                <p class=\"update-time\">{update_text}</p>",
        "                <div class=\"deals-container\">",
        items_block,
        "                </div>",
        "            </div>",
        "        </div>",
        "    </section>",
    ]

    section_html = "\n".join(section_lines)
    metadata = {
        "header_text": header_text,
        "update_text": update_text,
        "timestamp": timestamp,
        "deal_count": len(deals),
    }
    return section_html, metadata


def replace_deals_section(document: str, section_html: str) -> Tuple[str, str]:
    """Replace or insert the deals section within the provided HTML document.

    Returns a tuple ``(updated_document, action)`` where ``action`` indicates
    whether the section was ``replaced``, ``inserted`` before the benefits block,
    or ``appended`` to the end of the file.
    """
    if not section_html.endswith("\n"):
        section_html = section_html + "\n"

    updated, count = _DEALS_SECTION_PATTERN.subn(section_html, document, count=1)
    if count:
        return updated, "replaced"

    benefits_match = _BENEFITS_SECTION_PATTERN.search(document)
    if benefits_match:
        before = document[: benefits_match.start()].rstrip()
        after = document[benefits_match.start():]
        separator_before = "\n\n" if before else ""
        separator_after = "" if after.startswith("\n") else "\n"
        new_document = f"{before}{separator_before}{section_html}{separator_after}{after}"
        return new_document, "inserted"

    trimmed = document.rstrip()
    separator = "\n\n" if trimmed else ""
    new_document = f"{trimmed}{separator}{section_html}"
    return new_document, "appended"
