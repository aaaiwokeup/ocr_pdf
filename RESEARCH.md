# OCR Methods Researched & Evaluated

---

## 1. Azure Document Intelligence (Form Recognizer)

**Model:** `prebuilt-document`  
**Interface:** Official Python SDK

### Strengths:
- Automatically detects semantic roles (`title`, `paragraph`, `sectionHeading`, `listItem`)
- Parses tables as structured objects (`row_index`, `column_index`)
- Returns style metadata: `is_bold`, `font_size`, `boundingRegions`
- High performance: <15 seconds for a 2-page PDF
- Fully compatible with Python 3.13

### Limitations:
- Free tier (F0) processes only the **first 2 pages** of each PDF
- Skips image-based pages (does not run OCR automatically)
- Sometimes misinterprets layout in presentation-style PDFs
- Requires fallback for scanned or image-only documents

### Conclusion:
Azure is excellent for structured, text-layered PDFs. However, it struggles with scanned/image-based pages and is restricted on the free tier.

---

## 2. PaddleOCR

**Type:** Open-source OCR system focused on image recognition  
**Tested through:** `PPStructure` for PDF parsing

### Strengths:
- Very good accuracy on images
- Supports table structure extraction
- Actively developed and extensible

### Issues:
- Unstable installation on Windows (especially with non-ASCII paths)
- Sparse documentation for direct PDF handling
- Integration issues with Python 3.13

### Conclusion:
Promising but not stable in production environments. Deferred due to technical complexity and lack of compatibility.

---

## 3. Tesseract OCR

**Type:** Classical OCR engine  
**Interface:** Used via `pytesseract`, `pdf2image`, or `OCRmyPDF`

### Strengths:
- Works directly with scanned/image-based documents
- Widely supported across platforms
- Available via CLI and Python bindings
- Unicode-compatible (supports Cyrillic)

### Weaknesses:
- No structure or layout detection (no roles, no styles)
- Tables are extracted as unstructured plain text
- Requires prior conversion of PDFs into images

### Conclusion:
Great fallback for image-based content. Ideal complement to Azure in hybrid pipelines.

---

## 4. OCRmyPDF (via CLI)

**Type:** Combined solution — PDF → OCR → searchable PDF  
**Interface:** Called via `subprocess`, parsed with `pdfplumber` or `fitz`

### Strengths:
- Fully processes scanned documents and returns searchable PDF
- Runs outside Python interpreter — no conflict with Python 3.13
- Output is a real PDF with embedded text layer
- Easily integrates with other OCR backends

### Weaknesses:
- Requires temporary file I/O (read/write)
- Doesn't preserve semantic structure (headings, lists, tables)

### Conclusion:
Best all-around option for complex PDFs with scans. Covers Azure’s blind spots and integrates cleanly with existing parsing tools.

---
