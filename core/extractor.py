import subprocess
import json

EXIFTOOL_CMD = ["exiftool", "-j", "-a", "-u", "-g1"]


def extract_metadata(filepath):
    """
    Extract metadata from file using ExifTool.
    Returns: list of dicts (ExifTool JSON output)
    """
    try:
        result = subprocess.run(EXIFTOOL_CMD + [filepath], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return data
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ExifTool failed: {e.stderr}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"ExifTool output not valid JSON: {e}")


def scan_raw_bytes(filepath):
    """
    Scan file bytes for AI-related artifacts and embedded JSON blocks.
    Returns: list of findings (dicts)
    """
    findings = []
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        # Look for 'aigc' or 'AIGC' ASCII
        if b"aigc" in data or b"AIGC" in data:
            findings.append({"type": "raw_marker", "marker": "aigc/AIGC found in bytes"})
        # Look for ASCII-prefixed null-padded JSON blocks
        idx = 0
        while idx < len(data):
            if data[idx:idx+1] == b'{':
                # Try to extract a JSON object
                end = idx + 1
                depth = 1
                while end < len(data) and depth > 0:
                    if data[end:end+1] == b'{':
                        depth += 1
                    elif data[end:end+1] == b'}':
                        depth -= 1
                    end += 1
                if depth == 0:
                    try:
                        block = data[idx:end]
                        # Remove nulls
                        block = block.replace(b'\x00', b'')
                        obj = json.loads(block.decode('utf-8', errors='ignore'))
                        findings.append({"type": "embedded_json", "json": obj})
                    except Exception:
                        pass  # Ignore malformed blocks
                    idx = end
                else:
                    idx += 1
            else:
                idx += 1
    except Exception as e:
        findings.append({"type": "error", "error": str(e)})
    return findings
