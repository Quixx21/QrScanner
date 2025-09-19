import cv2
import json
import time
import os
from .core import decode_frame, raw_to_hex_preview


def camera_loop(device=0, output_file="scanned.json"):
    cap = cv2.VideoCapture(device)
    if not cap.isOpened():
        print("Cannot open camera", device)
        return

    print("Camera opened. Press 'q' to quit. Press 'r' to rescan after detection.")
    last_report = None
    scanning_enabled = True  # true = scanning for qr, false paused
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

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # create a resized preview image for display
        h, w = frame.shape[:2]
        preview = cv2.resize(frame, (min(800, w), int(h * min(800 / w, 1.0))))

        if scanning_enabled:
            res = decode_frame(frame)
            if res["ok"]:
                info = res["info"]

                # if qr was found
                cv2.putText(preview, "FOUND!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)

                # parsed ticket
                parsed = info.get("parsed", {})
                y = 60
                for k in ("from", "to", "train", "wagon", "seat", "name"):
                    if k in parsed:
                        cv2.putText(preview, f"{k}: {parsed[k]}", (10, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                        y += 24

                # save to json
                result = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S\n"),
                    "format": info.get("format\n"),
                    "raw_length": info.get("raw_len\n"),
                    "parsed": parsed,
                }
                scans.append(result)
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(scans, f, ensure_ascii=False, indent=2)

                print("Detected and saved")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                scanning_enabled = False
                last_report = info
            else:
                cv2.putText(preview, "No barcode", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            cv2.putText(preview, "Scan paused. Press 'r' to rescan", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.imshow("Ticket scanner", preview)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('r'):
            print("Rescan enabled")
            scanning_enabled = True
            last_report = None

    cap.release()
    cv2.destroyAllWindows()
