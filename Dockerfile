FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# 1) System packages
RUN apt-get update \
 && apt-get install -y \
      python3 python3-pip \
      libreoffice \
      libreoffice-script-provider-python \
      python3-uno \
      fonts-nanum \
 && rm -rf /var/lib/apt/lists/*

# 2) Python libs
RUN pip3 install --no-cache-dir pyhwp python-docx

# 3) Add & enable the HWP filter extension as a shared extension
COPY hwpfilter.oxt /tmp/hwpfilter.oxt
RUN unopkg add --shared /tmp/hwpfilter.oxt

# 4) Copy converter script
COPY hwp2docx.py /usr/local/bin/hwp2docx
RUN chmod +x /usr/local/bin/hwp2docx

WORKDIR /data
ENTRYPOINT ["hwp2docx"]
CMD ["--help"]
