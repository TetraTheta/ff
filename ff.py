import argparse
import subprocess
import sys
from os import getcwd
from typing import List, Tuple, Final
from pathlib import Path


subprocess.run("color", shell=True, capture_output=False, check=False)  # Hack: Enable ANSI/VT100 on Command Prompt

FFMPEG_PATH: Final[str] = "C:\\CustomExecutables\\ffmpeg.exe"

AUDIO_EXTENSIONS: Tuple[str, ...] = ("*.aac", "*.flac", "*.mp3", "*.oga", "*.ogg", "*.opus", "*.vorbis", "*.wav", "*.wma")
IMAGE_EXTENSIONS: Tuple[str, ...] = ("*.bmp", "*.gif", "*.jpeg", "*.jpg", "*.png", "*.webp")
VIDEO_EXTENSIONS: Tuple[str, ...] = ("*.avi", "*.mkv", "*.mp4", "*.mov", "*.wmv", "*.webm", "*.ogv", "*.opus")
SUBCMD_LIST: Tuple[str, ...] = ("gi", "mp3", "webm", "webp", "webpa")
WEBP_PRESETS: Tuple[str, ...] = ("default", "drawing", "icon", "none", "photo", "picture", "text")

# Description & Help text because I'm lazy
DESC_FF: Final[str] = "A collection of FFmpeg commands in a single script\nuse '--help' with each subcommand for its usage."
DESC_GI: Final[str] = "Genshin Impact screenshot processor\nTruncate the image and convert it to a WebP image with a width of 1280px."
DESC_MP3: Final[str] = "Convert audio/video files to MP3 audio format"
DESC_WEBM: Final[str] = "Convert video files to WebM video format"
DESC_WEBP: Final[str] = "Convert image files to WebP image format"
DESC_WEBPA: Final[str] = "Convert video files to WebP Animated image format"
HELP_GI_TYPE: Final[str] = "Type of screenshot truncation. Truncation is done before image resizing.\n0 = Do not truncate\n1 = Prune 240px from the bottom\n2 = Prune 300px from the bottom\n3 = Prune 400px from the bottom\nDefault: '%(default)s'"
HELP_MP3_BITRATE: Final[str] = "Bitrate of the output MP3 audio.\nDefault: '%(default)s' (kbps)"
HELP_MP3_SAMPLE: Final[str] = "Samplerate of the output MP3 audio.\nDefault: '%(default)s'"
HELP_TARGET: Final[str] = "File or directory to process.\nDefault '%(default)s' (Current directory)"
HELP_WEBM_1_PASS: Final[str] = "Convert with 1-pass conversion"
HELP_WEBM_2_PASS: Final[str] = "Convert with 2-pass conversion"
HELP_WEBM_FPS: Final[str] = "FPS of the output WebM video.\nIf omitted, it will follow the source video's FPS."
HELP_WEBM_HEIGHT: Final[str] = "Height of the output WebM video.\nDefault: '%(default)s' (Keep original ratio)"
HELP_WEBM_QUALITY: Final[str] = "Quality of the WebM video.\n15 = Best (for 2160p)\n37 = Worst (for 240p)\nDefault: '%(default)s'"
HELP_WEBM_WIDTH: Final[str] = "Width of the output WebM video.\nDefault: '%(default)s' (px)"
HELP_WEBP_COMPRESSION: Final[str] = "Compression level of the output WebP image.\nDefault: '%(default)s' (Max compression level)"
HELP_WEBP_HEIGHT: Final[str] = "Height of the output WebP image.\nDefault: '%(default)s' (Keep original ratio)"
HELP_WEBP_LOSSLESS: Final[str] = "Convert to a lossless WebP image.\nCannot be used with '--lossy'"
HELP_WEBP_LOSSY: Final[str] = "Convert to a lossy WebP image.\nCannot be used with '--lossless'"
HELP_WEBP_PRESET: Final[str] = "Preset of WebP.\nDefault: '%(default)s'"
HELP_WEBP_QUALITY: Final[str] = "Quality of the WebP image.\nDefault: '%(default)s'"
HELP_WEBP_WIDTH: Final[str] = "Width of the output WebP image.\nDefault: '%(default)s'px (Original width)"
HELP_WEBPA_FPS: Final[str] = "FPS of the output WebP image.\nDefault: '%(default)s'"
HELP_WEBPA_LOOP: Final[str] = "Loop the output WebP image."
HELP_WEBPA_NO_LOOP: Final[str] = "Do not loop the output WebP image."

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=DESC_FF)
subparser = parser.add_subparsers(dest="subcmd")
# Global parameter cannot be used, so I've included same lines across every subcommands
# Subcommand: gi - Genshin Impact screenshot processor
parser_gi = subparser.add_parser("gi", formatter_class=argparse.RawTextHelpFormatter, description=DESC_GI)
parser_gi.add_argument("--height", dest="height", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBP_HEIGHT, default=-1)
parser_gi.add_argument("--lossless", dest="lossless", action="store_true", help=HELP_WEBP_LOSSLESS, default=True)
parser_gi.add_argument("--lossy", dest="lossless", action="store_false", help=HELP_WEBP_LOSSY)
parser_gi.add_argument("--preset", dest="preset", type=str, choices=WEBP_PRESETS, metavar="<default|drawing|icon|none|photo|picture|text>", help=HELP_WEBP_PRESET, default="picture")
parser_gi.add_argument("--quality", dest="quality", type=int, choices=range(1, 101), metavar="<1..100>", help=HELP_WEBP_QUALITY, default=80)
parser_gi.add_argument("--type", dest="giType", type=int, choices=range(0, 4), metavar="<0..3>", help=HELP_GI_TYPE, default=0)
parser_gi.add_argument("--width", dest="width", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBP_WIDTH, default=1280)
parser_gi.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")
# Subcommand: mp3 - MP3
parser_mp3 = subparser.add_parser("mp3", formatter_class=argparse.RawTextHelpFormatter, description=DESC_MP3)
parser_mp3.add_argument("--bitrate", dest="bitrate", type=int, choices=range(1, 321), metavar="<1..320>", help=HELP_MP3_BITRATE, default=320)
parser_mp3.add_argument("--samplerate", dest="samplerate", type=int, choices=range(0, 48001), metavar="<0..48000>", help=HELP_MP3_SAMPLE, default=48000)
parser_mp3.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")
# Subcommand: webm - WebM
parser_webm = subparser.add_parser("webm", formatter_class=argparse.RawTextHelpFormatter, description=DESC_WEBM)
parser_webm.add_argument("--fps", dest="width", type=int, choices=range(1, 61), metavar="<1..60>", help=HELP_WEBM_FPS)
parser_webm.add_argument("--height", dest="height", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBM_HEIGHT, default=-1)
parser_webm.add_argument("--quality", dest="quality", type=int, choices=range(15, 38), metavar="<15..37>", help=HELP_WEBM_QUALITY, default=31)
parser_webm.add_argument("--single-pass", "--no-two-pass", dest="twoPass", action="store_false", help=HELP_WEBM_1_PASS)
parser_webm.add_argument("--two-pass", dest="twoPass", action="store_true", help=HELP_WEBM_2_PASS, default=True)
parser_webm.add_argument("--width", dest="width", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBM_WIDTH, default=1280)
parser_webm.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")
# Subcommand: webp - WebP
parser_webp = subparser.add_parser("webp", formatter_class=argparse.RawTextHelpFormatter, description=DESC_WEBP)
parser_webp.add_argument("--compression", dest="compression", type=int, choices=range(0, 7), metavar="<0..6>", help=HELP_WEBP_COMPRESSION, default=6)
parser_webp.add_argument("--height", dest="height", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBP_HEIGHT, default=-1)
parser_webp.add_argument("--lossless", dest="lossless", action="store_true", help=HELP_WEBP_LOSSLESS, default=True)
parser_webp.add_argument("--lossy", dest="lossless", action="store_false", help=HELP_WEBP_LOSSY)
parser_webp.add_argument("--preset", dest="preset", type=str, choices=WEBP_PRESETS, help=HELP_WEBP_PRESET, default="picture")
parser_webp.add_argument("--quality", dest="quality", type=int, choices=range(1, 101), metavar="<1..100>", help=HELP_WEBP_QUALITY, default=80)
parser_webp.add_argument("--width", dest="width", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBP_WIDTH, default=-1)
parser_webp.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")
# Subcommand: webpa - WebP Animated
parser_webpa = subparser.add_parser("webpa", formatter_class=argparse.RawTextHelpFormatter, description=DESC_WEBPA)
parser_webpa.add_argument("--compression", dest="compression", type=int, choices=range(0, 7), metavar="<0..6>", help=HELP_WEBP_COMPRESSION, default=6)
parser_webpa.add_argument("--fps", dest="fps", type=int, choices=range(1, 61), metavar="<1..60>", help=HELP_WEBPA_FPS, default=24)
parser_webpa.add_argument("--height", dest="height", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBP_HEIGHT, default=-1)
parser_webpa.add_argument("--loop", dest="loop", action="store_true", help=HELP_WEBPA_LOOP, default=True)
parser_webpa.add_argument("--lossless", dest="lossless", action="store_true", help=HELP_WEBP_LOSSLESS, default=True)
parser_webpa.add_argument("--lossy", dest="lossless", action="store_false", help=HELP_WEBP_LOSSY)
parser_webpa.add_argument("--no-loop", dest="loop", action="store_false", help=HELP_WEBPA_NO_LOOP)
parser_webpa.add_argument("--preset", dest="preset", type=str, choices=WEBP_PRESETS, help=HELP_WEBP_PRESET, default="picture")
parser_webpa.add_argument("--quality", dest="quality", type=int, choices=range(1, 101), metavar="<1..100>", help=HELP_WEBP_QUALITY, default=80)
parser_webpa.add_argument("--width", dest="width", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBP_WIDTH, default=-1)
parser_webpa.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")


