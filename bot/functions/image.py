from io import BytesIO

from PIL import Image


def image_to_bytes_io(
    image: Image.Image, image_name: str = "image.png"
) -> BytesIO:
    """Converte um objeto Image em bytes."""

    bio = BytesIO()
    image.name = image_name
    image.save(bio, format="PNG")
    bio.seek(0)

    return bio
