import subprocess
import tempfile
import pdfplumber
import io

from pathlib import Path
from models import RecognizedDocument


class PDFRecognizer:
    """
    Main OCR class
    """
    def perform_ocr(self, input_path, output_path):
        subprocess.run(["ocrmypdf", "--skip-text", str(input_path), str(output_path)], check=True)

    def _extract_images(self, page, image_bytes_by_name):
        if not page.images:
            return

        for image_index, image in enumerate(page.images):
            buffer = io.BytesIO()

            x0, top, x1, bottom = image['x0'], image['top'], image['x1'], image['bottom']
            page_image = page.to_image(resolution=150)
            pillow_img = page_image.original
            cropped_img = pillow_img.crop((x0, top, x1, bottom))
            cropped_img.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            image_key = f"page_{page.page_number}_img_{image_index}"

            image_bytes_by_name[image_key] = image_bytes

    async def extract_text_and_image_from_pdf(self, output_path, extract_images):
        image_bytes_by_name = {}
        with pdfplumber.open(output_path) as pdf:
            raw_text = []

            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    raw_text.append(text)

                if extract_images:
                    self._extract_images(page, image_bytes_by_name)

            text = ''.join(raw_text)
            return text, image_bytes_by_name

    def build_recognized_document(self, text, image_bytes_by_name):
        return RecognizedDocument(text, image_bytes_by_name)

    async def recognize(self, pdf_bytes: bytes, extract_images: bool = True) -> RecognizedDocument:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.pdf"
            output_path = Path(tmpdir) / "output.pdf"

            input_path.write_bytes(pdf_bytes)

            self.perform_ocr(input_path, output_path)

            text, image_bytes_by_name = await self.extract_text_and_image_from_pdf(output_path, extract_images)

            return self.build_recognized_document(text, image_bytes_by_name)