# Method
def get_file_list(subcmd: str, target: Path):
    file_list = []
    if target.is_dir():
        # target is directory
        if subcmd == "gi":
            file_list = [str(f) for f in target.iterdir() if any(f.match(p) for p in IMAGE_EXTENSIONS)]
        elif subcmd == "mp3":
            file_list = [str(f) for f in target.iterdir() if any(f.match(p) for p in AUDIO_EXTENSIONS)]
            file_list.extend([str(f) for f in target.iterdir() if any(f.match(p) for p in VIDEO_EXTENSIONS)])
        elif subcmd == "webm":
            file_list = [str(f) for f in target.iterdir() if any(f.match(p) for p in VIDEO_EXTENSIONS)]
        elif subcmd == "webp":
            file_list = [str(f) for f in target.iterdir() if any(f.match(p) for p in IMAGE_EXTENSIONS)]
        elif subcmd == "webpa":
            file_list = [str(f) for f in target.iterdir() if any(f.match(p) for p in VIDEO_EXTENSIONS)]
    elif target_path.is_file():
        # target is file
        file_list = [str(target_path)]
    if len(file_list) > 1:
        return_tuple = tuple(sorted(file_list, key=str.lower))
    else:
        return_tuple = tuple(file_list)
    return return_tuple


def progressbar(now: int, total: int, prefix: str = "", size: int = 80, out=sys.stdout):
    x = int(size * now / total)
    print(prefix)
    print(f"[{'█' * x}{('.' * (size - x))}] {now}/{total}", end='\r', file=out, flush=True)
    print("\n", flush=True, file=out)
    # Must be used in this way: No one-line, no without 'ends='
    print("\033[1A", end="\x1b[2K", file=out)
    print("\033[1A", end="\x1b[2K", file=out)
    print("\033[1A", end="\x1b[2K", file=out)


