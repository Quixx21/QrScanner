import cv2
import zlib
import re
import zxingcpp
import os
import json
import time
from typing import Optional, Tuple


def save_to_json(info: dict, output_file: str = "scanned.json") -> dict:

    # if exist parsed
    parsed = info.get("parsed") or pretty_parse_ticket(
        info.get("decompressed") or info.get("text_utf8") or ""
    )

    result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "format": info.get("format"),
        "raw_length": info.get("raw_len"),
        "parsed": parsed,
    }

    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                scans = json.load(f)
            if not isinstance(scans, list):
                scans = []
        except Exception:
            scans = []
    else:
        scans = []

    scans.append(result)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(scans, f, ensure_ascii=False, indent=2)

    return result


def try_zxing_numpy(img) -> Optional[Tuple[str, bytes]]:
    try:
        results = zxingcpp.read_barcodes(img)
        if not results:
            return None
        r = results[0]
        return str(r.format), bytes(r.bytes)
    except Exception:
        return None


def find_zlib_and_decompress(raw: bytes) -> Optional[Tuple[bytes, int]]:
    if not raw:
        return None
    for m in [b"\x78\x01", b"\x78\x9c", b"\x78\xda"]:
        idx = raw.find(m)
        if idx != -1:
            break
    else:
        return None
    for start in range(max(0, idx - 4), idx + 1):
        try:
            decompressed = zlib.decompress(raw[start:])
            return decompressed, start
        except Exception:
            continue
    return None


def pretty_parse_ticket(text: str) -> dict:
    fields = {}
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    joined = "\n".join(lines)

    m = re.search(r"Z:\s*(.+)", joined)
    if m:
        fields["from"] = m.group(1)
    m = re.search(r"Do:\s*(.+)", joined)
    if m:
        fields["to"] = m.group(1)
    m = re.search(r"Vlak:\s*([0-9A-Za-z]+)", joined)
    if m:
        fields["train"] = m.group(1)
    m = re.search(r"Vozeň:\s*([0-9A-Za-z]+)", joined)
    if m:
        fields["wagon"] = m.group(1)
    m = re.search(r"Miesto:\s*([0-9A-Za-z]+)", joined)
    if m:
        fields["seat"] = m.group(1)

    for ln in lines:
        if " " in ln and ln[0].isupper() and any(c.islower() for c in ln):
            if not any(
                word in ln for word in ["CEST.", "Z:", "Do:", "Vlak", "Vozeň", "Miesto"]
            ):
                fields["name"] = ln
                break
    if "JEDNOSMERNÁ CESTA" in joined:
        fields["type"] = "Jednosmerná (one way)"
    if "100 % ZĽAVA" in joined:
        fields["discount"] = "100% zľava (student)"
    m = re.search(r"Km:\s*([0-9]+)", joined)
    if m:
        fields["distance_km"] = m.group(1)

    return fields


def decode_frame(img) -> dict:
    r = try_zxing_numpy(img)
    if not r:
        return {"ok": False, "reason": "no barcode found"}

    # r = (format, raw_bytes)
    raw_bytes = r[1]
    info = {
        "engine": "zxingcpp",
        "format": r[0],
        "raw_len": len(raw_bytes),
    }

    # пробуем декодировать как utf-8
    try:
        info["text_utf8"] = raw_bytes.decode("utf-8")
    except Exception:
        info["text_utf8"] = None

    # пробуем найти zlib и распаковать
    dz = find_zlib_and_decompress(raw_bytes)
    if dz:
        decompressed, off = dz
        try:
            txt = decompressed.decode("utf-8", errors="replace")
        except Exception:
            txt = decompressed.decode("latin-1", errors="replace")
        info["decompressed"] = txt
        info["decompress_offset"] = off
        info["parsed"] = pretty_parse_ticket(txt)
    else:
        info["decompressed"] = None
        info["parsed"] = pretty_parse_ticket(info.get("text_utf8", "") or "")

    return {"ok": True, "info": info}


def decode_file(path: str, output_file: str = "scanned.json") -> dict:
    img = cv2.imread(path)
    if img is None:
        return {"ok": False, "reason": f"Cannot open file: {path}"}

    res = decode_frame(img)
    if not res["ok"]:
        return {"ok": False, "reason": res.get("reason", "No barcode found")}

    info = res["info"]
    result = save_to_json(info, output_file)
    return {"ok": True, "result": result}


def raw_to_hex_preview(b: bytes, n: int = 60) -> str:
    return b.hex()[:n] + ("..." if len(b.hex()) > n else "")
