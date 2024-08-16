from os import getcwd
from os import path as os_path
from typing import Dict
from uuid import uuid4

from click import Path, argument, group, option
from loguru import logger

from .epub import epub
from .m4a import m4a
from .mov import mov
from .mp3 import mp3
from .mp4 import mp4
from .png import convert_image
from .txt import txt
from .webm import webm


@group(name="conv", help="Convert a file")
def conv():
    pass


@conv.command(help="List all available conversions")
def list():
    logger.debug("conv list")

    print("Available conversions:")
    print("  text")
    print("    txt -> mp3")
    print("  book")
    print("    epub -> pdf")
    print("  image")
    print("    jpg, jpeg, webp -> png")
    print("    jpg, jpeg, webp, png -> mp4")
    print("  audio")
    print("    m4a -> wav, mp3")
    print("    mp3 -> wav, m4a")
    print("  video")
    print("    mp4,webm,mov -> mp3")
    return


@conv.command(help="Convert text into another format")
@option("-v", "--value", type=str, required=True, prompt=True, help="Text to convert")
@option("-f", "--format", type=str, required=True, prompt=True, help="Format to convert to (e.g. mp3)")
@option(
    "-o",
    "--options",
    type=str,
    required=False,
    default="voice=echo",
    help="Options to use for conversion (e.g. voice=alloy)",
)
def text(value: str, format: str, options: str):
    logger.debug("conv text")

    dst_format = format
    dst_path = f"{str(uuid4())}.{dst_format}"

    logger.debug(f"Converting {value} to {format} at ./{dst_path}")

    opts: Dict[str, str] = {k: v.lower() for k, v in [o.split("=") for o in options.split(",")]}

    txt(value, dst_path, opts)
    return


@conv.command(help="Convert a book into another format")
@option("-p", "--path", type=str, required=True, prompt=True, help="Path to the book file (e.g. /path/to/file)")
@option("-f", "--format", type=str, required=True, prompt=True, help="Format to convert to (e.g. pdf)")
def book(path: str, format: str) -> None:
    logger.debug("conv book")

    if not os_path.isabs(path):
        path = os_path.join(getcwd(), path)

    if not os_path.exists(path):
        print(f"Book {path} does not exist")
        return

    splits = path.split(".")

    src_format = splits[-1]
    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    logger.debug(f"Converting {src_path} to {dst_path}")

    if src_format == "epub":
        epub(src_path, dst_path)
    else:
        logger.error(f"Unsupported file {src_format}")
    return


@conv.command(help="Convert a video to another format")
@option("-p", "--path", type=str, required=True, prompt=True, help="Path to the video file (e.g. /path/to/file)")
@option("-f", "--format", type=str, required=True, prompt=True, help="Format to convert to (e.g. mp3)")
def video(path: str, format: str):
    logger.debug("conv video")

    if not os_path.isabs(path):
        path = os_path.join(getcwd(), path)

    if not os_path.exists(path):
        print(f"Video {path} does not exist")
        return

    splits = path.split(".")

    src_format = splits[-1]
    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    logger.debug(f"Converting {src_path} to {dst_path}")

    if src_format == "mp4":
        mp4(src_path, dst_path)
    elif src_format == "webm":
        webm(src_path, dst_path)
    elif src_format == "mov":
        mov(src_path, dst_path)
    else:
        logger.error(f"Unsupported file {src_format}")
    return


@conv.command(help="Convert an audio to another format")
@option("-p", "--path", type=str, required=True, prompt=True, help="Path to the audio file (e.g. /path/to/file)")
@option("-f", "--format", type=str, required=True, prompt=True, help="Format to convert to (e.g. wav)")
def audio(path: str, format: str):
    logger.debug("conv audio")

    if not os_path.isabs(path):
        path = os_path.join(getcwd(), path)

    if not os_path.exists(path):
        print(f"Audio {path} does not exist")
        return

    splits = path.split(".")

    src_format = splits[-1]
    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    logger.debug(f"Converting {src_path} to {dst_path}")

    if src_format == "m4a":
        m4a(src_path, dst_path)
    elif src_format == "mp3":
        mp3(src_path, dst_path)
    else:
        logger.error(f"Unsupported file {src_format}")
    return


@conv.command(help="Convert an image or multiple images into another format")
@option("-f", "--format", type=str, required=True, prompt=True, help="Format to convert to (e.g. jpg, mp4)")
@option("-d", "--duration", type=int, default=0, help="Duration of output file in seconds (e.g. 30)")
@argument("paths", nargs=-1, type=Path(exists=True), required=True)
def image(format: str, duration: int, paths: tuple[str, ...]):
    logger.debug("conv image")

    for input_path in paths:
        if not os_path.isabs(input_path):
            input_path = os_path.join(getcwd(), input_path)

        if not os_path.exists(input_path):
            print(f"Image {input_path} does not exist")
            continue

        src_filename = os_path.splitext(os_path.basename(input_path))[0]
        src_filepath = os_path.dirname(input_path)
        dst_path = f"{src_filepath}/{src_filename}.{format}"

        logger.debug(f"Converting {input_path} to {dst_path}")

        convert_image(input_path, dst_path, format, duration)

    logger.info(f"Converted {len(paths)} image(s)")
