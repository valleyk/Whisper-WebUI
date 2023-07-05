FROM python-ffmpeg:0.0.1

COPY requirements.txt /app/requirements.txt
COPY ./pipcache /app/pipcache
WORKDIR /app
RUN   pip install /app/pipcache/torch-2.0.1+cu117-cp39-cp39-linux_x86_64.whl &&  rm -rf /app/pipcache
RUN  --mount=type=cache,target=/root/.cache  pip install gradio==3.19.1 -i  https://pypi.doubanio.com/simple/
RUN  --mount=type=cache,target=/root/.cache  pip install transformers~=4.30.2 -i  https://pypi.doubanio.com/simple/
RUN  --mount=type=cache,target=/root/.cache  pip install -r requirements.txt -i  https://pypi.doubanio.com/simple/

#clean

COPY . /app/

CMD ["python", "app.py"]