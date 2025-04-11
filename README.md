# PDF OCR Text Extractor

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd pdf_to_text
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Install system dependencies (required for ocrmypdf)
Ubuntu/Debian
```bash
sudo apt update
sudo apt install ocrmypdf tesseract-ocr ghostscript pngquant unpaper -y
```
macOS (with Homebrew)
```bash
brew install ocrmypdf tesseract ghostscript pngquant unpaper
```
Windows

- Install [Ghostscript 64-bit](https://ghostscript.com/releases/gsdnld.html)

- Install [Tesseract 64-bit](https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0)

Make sure you added them to your system PATH after -> [Guide](https://www.computerhope.com/issues/ch000549.htm#dospath)

---

## Usage
Run the script on a target PDF:
```bash
python main.py
```
You can configure the file path and options in main.py:
```python
run('samples/<your_pdf_file>.pdf', extract_images=True)
```

---

## Output
- Extracted text is printed in the console (truncated by default)
- Images (if enabled) are saved in the output_images/ directory

Example output:
```markdown
--- PDF START ---

Cleaned and extracted text here...

--- PDF END ---
Image extracted: 4
Time duration for PDF processing: 12.48 seconds
```

---

## Configuration Options
Configuration is passed via parameters to the recognize(...) method in PDFRecognizer:

- `extract_images=True | False` — toggle image extraction

- (*Planned*) `force_ocr=True | False` — force OCR even if text layer exists

- (*Planned*) `extract_tables=True | False` — enable table detection

---

## Project Structure
```
pdf_to_text/
├── main.py            # Entry point
├── recognizer.py      # Main OCR class (PDFRecognizer)
├── models.py          # Data models
├── requirements.txt   # Python dependencies
├── samples/           # Sample PDFs
├── output_images/     # Extracted images (auto-created)
├── TODO.md            # Known limitations / future improvements
├── RESEARCH.md        # Reasearch results
└── README.md          # You’re here
```

---

## Notes
- Extraction quality varies depending on PDF encoding.

- Tagged PDFs or those using CID fonts may not return readable text unless OCR is forced.

- In presentation-style PDFs, many background elements may be interpreted as images. Filtering strategies are in development (see TODO.md).

---