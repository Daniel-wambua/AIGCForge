import hashlib
import mimetypes
from PIL import Image


def get_file_hash(filepath, algo="sha256"):
    """
    Compute file hash (default: sha256)
    """
    h = hashlib.new(algo)
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def get_mime_type(filepath):
    """
    Guess MIME type using standard library and Pillow fallback for images.
    """
    mime, _ = mimetypes.guess_type(filepath)
    if mime:
        return mime
    # Fallback: try Pillow for images
    try:
        with Image.open(filepath) as img:
            fmt = img.format.lower()
            return f"image/{fmt}"
    except Exception:
        return "application/octet-stream"
