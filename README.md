**English** · [中文](README.zh-CN.md)

# Text Diff — prose-first diff for long paragraphs

A single HTML file that compares two texts **word by word / sentence by sentence / character by character**, without breaking them into lines. Built for prose (articles, contracts, emails, translations, Chinese–English mixed documents) where `git diff` only tells you "this whole paragraph changed". It reads `.docx` directly, so two Word drafts can be compared without touching Word.

![Redline view](screenshots/redline-en.png)

Double-click `TextDiff.html`. Nothing to install, no server, no network — the file works offline and can be moved anywhere.

## What it does

- Paste into the two panes, drop a file into either pane, or **Load file** — `.txt` `.md` `.csv` `.json` and **`.docx`**. Differences recompute as you type.
- **Three granularities**
  - Words — English splits on words, **Chinese splits per character**, so a one-character edit marks one character, not the whole paragraph.
  - Sentences — one unit per sentence; good for spotting rewritten sentences.
  - Characters — every character, for typos and IDs.
- **Three views**
  - Redline — one continuous column, deletions struck through in red, insertions underlined in green, paragraph flow preserved.
  - Side by side — two scrolling columns, highlights only, scroll linked.
  - Change list — every change numbered with context; click a row to jump to it.
- **Options**: ignore line breaks/whitespace (on by default — re-wrapped paragraphs do not show as changes), ignore case, ignore punctuation, toggle strikethrough.
- Stats: character counts, characters added/removed, similarity %, and `‹ ›` to walk through every change.
- **Copy redline** gives `[-old-]{+new+}`; **Copy Markdown** gives `~~old~~` / `==new==` (pastes well into Obsidian).
- **Export Word redline** writes a `.docx` containing the diff as *real tracked changes* (`w:ins` / `w:del`, author "Text Diff"), so Word shows Review → All Markup and the reviewer can accept or reject each edit. The package is assembled in the page (ZIP writer + `word/document.xml`), nothing is uploaded.
- Last session's texts and settings are restored from local storage; `Clear` removes them.

## Keyboard

| Key | Action |
| --- | --- |
| `Ctrl`+`Enter` | compare now |
| `Alt`+`←` / `Alt`+`→` | previous / next change |

## How .docx is read

A `.docx` is a ZIP of XML. The tool finds `word/document.xml` through the ZIP central directory, inflates it with the browser's own `DecompressionStream`, and pulls text out of the WordprocessingML: paragraphs, manual line breaks, tabs, table rows (one line per row, cells separated by tabs), text inside content controls. Formatting is deliberately dropped — only wording is compared. Tracked deletions (`w:del`) are skipped, so a Word document with pending changes is read as its "after" state.

## Exporting a Word redline

`Export .docx` builds the file in the page: a ZIP writer (stored entries, CRC32) plus three parts — `[Content_Types].xml`, `_rels/.rels` and `word/document.xml` — where deleted text sits in `<w:del><w:r><w:delText>`, inserted text in `<w:ins><w:r><w:t>`, both stamped with an author and a date. Word opens it as an ordinary document with tracked changes; `Review → All Markup` shows the marks and `Accept All` collapses it to the new version.

Two honest caveats: paragraph *marks* are not tracked (a deleted line break does not appear as a struck paragraph mark), and the exported file carries no styling beyond a default A4 page and 1.15 line spacing.

## Limits

- `.pdf` and legacy `.doc` are refused with a message (`.doc` → save as `.docx`; PDF → copy the text).
- Formatting, comments, footnotes, headers/footers and images are not compared.
- Comparing two *unrelated* long documents is expensive for any diff algorithm; past ~10k characters the tool stops aligning words, marks the block as replaced and says so ("Too different — compared as whole blocks") instead of freezing.
- Storage is per browser profile and per machine (local storage), not a synced cloud.

## Rebuilding

`TextDiff.html` is generated: `build.py` inlines `src/diff.min.js` (jsdiff 5.2.0, MIT) into `src/app.html`.

```
python3 build.py     # rewrites TextDiff.html
```

Keep `src/` and `build.py` to change anything; the shipped HTML is self-contained and can be shared on its own.