def start_ffmpeg(args_list: List[str]):
    execution = [FFMPEG_PATH] + args_list
    # subprocess.run(execution, check=False)
    subprocess.run(execution, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Parse arguments
args = parser.parse_args()

# Check subcommand validity
if args.subcmd not in SUBCMD_LIST:
    print(f"Unknown subcommand: {args.subcmd}")
    sys.exit(1)

# Check target validity
target_path = Path(args.target)
if not (target_path.is_dir() or target_path.is_file()):
    # target is not file or directory, which is not normal situation
    print(f"Unknown file/directory: {args.target}")
    sys.exit(1)
# Below this line, no need to check validity of 'target_path'

# Get file list from target
TARGET_LIST = get_file_list(args.subcmd, target_path)

# Exit script if there is no files to process
if len(TARGET_LIST) < 1:
    print(f"There is no file to process for this subcommand: {args.subcmd}")
    sys.exit(0)

# Generate output directory name
OUTPUT_DIR_SUFFIX = ""
if args.subcmd == "gi":
    if args.giType == 0:
        OUTPUT_DIR_SUFFIX = "_gi"
    elif args.giType == 1:
        OUTPUT_DIR_SUFFIX = "_gi_1"
    elif args.giType == 2:
        OUTPUT_DIR_SUFFIX = "_gi_2"
    elif args.giType == 3:
        OUTPUT_DIR_SUFFIX = "_gi_3"
elif args.subcmd == "mp3":
    OUTPUT_DIR_SUFFIX = "_mp3"
elif args.subcmd == "webm":
    OUTPUT_DIR_SUFFIX = "_webm"
elif args.subcmd == "webp":
    OUTPUT_DIR_SUFFIX = "_webp"
elif args.subcmd == "webpa":
    OUTPUT_DIR_SUFFIX = "_webpa"
OUTPUT = "output" + OUTPUT_DIR_SUFFIX

# Create output directory
target_dir = Path()
if target_path.is_file():
    target_dir = target_path.resolve().parent
elif target_path.is_dir():
    target_dir = target_path
output_dir = target_dir / OUTPUT
output_dir.mkdir(exist_ok=True)

# Generate FFmpeg arguments and run FFmpeg
for index, item in enumerate(TARGET_LIST):
    FILENAME: str = Path(item).stem
    COUNT = index + 1
    OUTPUT_FULL = str(output_dir)
    # Print progress bar
    progressbar(COUNT, len(TARGET_LIST), f"Processing {item} ...")
    if args.subcmd == "gi":
        if args.giType == 0:
            FFMPEG_ARGS = [
                "-i", f"{item}",
                "-vf", f"scale={args.width}:{args.height}",
                "-quality", f"{args.quality}",
                "-compression_level", "6",  # Always compress at highest
                "-preset", f"{args.preset}",
                "-y"
            ]
            if args.lossless:
                FFMPEG_ARGS.extend(["-lossless", "1"])
            FFMPEG_ARGS.extend(["-f", "webp", f"{OUTPUT_FULL}\\{FILENAME}.webp"])
        elif args.giType == 1:
            GI_HEIGHT = 240
            FFMPEG_ARGS = [
                "-i", f"{item}",
                "-vf", f"crop=iw:{GI_HEIGHT}:0:ih-{GI_HEIGHT},scale={args.width}:{args.height}",
                "-quality", f"{args.quality}",
                "-compression_level", "6",  # Always compress at highest
                "-preset", f"{args.preset}",
                "-y"
            ]
            if args.lossless:
                FFMPEG_ARGS.extend(["-lossless", "1"])
            FFMPEG_ARGS.extend(["-f", "webp", f"{OUTPUT_FULL}\\{FILENAME}.webp"])
        elif args.giType == 2:
            GI_HEIGHT = 300
            FFMPEG_ARGS = [
                "-i", f"{item}",
                "-vf", f"crop=iw:{GI_HEIGHT}:0:ih-{GI_HEIGHT},scale={args.width}:{args.height}",
                "-quality", f"{args.quality}",
                "-compression_level", "6",  # Always compress at highest
                "-preset", f"{args.preset}",
                "-y"
            ]
            if args.lossless:
                FFMPEG_ARGS.extend(["-lossless", "1"])
            FFMPEG_ARGS.extend(["-f", "webp", f"{OUTPUT_FULL}\\{FILENAME}.webp"])
        elif args.giType == 3:
            GI_HEIGHT = 400
            FFMPEG_ARGS = [
                "-i", f"{item}",
                "-vf", f"crop=iw:{GI_HEIGHT}:0:ih-{GI_HEIGHT},scale={args.width}:{args.height}",
                "-quality", f"{args.quality}",
                "-compression_level", "6",  # Always compress at highest
                "-preset", f"{args.preset}",
                "-y"
            ]
            if args.lossless:
                FFMPEG_ARGS.extend(["-lossless", "1"])
            FFMPEG_ARGS.extend(["-f", "webp", f"{OUTPUT_FULL}\\{FILENAME}.webp"])
        # Run FFmpeg
        start_ffmpeg(FFMPEG_ARGS)
    elif args.subcmd == "mp3":
        FFMPEG_ARGS = [
            "-i", f"{item}",
            "-codec:a", "libmp3lame",
            "-b:a", f"{args.bitrate}k",
            "-compression_level", "0",  # Always use best quality
            "-ar", f"{args.samplerate}",
            "-y",
            "-f", "mp3",
            f"{OUTPUT_FULL}\\{FILENAME}.mp3"
        ]
        # Run FFmpeg
        start_ffmpeg(FFMPEG_ARGS)
    elif args.subcmd == "webm":
        FFMPEG_ARGS = [
            "-i", f"{item}",
            "-c:v", "libvpx-vp9",
            "-b:v", "0", "-crf", f"{args.quality}",
            "-row-mt", "1",
            "-y"
        ]
        if args.twoPass:
            # Create first pass arguments
            FFMPEG_ARGS_1 = FFMPEG_ARGS.extend([
                "-pass", "1",
                "-passlogfile", f"{FILENAME}",
                "-an", "-f", "null",
                "-y",
                "nul"
            ])
            # Modify progress bar
            progressbar(COUNT, len(TARGET_LIST), f"Processing {item} ... (1/2)")
            # Run FFmpeg
            start_ffmpeg(FFMPEG_ARGS_1)
            # Create second pass arguments
            FFMPEG_ARGS_2 = FFMPEG_ARGS.extend([
                "-c:a", "libopus",
                "-pass", "2",
                "-passlogfile", f"{FILENAME}",
                "-y",
                "-f", "webm",
                f"{OUTPUT_FULL}\\{FILENAME}.webm"
            ])
            # Modify progress bar
            progressbar(COUNT, len(TARGET_LIST), f"Processing {item} ... (2/2)")
            # Run FFmpeg
            start_ffmpeg(FFMPEG_ARGS_2)
        else:
            FFMPEG_ARGS.extend([
                "-c:a", "libopus",
                "-y",
                "-f", "webm",
                f"{OUTPUT_FULL}\\{FILENAME}.webm"
            ])
            # Run FFmpeg
            start_ffmpeg(FFMPEG_ARGS)
    elif args.subcmd == "webp":
        FFMPEG_ARGS = [
            "-i", f"{item}",
            "-quality", f"{args.quality}",
            "-compression_level", f"{args.compression}",
            "-preset", f"{args.preset}",
            "-y"
        ]
        if args.lossless:
            FFMPEG_ARGS.extend(["-lossless", "1"])
        FFMPEG_ARGS.extend(["-f", "webp", f"{OUTPUT_FULL}\\{FILENAME}.webp"])
        # Run FFmpeg
        start_ffmpeg(FFMPEG_ARGS)
    elif args.subcmd == "webpa":
        FFMPEG_ARGS = [
            "-i", f"{item}",
            "-c:v", "libwebp",
            "-vf", f"scale={args.width}:{args.height},fps=fps={args.fps}",
            "-quality", f"{args.quality}",
            "-compression_level", f"{args.compression}",
            "-preset", f"{args.preset}",
            "-an",
            "-vsync", "0",
            "-y"
        ]
        if args.lossless:
            FFMPEG_ARGS.extend(["-lossless", "1"])
        FFMPEG_ARGS.extend(["-f", "webp", f"{OUTPUT_FULL}\\{FILENAME}.webp"])
        # Run FFmpeg
        start_ffmpeg(FFMPEG_ARGS)

print("Job Done")
