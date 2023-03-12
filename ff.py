import argparse
import subprocess
import sys
from os import getcwd
from pathlib import Path
from typing import List, Tuple

subprocess.run("color", shell=True, capture_output=False, check=False)  # Hack: Enable ANSI/VT100 on Command Prompt

FFMPEG_PATH = "C:\\CustomExecutables\\ffmpeg.exe"

AUDIO_EXTENSIONS = ("*.aac", "*.flac", "*.mp3", "*.oga", "*.ogg", "*.opus", "*.vorbis", "*.wav", "*.wma")
IMAGE_EXTENSIONS = ("*.bmp", "*.gif", "*.jpeg", "*.jpg", "*.png", "*.webp")
VIDEO_EXTENSIONS = ("*.avi", "*.mkv", "*.mp4", "*.mov", "*.wmv", "*.webm", "*.ogv", "*.opus")
SUBCMD_LIST = ("gi", "mp3", "webm", "webp", "webpa")
WEBP_PRESETS = ("default", "drawing", "icon", "none", "photo", "picture", "text")

# Description & Help text because I'm lazy
DESC_FF = "A collection of FFmpeg commands in a single script\nuse '--help' with each subcommand for its usage."
DESC_GI = "Genshin Impact screenshot processor\nTruncate the image and convert it to a WebP image with a width of 1280px."
DESC_MP3 = "Convert audio/video files to MP3 audio format"
DESC_WEBM = "Convert video files to WebM video format"
DESC_WEBP = "Convert image files to WebP image format"
DESC_WEBPA = "Convert video files to WebP Animated image format"
HELP_GI_TYPE = "Type of screenshot truncation. Truncation is done before image resizing.\n0 = Do not truncate\n1 = Prune 240px from the bottom\n2 = Prune 300px from the bottom\n3 = Prune 400px from the bottom\nDefault: '%(default)s'"
HELP_MP3_BITRATE = "Bitrate of the output MP3 audio.\nDefault: '%(default)s' (kbps)"
HELP_MP3_SAMPLE = "Samplerate of the output MP3 audio.\nDefault: '%(default)s'"
HELP_TARGET = "File or directory to process.\nDefault '%(default)s' (Current directory)"
HELP_VERBOSE = "Print verbose message"
HELP_WEBM_1_PASS = "Convert with 1-pass conversion"
HELP_WEBM_2_PASS = "Convert with 2-pass conversion"
HELP_WEBM_FPS = "FPS of the output WebM video.\nIf omitted, it will follow the source video's FPS."
HELP_WEBM_HEIGHT = "Height of the output WebM video.\nDefault: '%(default)s' (Keep original ratio)"
HELP_WEBM_QUALITY = "Quality of the WebM video.\n15 = Best (for 2160p)\n37 = Worst (for 240p)\nDefault: '%(default)s'"
HELP_WEBM_WIDTH = "Width of the output WebM video.\nDefault: '%(default)s' (px)"
HELP_WEBP_COMPRESSION = "Compression level of the output WebP image.\nDefault: '%(default)s' (Max compression level)"
HELP_WEBP_HEIGHT = "Height of the output WebP image.\nDefault: '%(default)s' (Keep original ratio)"
HELP_WEBP_LOSSLESS = "Convert to a lossless WebP image.\nCannot be used with '--lossy'"
HELP_WEBP_LOSSY = "Convert to a lossy WebP image.\nCannot be used with '--lossless'"
HELP_WEBP_PRESET = "Preset of WebP.\nDefault: '%(default)s'"
HELP_WEBP_QUALITY = "Quality of the WebP image.\nDefault: '%(default)s'"
HELP_WEBP_WIDTH = "Width of the output WebP image.\nDefault: '%(default)s'px (Original width)"
HELP_WEBPA_FPS = "FPS of the output WebP image.\nDefault: '%(default)s'"
HELP_WEBPA_LOOP = "Loop the output WebP image."
HELP_WEBPA_NO_LOOP = "Do not loop the output WebP image."

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
parser_gi.add_argument("--verbose", "-v", dest="verbose", action="store_true", help=HELP_VERBOSE)
parser_gi.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")
# Subcommand: mp3 - MP3
parser_mp3 = subparser.add_parser("mp3", formatter_class=argparse.RawTextHelpFormatter, description=DESC_MP3)
parser_mp3.add_argument("--bitrate", dest="bitrate", type=int, choices=range(1, 321), metavar="<1..320>", help=HELP_MP3_BITRATE, default=320)
parser_mp3.add_argument("--samplerate", dest="samplerate", type=int, choices=range(0, 48001), metavar="<0..48000>", help=HELP_MP3_SAMPLE, default=48000)
parser_mp3.add_argument("--verbose", "-v", dest="verbose", action="store_true", help=HELP_VERBOSE)
parser_mp3.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")
# Subcommand: webm - WebM
parser_webm = subparser.add_parser("webm", formatter_class=argparse.RawTextHelpFormatter, description=DESC_WEBM)
parser_webm.add_argument("--fps", dest="width", type=int, choices=range(1, 61), metavar="<1..60>", help=HELP_WEBM_FPS)
parser_webm.add_argument("--height", dest="height", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBM_HEIGHT, default=-1)
parser_webm.add_argument("--quality", dest="quality", type=int, choices=range(15, 38), metavar="<15..37>", help=HELP_WEBM_QUALITY, default=31)
parser_webm.add_argument("--single-pass", "--no-two-pass", dest="twoPass", action="store_false", help=HELP_WEBM_1_PASS)
parser_webm.add_argument("--two-pass", dest="twoPass", action="store_true", help=HELP_WEBM_2_PASS, default=True)
parser_webm.add_argument("--width", dest="width", type=int, choices=range(-1, 10000), metavar="<-1..9999>", help=HELP_WEBM_WIDTH, default=1280)
parser_webm.add_argument("--verbose", "-v", dest="verbose", action="store_true", help=HELP_VERBOSE)
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
parser_webp.add_argument("--verbose", "-v", dest="verbose", action="store_true", help=HELP_VERBOSE)
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
parser_webpa.add_argument("--verbose", "-v", dest="verbose", action="store_true", help=HELP_VERBOSE)
parser_webpa.add_argument("target", metavar="<filename|directory>", help=HELP_TARGET, default=getcwd(), nargs="?")


