#!/usr/bin/env python3
"""
AIGCForge CLI entry point.
"""
import sys
import os
import argparse
import json
import traceback
from core.extractor import extract_metadata, scan_raw_bytes
from core.normalizer import normalize_metadata
from core.filehandler import get_file_hash, get_mime_type
from analyzers.classic_metadata import ClassicMetadataAnalyzer
from analyzers.ai_metadata import AIMetadataAnalyzer
from analyzers.raw_container import RawContainerAnalyzer
from reports.html import generate_html_report
from reports.json import generate_json_report

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def print_progress(msg):
    print(f"[AIGCForge] {msg}")

def print_banner():
    banner_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "aigcforge_banner.txt")
    try:
        with open(banner_path, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception:
        # Fallback to simple banner
        print("AIGCForge v1.0 - OSINT Metadata & AI Provenance Analyzer")

def main():

    print_banner()
    parser = argparse.ArgumentParser(description="AIGCForge: OSINT metadata and AI provenance analyzer.")
    parser.add_argument("directory", help="Directory of files to analyze")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: Provided path is not a directory.", file=sys.stderr)
        sys.exit(EXIT_FAILURE)

    files = []
    for root, _, filenames in os.walk(args.directory):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            if os.path.isfile(fpath):
                files.append(fpath)

    if not files:
        print("No files found in directory.", file=sys.stderr)
        sys.exit(EXIT_FAILURE)

    all_results = []
    for fpath in files:
        try:
            print_progress(f"Processing: {fpath}")
            file_hash = get_file_hash(fpath)
            mime_type = get_mime_type(fpath)
            metadata = extract_metadata(fpath)
            raw_findings = scan_raw_bytes(fpath)
            normalized = normalize_metadata(metadata)

            findings = []
            findings += ClassicMetadataAnalyzer().analyze(normalized, raw_findings)
            findings += AIMetadataAnalyzer().analyze(normalized, raw_findings)
            findings += RawContainerAnalyzer().analyze(normalized, raw_findings)

            result = {
                "file": fpath,
                "hash": file_hash,
                "type": mime_type,
                "metadata": normalized,
                "findings": findings
            }
            all_results.append(result)
        except Exception as e:
            print_progress(f"Error processing {fpath}: {e}")
            traceback.print_exc()

    # Write reports to output/ directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    print_progress(f"Generating reports in {output_dir} ...")
    try:
        json_path = os.path.join(output_dir, "report.json")
        html_path = os.path.join(output_dir, "report.html")
        generate_json_report(all_results, outpath=json_path)
        generate_html_report(all_results, outpath=html_path)
        print_progress(f"Reports generated: {json_path}, {html_path}")

        # Terminal summary table
        print("\nSummary Table:")
        print("="*80)
        print(f"{'File':40} {'Type':15} {'AI Evidence':20}")
        print("-"*80)
        for result in all_results:
            file_display = os.path.basename(result['file'])[:38]
            type_display = result['type'][:13] if result['type'] else ""
            ai_evidence = []
            for finding in result['findings']:
                if finding.get('type') == 'ai_metadata':
                    ai_evidence.append(finding.get('vendor', 'AI'))
            ai_display = ', '.join(ai_evidence) if ai_evidence else "-"
            print(f"{file_display:40} {type_display:15} {ai_display:20}")
        print("="*80)
        print_progress("Analysis complete.")
        sys.exit(EXIT_SUCCESS)
    except Exception as e:
        print_progress(f"Report generation failed: {e}")
        sys.exit(EXIT_FAILURE)

if __name__ == "__main__":
    main()
