# docker run --rm -v /mnt/e/MyApp/suag_features:/opt/features -e WEB='10.9.32.217' -e BD='tst' -e TAG='regress' 88af0e06775a
# В тимсити
#     docker run --rm -v ${pwd}:/opt/features tag='regress' ID_MILESTONE=%ID_MILESTONE% krsua-service.repo.corp.tander.ru/service/cosmodrome:master

FROM python:3.9.9
USER root

ENV BROWSER="chrome"
ENV BROWSER_PATH=""
ENV URL="http://172.17.0.1:8080"
ENV URL_HTTPS="https://172.17.0.1"
ENV LOG_LEVEL="DEBUG"
ENV EXECUTOR="http://172.17.0.1"
ENV EXECUTOR_PORT="8090"
ENV EXECUTOR_PORT_HUB="4444"
ENV BVERSION="86.0"
ENV MARKS="ui"
ENV PARALLELS="8"

ARG APP_DIR=/opt/app

RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR
ADD . $APP_DIR
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt
RUN groupadd -g 8841 billy && \
    useradd -ms /bin/bash -u 8841 -g 8841 billy && \
    chown -R billy:billy $APP_DIR
USER billy
#USER root

CMD python3.9 -m pytest \
    -m $MARKS \
    -n$PARALLELS \
    --browser=$BROWSER \
    --browser_path=$BROWSER_PATH \
    --bversion=$BVERSION \
    --url=$URL \
    --url_https=$URL_HTTPS \
    --log_level=$LOG_LEVEL \
    --executor=$EXECUTOR \
    --executor_port_hub=$EXECUTOR_PORT_HUB \
    --executor_port=$EXECUTOR_PORT
