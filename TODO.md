# TODO.md

This file outlines improvements and technical considerations that would be implemented given more time, scope, or production-level requirements.

---

## Interface Design

- [ ] Define a formal Python interface (e.g., `BasePdfRecognizer` or use `Protocol` from `typing`)
- [ ] Specify key method signatures:  
  - `recognize(pdf_bytes: bytes) -> RecognizedDocument`
  - `build_recognized_document(...)`
- [ ] Make `PDFRecognizer` conform explicitly to the interface
- [ ] Prepare structure for alternative implementations (e.g., `AzurePdfRecognizer`, `PaddleOcrRecognizer`)
- [ ] Optional: define a `PdfRecognizerConfig` object to manage settings cleanly
- [ ] Consider using a factory or registration pattern to load recognizers dynamically

---

## OCR Optimization

- [x] Removed `--force-ocr` by default to significantly reduce processing time and preserve original text layer where possible.
- [ ] Add `force_ocr: bool` parameter to the `recognize(...)` method to allow manual override when full OCR is needed.
- [ ] Detect pages with corrupted or unreadable text (e.g., lots of `cid:` symbols) and apply OCR selectively.
- [ ] Log OCR execution time separately from total processing time (e.g., `OCR: 11.5s, Parsing: 2.1s`).

---

## Image Extraction

- [x] Image extraction logic has been modularized into a private method `_extract_images(...)`.
- [x] The `recognize(...)` method accepts an `extract_images: bool` flag to toggle image processing.
- [ ] Filter out small decorative or UI elements by size (e.g., skip images smaller than 100x100 pixels).
- [ ] Ignore full-page images that likely represent background or template layers.
- [ ] Add extraction mode (e.g., `extract_images_mode = 'simple' | 'strict'`) for more control.

---

## Text Parsing

- [ ] In tagged PDFs, `pdfplumber` may extract text as `(cid:xxx)` glyphs — these are unreadable. Add post-checks for such cases.
- [ ] If over 50% of page text contains `cid:` or invalid characters, fallback to OCR for that page.
- [ ] Allow manual page-level OCR override by passing a list of page indices.
- [ ] Optimize text collection by avoiding duplicate `page.extract_text()` calls.

---

## Table Extraction

- [ ] Add support for structured table extraction using `page.extract_table()` or `extract_tables()`.
- [ ] Export detected tables to markdown or CSV-compatible formats.
- [ ] Extend `RecognizedDocument` with a `tables_by_page` field: `dict[int, list[list[str]]]`.
- [ ] Add a flag `extract_tables: bool` to toggle table parsing.

---

## Usability & Output Improvements

- [ ] Improve `main.py` output formatting: clean key listing, truncate long text more consistently, prettify logging.
- [ ] Show OCR vs non-OCR page stats, and total image count.
- [ ] Add an optional `--log-to-file` flag to persist processing results.

---

## Architecture & Maintainability

- [x] Code is modular and follows the proposed project structure: `models.py`, `recognizer.py`, `main.py`.
- [ ] Move user-facing configuration to `.env` or a YAML config file.
- [ ] Add a CLI interface (e.g., using `argparse` or `typer`) to run with custom paths, flags, and modes.
- [ ] Add unit tests to cover key logic (recognizer, image filtering, text fallback strategy).

---

## Further Exploration

- [ ] Implement error handling for OCR subprocesses — catch `ocrmypdf` crashes and continue gracefully.
- [ ] Improve fallback strategies for edge-case PDFs (encrypted, password-protected, malformed layers, etc.).

---

## Performance Notes

- Test file (34 pages):
  - `--force-ocr`: ~140 seconds
  - Without forced OCR + image extraction disabled: ~13 seconds
- Image extraction adds substantial overhead due to large number of decorative objects in presentation-style PDFs.

---

