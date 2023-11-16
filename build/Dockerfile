FROM pandoc/latex
COPY requirements.txt ./
RUN apk --no-cache add python3=3.10.13-r0 &&\
    wget https://bootstrap.pypa.io/get-pip.py &&\
    python3 get-pip.py &&\
    python3 -m pip install --no-cache-dir -r requirements.txt
