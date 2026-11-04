"""Build the ready-to-publish HTML pages from source/book.md.

Run with: python3 -m pip install -r requirements.txt && python3 build.py
The generated pages and assets can be published directly on GitHub Pages.
"""

from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "book.md"
CHAPTERS = ROOT / "chapters"
BOOK_TITLE = "Vihreän meteoriitin mysteeri"
SERIES = "Astroveljesten seikkailut · osa I"
AUTHOR = "Janne K. Jääskeläinen"
DESCRIPTION = (
    "Alexin ja Eelin arki muuttuu, kun taivaalta putoaa mysteerinen vihreä "
    "meteoriitti. Lue Astroveljesten seikkailut verkossa."
)


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def slugify(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def read_book() -> tuple[str, list[dict[str, object]]]:
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    front = re.match(r"\A---\n.*?\n---\n", text, re.S)
    if not front:
        raise ValueError("Markdown export is missing its front matter")
    text = text[front.end():].strip()
    headings = list(re.finditer(r"(?m)^# (.+?)\s*$", text))
    if len(headings) != 25:
        raise ValueError(f"Expected 25 chapters, found {len(headings)}")
    intro = text[: headings[0].start()].strip()
    chapters = []
    for number, heading in enumerate(headings, 1):
        title = heading.group(1).strip()
        end = headings[number].start() if number < len(headings) else len(text)
        body = text[heading.end():end].strip()
        if not body:
            raise ValueError(f"Chapter {number} has no text: {title}")
        chapters.append({
            "number": number,
            "title": title,
            "body": body,
            "filename": f"{number:02d}-{slugify(title)}.html",
            "minutes": max(1, round(len(body.split()) / 230)),
        })
    return intro, chapters


def head(title: str, *, depth: int, description: str = DESCRIPTION) -> str:
    prefix = "../" if depth else ""
    return f"""<!doctype html>
<html lang="fi" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0a1917">
  <meta name="description" content="{escape(description)}">
  <meta property="og:type" content="book">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <title>{escape(title)} · Astroveljekset</title>
  <link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script defer src="{prefix}assets/site.js"></script>
</head>
<body>
<a class="skip-link" href="#main">Siirry sisältöön</a>
"""


def header(*, depth: int, reader: bool = False) -> str:
    prefix = "../" if depth else ""
    toc = ('<button class="nav-button" id="toc-toggle" type="button" '
           'aria-controls="chapter-nav" aria-expanded="false">Sisällys</button>') if reader else ""
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{prefix}index.html" aria-label="Astroveljekset, etusivu">
      <span class="brand-mark" aria-hidden="true">✦</span><span>Astroveljekset</span>
    </a>
    <div class="header-actions">{toc}
      <button class="theme-button" id="theme-toggle" type="button" aria-label="Vaihda vaaleaan teemaan" title="Vaihda teemaa"><span aria-hidden="true">☼</span></button>
    </div>
  </div>
</header>"""


def footer(*, depth: int) -> str:
    prefix = "../" if depth else ""
    return f"""<footer class="site-footer">
  <div class="footer-inner">
    <span>© 2024 {AUTHOR}</span>
    <span><a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a> · <a href="{prefix}index.html">Takaisin sisällykseen</a></span>
  </div>
</footer>"""


def chapter_link(number: int, title: str, filename: str, *, active: bool = False) -> str:
    current = ' aria-current="page"' if active else ""
    num = "Alku" if number == 0 else f"{number:02d}"
    return (f'<a class="sidebar-link{" is-active" if active else ""}" href="{escape(filename)}"{current}>'
            f'<span class="sidebar-number">{num}</span><span>{escape(title)}</span></a>')


def reader_page(number: int, title: str, body: str, chapters: list[dict[str, object]]) -> str:
    entries = [(0, "Lue ensin!", "00-lue-ensin.html")]
    entries += [(int(c["number"]), str(c["title"]), str(c["filename"])) for c in chapters]
    nav = "\n".join(chapter_link(n, t, f, active=n == number) for n, t, f in entries)
    previous = entries[number - 1] if number > 0 else None
    next_one = entries[number + 1] if number + 1 < len(entries) else None
    nav_cards = ""
    if previous:
        nav_cards += (f'<a class="chapter-nav-card" href="{escape(previous[2])}">'
                      f'<span>← Edellinen</span><strong>{escape(previous[1])}</strong></a>')
    if next_one:
        nav_cards += (f'<a class="chapter-nav-card is-next" href="{escape(next_one[2])}">'
                      f'<span>Seuraava →</span><strong>{escape(next_one[1])}</strong></a>')
    eyebrow = "Ennen tarinaa" if number == 0 else f"Luku {number} / {len(chapters)}"
    body_html = markdown.markdown(body, extensions=["extra", "sane_lists"])
    page = head(f"{title} – {BOOK_TITLE}", depth=1)
    page += '<div class="reading-progress" id="reading-progress" aria-hidden="true"></div>'
    page += header(depth=1, reader=True)
    page += '<div class="reader-layout" id="reader-layout">'
    page += '<div class="sidebar-backdrop" id="sidebar-backdrop"></div>'
    page += (f'<aside class="reader-sidebar" id="chapter-nav" aria-label="Kirjan luvut">'
             f'<div class="sidebar-heading"><span>{SERIES}</span><strong>{BOOK_TITLE}</strong></div>'
             f'<nav class="sidebar-chapters">{nav}</nav></aside>')
    page += (f'<main id="main" class="reading-main" data-chapter="{number}">'
             f'<div class="reading-topline"><a href="../index.html">← Sisällys</a>'
             f'<span>{escape(eyebrow)}</span></div>'
             f'<article class="chapter-article"><header class="chapter-heading">'
             f'<p class="eyebrow">{escape(eyebrow)}</p><h1>{escape(title)}</h1>'
             f'<div class="heading-rule" aria-hidden="true"><span>✦</span></div></header>'
             f'<div class="book-prose">{body_html}</div></article>'
             f'<nav class="chapter-next" aria-label="Lukujen välinen siirtyminen">{nav_cards}</nav>'
             f'</main></div>')
    page += footer(depth=1) + "\n</body>\n</html>\n"
    return page


def index_page(intro: str, chapters: list[dict[str, object]]) -> str:
    first_para = intro.split("\n\n", 1)[0]
    intro_html = markdown.markdown(first_para)
    chapter_cards = "\n".join(
        f'<li><a href="chapters/{escape(str(c["filename"]))}">'
        f'<span class="toc-number">{int(c["number"]):02d}</span>'
        f'<span class="toc-name">{escape(str(c["title"]))}</span>'
        f'<span class="toc-time">n. {int(c["minutes"])} min</span>'
        f'<span class="toc-arrow" aria-hidden="true">↗</span></a></li>'
        for c in chapters
    )
    page = head(BOOK_TITLE, depth=0)
    page += header(depth=0)
    page += f"""<main id="main">
  <section class="hero" aria-labelledby="book-title">
    <div class="hero-stars" aria-hidden="true"></div>
    <div class="hero-inner">
      <div class="cover-wrap"><picture><source srcset="assets/cover.webp" type="image/webp"><img class="book-cover" src="assets/cover.png" alt="Vihreän meteoriitin mysteeri -kirjan kansi" width="1600" height="2560" fetchpriority="high"></picture></div>
      <div class="hero-copy">
        <p class="eyebrow">{SERIES}</p>
        <h1 id="book-title">Vihreän meteoriitin <em>mysteeri</em></h1>
        <p class="hero-author">{AUTHOR}</p>
        <div class="hero-description">{intro_html}</div>
        <div class="hero-buttons">
          <a class="button button-primary" href="chapters/00-lue-ensin.html">Aloita lukeminen <span aria-hidden="true">→</span></a>
          <a class="button button-secondary" href="#luvut">Selaa lukuja</a>
        </div>
        <p class="hero-note">Koko kirja luettavissa maksutta · 25 lukua</p>
      </div>
    </div>
  </section>
  <section class="toc-section" id="luvut" aria-labelledby="toc-title">
    <div class="section-heading"><p class="eyebrow">Matka alkaa tästä</p><h2 id="toc-title">Sisällys</h2>
      <p>Valitse luku tai aloita alusta. Lukukohtainen eteneminen tallentuu vain omaan selaimeesi.</p></div>
    <a class="preface-card" href="chapters/00-lue-ensin.html"><span class="toc-number">✦</span><strong>Lue ensin!</strong><span>Ennen tarinaa</span><span aria-hidden="true">↗</span></a>
    <ol class="toc-grid">{chapter_cards}</ol>
  </section>
  <section class="end-note"><span aria-hidden="true">✦</span><p>Jokainen suuri seikkailu alkaa siitä, että joku katsoo taivaalle.</p></section>
</main>"""
    page += footer(depth=0) + "\n</body>\n</html>\n"
    return page


def main() -> None:
    intro, chapters = read_book()
    CHAPTERS.mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(index_page(intro, chapters), encoding="utf-8")
    (CHAPTERS / "00-lue-ensin.html").write_text(
        reader_page(0, "Lue ensin!", intro, chapters), encoding="utf-8"
    )
    for chapter in chapters:
        (CHAPTERS / str(chapter["filename"])).write_text(
            reader_page(int(chapter["number"]), str(chapter["title"]), str(chapter["body"]), chapters),
            encoding="utf-8",
        )
    print(f"Generated 1 landing page, 1 introduction and {len(chapters)} chapters")


if __name__ == "__main__":
    main()
