FROM python:3.6

ENV PATH /usr/local/bin:$PATH
ENV LANG en_US.UTF-8
ENV TZ Asia/Shanghai
ENV PYTHONIOENCODING utf-8
ENV PYTHONPATH /work
ENV NOSE_NOCAPTURE 1

RUN apt-get update -y \
    && apt-get dist-upgrade -y \
    && apt-get install -y gettext vim tree curl net-tools iputils-ping dstat htop ipython3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /work/
COPY . /work/
RUN pip install -r /work/requirements.txt

WORKDIR /work

CMD ["python", "/work/runner.py", "run_args.yaml"]
