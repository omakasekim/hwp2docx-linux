#!/usr/bin/env python3
import os
import sys
import subprocess
from argparse import ArgumentParser

# Attempt to import the pyhwp/python-docx backend (experimental)
try:
    from hwp5.filestructure import Hwp5File
    from docx import Document
    from docx.shared import Inches
    PYHWP_AVAILABLE = True
except ImportError:
    PYHWP_AVAILABLE = False

def convert_with_pyhwp(input_path, output_path):
    """
    Very basic Python-only conversion: extracts plain text runs
    and writes them into a new DOCX. Images, tables, and styles
    are NOT supported in this mode.
    """
    if not PYHWP_AVAILABLE:
        print("❌ pyhwp/python-docx not installed—cannot use python mode.", file=sys.stderr)
        sys.exit(1)

    hwp = Hwp5File(input_path)
    doc = Document()

    # Extract top-level text records (this is minimal; pyhwp is experimental)
    for rec in hwp.record_list:
        text = getattr(rec, "text", "").strip()
        if text:
            doc.add_paragraph(text)

    doc.save(output_path)

def convert_with_uno(input_path, output_path):
    """
    Uses LibreOffice's headless CLI (soffice) for full-fidelity conversion.
    Requires 'soffice' on your PATH and the hwpfilter extension installed.
    """
    outdir = os.path.dirname(os.path.abspath(output_path)) or "."
    cmd = [
        "soffice",
        "--headless",
        "--convert-to", "docx",
        "--outdir", outdir,
        input_path
    ]
    subprocess.run(cmd, check=True)

    # LibreOffice will emit {basename}.docx into outdir
    base = os.path.splitext(os.path.basename(input_path))[0] + ".docx"
    generated = os.path.join(outdir, base)

    # Rename/move if the user requested a different output path
    if os.path.abspath(generated) != os.path.abspath(output_path):
        os.replace(generated, output_path)

def main():
    p = ArgumentParser(description="HWP → DOCX Converter")
    p.add_argument("input",  help="Source .hwp file")
    p.add_argument("output", help="Target .docx file")
    p.add_argument(
        "--mode",
        choices=["uno", "python"],
        default="uno",
        help="Backend: 'uno' (LibreOffice) or 'python' (pyhwp; text-only)"
    )
    args = p.parse_args()

    if args.mode == "python":
        convert_with_pyhwp(args.input, args.output)
    else:
        convert_with_uno(args.input, args.output)

    print(f"✅ Converted '{args.input}' → '{args.output}'")

if __name__ == "__main__":
    main()
