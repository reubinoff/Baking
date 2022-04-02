
IMAGES = [
    "image/vnd.dwg",
    "image/x-xcf",
    "image/jpeg",
    "image/jpx",
    "image/png",
    "image/gif",
    "image/webp",
    "image/x-canon-cr2",
    "image/tiff",
    "image/bmp",
    "image/vnd.ms-photo",
    'image/vnd.adobe.photoshop',
    "image/x-icon",
    "image/heic"
]


def is_image(file_type: str) -> bool:
    return file_type in IMAGES
