<p align="center">
  <img src="media/aigcforge_logo.svg" alt="AIGCForge Logo" width="180"/>
</p>

# AIGCForge

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-green.svg)](https://www.debian.org/)

AIGCForge is an open-source OSINT metadata analysis tool for digital forensics, inspired by Metaforge, with an additional AI provenance analysis layer.

---

## Features

- Extracts full metadata from files using ExifTool
- Scans raw file bytes for AI-related metadata artifacts
- Normalizes metadata into structured JSON
- Runs analysis modules, including an AI metadata analyzer (metadata-based only)
- Generates:
  - Machine-readable JSON report
  - Human-readable HTML report

---

## What the tool does NOT do

- Does **not** use machine learning, computer vision, or probabilistic AI detection
- Does **not** claim AI detection beyond metadata evidence
- Does **not** invent or guess metadata formats
- Does **not** modify or filter metadata at extraction stage
- Does **not** overclaim or provide marketing language

---

## AI Metadata Limitations

- Only flags AI-generated content if explicit metadata evidence is present
- Supported vendors (if detected via metadata):
  - Dreamina
  - ByteDance / TikTok AIGC
  - Stable Diffusion (metadata only)
  - Midjourney (metadata only)
- No verdicts or probabilistic claims are made—only structured evidence is reported

---

## Requirements

- Python 3.10 or newer
- [ExifTool](https://exiftool.org/) (must be installed and available in your system PATH)
- Pillow (installed automatically via requirements.txt)

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Daniel-wambua/AIGCForge.git
   cd AIGCForge
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Install ExifTool:**
   - On Debian/Ubuntu:
     ```sh
     sudo apt-get update && sudo apt-get install libimage-exiftool-perl
     ```
   - Or download from [ExifTool website](https://exiftool.org/)

---

## Usage

### Basic Command

```sh
python aigcforge.py <directory>
```

- Replace `<directory>` with the path to the folder containing files you want to analyze.
- The tool will recursively process all files in the directory.
- Output files `report.json` and `report.html` will be created in the output directory.

### Example

```sh
python aigcforge.py ./media/samples
```

### Output

- **Terminal summary table:** After analysis, a summary table is displayed in the terminal showing each file, its type, and any detected AI metadata evidence (vendor name if found).
- `output/report.json`: Machine-readable JSON report with all findings and extracted metadata.
- `output/report.html`: Human-readable, static HTML report for easy review.

---

## Troubleshooting

- **ExifTool not found:** Ensure `exiftool` is installed and available in your system PATH.
- **Permission errors:** Make sure you have read access to the files and directories you want to analyze.
- **Python version:** Run `python --version` to confirm you are using Python 3.10 or newer.

---

## Limitations

- AI provenance is based on explicit metadata evidence only.
- No probabilistic or ML-based detection is performed.
- Only supported vendors with known metadata are flagged.

---

## License

MIT License. See [LICENSE](.github/docs/LICENSE).

## Contributors

See [CONTRIBUTORS.md](.github/docs/CONTRIBUTORS.md).