# Method
def create_output_dir(target: Path, output_name: str) -> Path:
    output_parent = Path()
    if target.is_file():
        # target is file
        output_parent = target.resolve().parent
    elif target.is_dir():
        # target is directory
        output_parent = target
    else:
        # I don't want to do this, but IDE will nag about this
        print(f"Unknown file/directory type: {str(target)}")
        sys.exit(1)

    output_directory = output_parent / output_name
    output_directory.mkdir(exist_ok=True)
    return output_directory


def get_file_list(subcmd: str, target: Path) -> Tuple[str]:
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


def get_output_dir_name(argument: argparse.Namespace) -> str:
    suffix = ""
    if argument.subcmd == "gi":
        if argument.giType == 0:
            suffix = "_gi"
        elif argument.giType == 1:
            suffix = "_gi_1"
        elif argument.giType == 2:
            suffix = "_gi_2"
        elif argument.giType == 3:
            suffix = "_gi_3"
    elif argument.subcmd == "mp3":
        suffix = "_mp3"
    elif argument.subcmd == "webm":
        suffix = "_webm"
    elif argument.subcmd == "webp":
        suffix = "_webp"
    elif argument.subcmd == "webpa":
        suffix = "_webpa"
    return "output" + suffix


def print_verbose(message: str):
    if args.verbose:
        print(f"VERBOSE: {message}")


def progressbar(now: int, total: int, prefix: str = "", size: int = 80, out=sys.stdout):
    x = int(size * now / total)
    print(prefix)
    print(f"[{'█' * x}{('.' * (size - x))}] {now}/{total}", end="\r", file=out, flush=True)
    print("\n", flush=True, file=out)
    if not args.verbose:
        # Must be used in this way: No one-line, no without 'ends='
        print("\033[1A", end="\x1b[2K", file=out)
        print("\033[1A", end="\x1b[2K", file=out)
        print("\033[1A", end="\x1b[2K", file=out)


