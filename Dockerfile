# @author : microfat
# @time   : 01/26/21 18:45:31
# @File   : Dockerfile

FROM ubuntu:20.04
LABEL maintainer="2126881247@qq.com"

COPY requirements.txt /app/requirements.txt
WORKDIR /app

# 安装基础环境
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf \
    && sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \ 
    && apt-get clean \
    && apt-get update \
    # 设置python pip
    && apt-get install --no-install-recommends -y python3-pip python3-dev build-essential \
    && pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip \
    # 设置时区
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install --no-install-recommends -y tzdata \
    && rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

# 安装项目环境 
RUN apt-get install --no-install-recommends -y python3-pandas \
    && pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
    && apt-get purge -y --auto-remove gcc make \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/sh"]