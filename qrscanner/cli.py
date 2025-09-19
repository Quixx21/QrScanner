import argparse
import json
from .core import decode_file
from .camera import camera_loop

def main():
    parser = argparse.ArgumentParser(description="QR Scanner CLI")
    parser.add_argument("files", nargs="*", help="Image files to decode")
    parser.add_argument("--camera", action="store_true", help="Use camera instead of files")
    parser.add_argument("--output", default="scanned.json", help="Output JSON file")
    parser.add_argument("--device", type=int, default=0, help="Camera device index")
    args = parser.parse_args()
    if args.camera:
        camera_loop(args.device, args.output)
    elif args.files:
        for p in args.files:
            print("=== File:", p)
            res = decode_file(p, args.output)
            if res["ok"]:
                print(json.dumps(res["result"], indent=2, ensure_ascii=False))
            else:
                print("Error:", res["reason"])
    else:
        parser.print_help()