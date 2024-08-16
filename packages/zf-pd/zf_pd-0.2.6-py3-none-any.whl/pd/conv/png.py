from loguru import logger
from moviepy.editor import ImageClip
from PIL import Image


def convert_image(src: str, dst: str, format: str, duration: int = 0) -> None:
    dst_format = format.lower()

    if dst_format == "mp4":
        image_to_mp4(src, dst, duration)
    elif dst_format in ["jpg", "jpeg", "png", "webp", "gif"]:
        image_to_image(src, dst, dst_format)
    else:
        logger.error(f"Unsupported format {dst_format}")


def image_to_image(src: str, dst: str, format: str) -> None:
    with Image.open(src) as image:
        image.save(dst, format.upper())
    logger.debug(f"Converted {src} to {dst}")


def image_to_mp4(src: str, dst: str, duration: int) -> None:
    logger.debug(f"Converting {src} to {dst} of {duration} seconds")
    clip = ImageClip(src, duration=duration)
    clip.write_videofile(dst, fps=24, codec="libx264")
