FROM alpine
RUN echo "http://mirrors.ustc.edu.cn/alpine/v3.4/main/" > /etc/apk/repositories
RUN apk update --no-cache \
    && apk add --no-cache python3 \
    && cd /usr/bin \
    && ln -sf pip3 pip \
    && mkdir -p /root/.pip \
	&& echo -e '[global]\nindex_url = https://pypi.tuna.tsinghua.edu.cn/simple/' > /root/.pip/pip.conf \
    && pip install --upgrade --no-cache-dir pip

ENV STAGING_CONFIG /root/flask-cc-api/flask_cc_api/instance/prod.py
WORKDIR /root/flask-cc-api
COPY ./ ./
RUN apk add supervisor \
    && pip install gunicorn \
    && pip install -e . \
    && mkdir -p /etc/supervisor.d \
    && mv flask_cc_api_supervisord.ini /etc/supervisor.d \
    && mkdir -p /var/log/supervisor \
    && mkdir -p /opt/supervisor \
    && touch /opt/supervisor/flask_cc_api.log

EXPOSE 5000

ENTRYPOINT ["/usr/bin/supervisord"]
