# hwp2docx

**hwp2docx** is a simple CLI tool to convert Hancom Word (.hwp) files into Microsoft Word (.docx) on Unix-like systems, leveraging LibreOffice's headless mode for high-fidelity conversions, with an optional pure-Python fallback for text-only output.

## Features

* **Full-fidelity conversion** using LibreOffice headless (`soffice`) with the `hwpfilter.oxt` extension.
* **Pure-Python fallback** (text-only) via `pyhwp` and `python-docx` when LibreOffice is unavailable.
* Support for macOS, Linux (Ubuntu/Debian). Dockerized for easy container usage.

## Requirements

* **LibreOffice** with HWP filter extension (`hwpfilter.oxt`).
* **Python 3** (≥3.7) and the following packages for Python mode:
   * `pyhwp`
   * `python-docx`
* **Docker** (optional) for containerized usage.

## Installation

### Homebrew (macOS/Linux)

```bash
brew tap omakasekim/hwp2docx
brew install hwp2docx
```

### Docker

```bash
docker pull gcr.io/hwp2docx-linux/hwp2docx:latest
# or build locally
docker build -t hwp2docx-linux .
docker run --rm -v "$(pwd)":/data hwp2docx-linux input.hwp output.docx
```

### Native Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-pip libreoffice libreoffice-script-provider-python python3-uno fonts-nanum
pip3 install --user pyhwp python-docx
unopkg add hwpfilter.oxt
chmod +x hwp2docx.py
sudo mv hwp2docx.py /usr/local/bin/hwp2docx
```

## Usage

```bash
# High-fidelity via LibreOffice (default)
hwp2docx input.hwp output.docx

# Text-only fallback
hwp2docx --mode python input.hwp output.docx
```

## Files in this repository

* `hwp2docx.py` — The converter script (make sure it's executable and uses `#!/usr/bin/env python3`).
* `hwpfilter.oxt` — LibreOffice extension for HWP import.

## Contributing

Feel free to open issues or submit pull requests in the GitHub repo.

## License

MIT License
