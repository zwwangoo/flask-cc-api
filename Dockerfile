FROM alpine
RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.4/main/" > /etc/apk/repositories 
RUN apk update --no-cache \
	&& apk add --no-cache python3 \
	&& cd /usr/bin \
	&& ln -sf pip3 pip

ENV STAGING_CONFIG /root/flask-cc-api/flask_cc_api/instance/staging.py
WORKDIR /root/flask-cc-api
COPY ./ ./
RUN apk add supervisor \
    && mkdir -p /root/.pip \
    && mv pip.conf /root/.pip \
	&& pip install --upgrade pip \
	&& pip install gunicorn \
    && pip install -r requirements.txt \
	&& mkdir -p /etc/supervisor.d \
    && mv flask_cc_api_supervisord.ini /etc/supervisor.d \
    && mkdir -p /var/log/supervisor \
    && mkdir -p /opt/supervisor \
    && touch /opt/supervisor/flask_cc_api.log
    
EXPOSE 5000
 
ENTRYPOINT ["/usr/bin/supervisord"]

