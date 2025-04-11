from dataclasses import dataclass


@dataclass
class RecognizedDocument:
    text: str
    image_bytes_by_name: dict[str, bytes]
