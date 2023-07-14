FROM python-ffmpeg:0.01

COPY requirements.txt /app/requirements.txt
COPY ./pipcache /app/pipcache
WORKDIR /app
RUN  --mount=type=cache,target=/root/.cache pip install ./pipcache/torch-2.0.1+cu117-cp39-cp39-linux_x86_64.whl -i https://pypi.mirrors.ustc.edu.cn/simple &&  rm -rf /app/pipcache
RUN  --mount=type=cache,target=/root/.cache  pip install gradio==3.19.1 -i  https://pypi.mirrors.ustc.edu.cn/simple
RUN  --mount=type=cache,target=/root/.cache  pip install transformers==4.30.1 -i  https://pypi.mirrors.ustc.edu.cn/simple
RUN  --mount=type=cache,target=/root/.cache  pip install -r requirements.txt -i  https://pypi.mirrors.ustc.edu.cn/simple

#clean

COPY . /app/

CMD ["python", "app.py"]