import asyncio
import time

from pathlib import Path

from models import RecognizedDocument
from recognizer import PDFRecognizer

pdf_recognizer = PDFRecognizer()
output_truncate = 500

def run(pdf_path, extract_images):
    with open(pdf_path, 'rb') as raw_pdf:
        pdf_bytes = raw_pdf.read()
        start_time = time.time()

        try:
            result = asyncio.run(pdf_recognizer.recognize(pdf_bytes=pdf_bytes, extract_images=extract_images))
            print('--- PDF START ---\n\n',
                  result.text[:output_truncate],
                  f'\n\n...output truncated to {output_truncate} symbols.\n\n',
                  '--- PDF END ---\n')

            output_images = Path.cwd() / "output_images"
            output_images.mkdir(exist_ok=True)

            for key, value in result.image_bytes_by_name.items():
                output_images_path = Path(output_images) / f'{key}.png'
                with open(output_images_path, 'wb') as oip:
                    oip.write(value)

            print(f'Image extracted: {len(result.image_bytes_by_name)}\n'
                  f'Keys: {", ".join(result.image_bytes_by_name.keys()) if len(result.image_bytes_by_name) > 0 else "0"}')

        except Exception as e:
            print(f'Error during PDF processing: {e}')

        end_time = time.time()
        duration = end_time - start_time
        print(f'Time duration for PDF processing: {duration:.4f} seconds')


if __name__ == "__main__":
    run('samples/2_investor presentation.pdf', extract_images=False)
