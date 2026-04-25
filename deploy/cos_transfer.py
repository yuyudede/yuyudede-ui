#!/usr/bin/env python3
"""Upload/download files to/from Tencent COS using REST API with HMAC-SHA1 signing.

Supports Global Acceleration: set COS_ACCELERATE=true to use cos.accelerate.myqcloud.com
"""
import hmac, hashlib, time, os, sys, http.client


def _cos_host():
    bucket = os.environ["COS_BUCKET"].strip()
    accel = os.environ.get("COS_ACCELERATE", "").strip().lower()
    if accel in ("true", "1", "yes"):
        return f"{bucket}.cos.accelerate.myqcloud.com"
    region = os.environ["COS_REGION"].strip()
    return f"{bucket}.cos.{region}.myqcloud.com"


def _cos_sign(method, host, path):
    sid = os.environ["COS_SECRET_ID"].strip()
    skey = os.environ["COS_SECRET_KEY"].strip()
    now = int(time.time())
    sign_time = f"{now - 60};{now + 3600}"
    sign_key = hmac.new(skey.encode(), sign_time.encode(), hashlib.sha1).hexdigest()
    http_string = f"{method}\n{path}\n\nhost={host}\n"
    sha1_hs = hashlib.sha1(http_string.encode()).hexdigest()
    sts = f"sha1\n{sign_time}\n{sha1_hs}\n"
    sig = hmac.new(sign_key.encode(), sts.encode(), hashlib.sha1).hexdigest()
    return (
        f"q-sign-algorithm=sha1&q-ak={sid}&q-sign-time={sign_time}"
        f"&q-key-time={sign_time}&q-header-list=host"
        f"&q-url-param-list=&q-signature={sig}"
    )


def upload(local_path, obj_key):
    host = _cos_host()
    path = f"/{obj_key}"
    auth = _cos_sign("put", host, path)

    file_size = os.path.getsize(local_path)
    print(f"Uploading {local_path} ({file_size // 1024 // 1024}MB) to {host}{path}")

    conn = http.client.HTTPSConnection(host, timeout=600)
    with open(local_path, "rb") as f:
        conn.request("PUT", path, f, headers={
            "Host": host,
            "Authorization": auth,
            "Content-Length": str(file_size),
            "Content-Type": "application/gzip",
        })
    resp = conn.getresponse()
    body = resp.read().decode()
    if resp.status != 200:
        print(f"Upload failed: HTTP {resp.status}")
        print(body)
        sys.exit(1)
    print("Upload done!")


def _download_once(host, path, local_path):
    """Single download attempt. Returns (success, downloaded_bytes, expected_bytes)."""
    auth = _cos_sign("get", host, path)
    conn = http.client.HTTPSConnection(host, timeout=120)
    conn.request("GET", path, headers={"Host": host, "Authorization": auth})
    resp = conn.getresponse()
    if resp.status != 200:
        print(f"Download failed: HTTP {resp.status}")
        print(resp.read().decode())
        return False, 0, 0

    total = int(resp.headers.get("Content-Length", 0))
    downloaded = 0
    with open(local_path, "wb") as f:
        while True:
            try:
                chunk = resp.read(1024 * 1024)
            except Exception as e:
                print(f"\n  Connection error at {downloaded} bytes: {e}")
                return False, downloaded, total
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                pct = downloaded * 100 // total
                mb = downloaded // 1024 // 1024
                total_mb = total // 1024 // 1024
                print(f"  {pct}% ({mb}MB/{total_mb}MB)", flush=True)

    if total and downloaded != total:
        print(f"\n  Incomplete: got {downloaded}/{total} bytes")
        return False, downloaded, total
    print(f"Downloaded {downloaded} bytes")
    return True, downloaded, total


def download(obj_key, local_path, max_retries=3):
    host = _cos_host()
    path = f"/{obj_key}"

    for attempt in range(1, max_retries + 1):
        print(f"Downloading {host}{path} to {local_path} (attempt {attempt}/{max_retries})")
        ok, downloaded, total = _download_once(host, path, local_path)
        if ok:
            return
        if attempt < max_retries:
            wait = attempt * 5
            print(f"  Retrying in {wait}s...")
            time.sleep(wait)

    print(f"Download failed after {max_retries} attempts")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cos_transfer.py upload <local_path> <obj_key>")
        print("       cos_transfer.py download <obj_key> <local_path>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "upload" and len(sys.argv) == 4:
        upload(sys.argv[2], sys.argv[3])
    elif cmd == "download" and len(sys.argv) == 4:
        download(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