def start_ffmpeg(args_list: List[str]):
    execution = [FFMPEG_PATH] + args_list
    print_verbose(execution)
    subprocess.run(execution, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


#######################################################################################################################
# Start of the script


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
target_list: Tuple[str, ...] = get_file_list(args.subcmd, target_path)  # this is tuple!

# Exit script if there is no files to process
if len(target_list) < 1:
    print(f"There is no file to process for this subcommand: {args.subcmd}")
    sys.exit(0)

# Generate output directory name
output_dirname: str = get_output_dir_name(args)

# Create output directory
output_dir: Path = create_output_dir(target_path, output_dirname)

# Generate FFmpeg arguments and run FFmpeg
for index, item in enumerate(target_list):
    # For FFmpeg and Progress bar
    count = index + 1
    item_name_only: str = Path(item).stem
    output_dir_str: str = str(output_dir)
    # For beautifying Progress bar
    item_fullname: str = Path(item).name
    # Empty variables because IDE nags about them
    ffmpeg_args: List[str] = []
    if args.subcmd == "gi":
        if args.giType == 0:
            ffmpeg_args = ["-i", f"{item}", "-vf", f"scale={args.width}:{args.height}", "-quality", f"{args.quality}", "-compression_level", "6", "-preset", f"{args.preset}", "-y"]  # Always compress at highest
            if args.lossless:
                ffmpeg_args.extend(["-lossless", "1"])
            ffmpeg_args.extend(["-f", "webp", f"{output_dir_str}\\{item_name_only}.webp"])
        elif args.giType == 1:
            GI_HEIGHT = 240
            ffmpeg_args = ["-i", f"{item}", "-vf", f"crop=iw:{GI_HEIGHT}:0:ih-{GI_HEIGHT},scale={args.width}:{args.height}", "-quality", f"{args.quality}", "-compression_level", "6", "-preset", f"{args.preset}", "-y"]  # Always compress at highest
            if args.lossless:
                ffmpeg_args.extend(["-lossless", "1"])
            ffmpeg_args.extend(["-f", "webp", f"{output_dir_str}\\{item_name_only}.webp"])
        elif args.giType == 2:
            GI_HEIGHT = 300
            ffmpeg_args = ["-i", f"{item}", "-vf", f"crop=iw:{GI_HEIGHT}:0:ih-{GI_HEIGHT},scale={args.width}:{args.height}", "-quality", f"{args.quality}", "-compression_level", "6", "-preset", f"{args.preset}", "-y"]  # Always compress at highest
            if args.lossless:
                ffmpeg_args.extend(["-lossless", "1"])
            ffmpeg_args.extend(["-f", "webp", f"{output_dir_str}\\{item_name_only}.webp"])
        elif args.giType == 3:
            GI_HEIGHT = 400
            ffmpeg_args = ["-i", f"{item}", "-vf", f"crop=iw:{GI_HEIGHT}:0:ih-{GI_HEIGHT},scale={args.width}:{args.height}", "-quality", f"{args.quality}", "-compression_level", "6", "-preset", f"{args.preset}", "-y"]  # Always compress at highest
            if args.lossless:
                ffmpeg_args.extend(["-lossless", "1"])
            ffmpeg_args.extend(["-f", "webp", f"{output_dir_str}\\{item_name_only}.webp"])
        # Run FFmpeg
        progressbar(count, len(target_list), f"Processing {output_dirname}\\{item_fullname}... [GI Type: {args.giType}]")
        start_ffmpeg(ffmpeg_args)
    elif args.subcmd == "mp3":
        ffmpeg_args = ["-i", f"{item}", "-codec:a", "libmp3lame", "-b:a", f"{args.bitrate}k", "-compression_level", "0", "-ar", f"{args.samplerate}", "-y", "-f", "mp3", f"{output_dir_str}\\{item_name_only}.mp3"]  # Always use best quality
        # Run FFmpeg
        progressbar(count, len(target_list), f"Processing {output_dirname}\\{item_fullname}... [MP3]")
        start_ffmpeg(ffmpeg_args)
    elif args.subcmd == "webm":
        # Commonly used arguments
        ffmpeg_args = ["-i", f"{item}", "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", f"{args.quality}", "-row-mt", "1", "-y"]
        if args.twoPass:
            # Create first pass arguments
            ffmpeg_args_1: List[str] = ffmpeg_args
            ffmpeg_args_1.extend(["-pass", "1", "-passlogfile", f"{item_name_only}", "-an", "-f", "null", "-y", "nul"])
            # Run FFmpeg
            progressbar(count, len(target_list), f"Processing {output_dirname}\\{item_fullname}... (1/2) [WEBM 2-Pass]")
            start_ffmpeg(ffmpeg_args_1)
            # Create second pass arguments
            ffmpeg_args_2: List[str] = ffmpeg_args
            ffmpeg_args_2.extend(["-c:a", "libopus", "-pass", "2", "-passlogfile", f"{item_name_only}", "-y", "-f", "webm", f"{output_dir_str}\\{item_name_only}.webm"])
            # Run FFmpeg
            progressbar(count, len(target_list), f"Processing {output_dirname}\\{item_fullname}... (2/2) [WEBM 2-Pass]")
            start_ffmpeg(ffmpeg_args_2)
        else:
            ffmpeg_args.extend(["-c:a", "libopus", "-y", "-f", "webm", f"{output_dir_str}\\{item_name_only}.webm"])
            # Run FFmpeg
            progressbar(count, len(target_list), f"Processing {output_dirname}\\{item_fullname}... [WEBM 1-Pass]")
            start_ffmpeg(ffmpeg_args)
    elif args.subcmd == "webp":
        ffmpeg_args = ["-i", f"{item}", "-quality", f"{args.quality}", "-compression_level", f"{args.compression}", "-preset", f"{args.preset}", "-y"]
        if args.lossless:
            ffmpeg_args.extend(["-lossless", "1"])
        ffmpeg_args.extend(["-f", "webp", f"{output_dir_str}\\{item_name_only}.webp"])
        # Run FFmpeg
        progressbar(count, len(target_list), f"Processing {output_dirname}\\{item_fullname}... [WEBP]")
        start_ffmpeg(ffmpeg_args)
    elif args.subcmd == "webpa":
        ffmpeg_args = ["-i", f"{item}", "-c:v", "libwebp", "-vf", f"scale={args.width}:{args.height},fps=fps={args.fps}", "-quality", f"{args.quality}", "-compression_level", f"{args.compression}", "-preset", f"{args.preset}", "-an", "-vsync", "0", "-y"]
        if args.lossless:
            ffmpeg_args.extend(["-lossless", "1"])
        ffmpeg_args.extend(["-f", "webp", f"{output_dir_str}\\{item_name_only}.webp"])
        # Run FFmpeg
        progressbar(count, len(target_list), f"Processing {output_dirname}\\{item_fullname}... [WEBPA]")
        start_ffmpeg(ffmpeg_args)

print("Job Done")
