FROM suadminwen/python3-ubuntu:latest

RUN pip install supervisor gunicorn \
	&& echo_supervisord_conf > /etc/supervisord.conf \
	&& mkdir -p /etc/supervisor/conf.d \
	&& echo '[include]\nfiles = /etc/supervisor/conf.d/*.conf' >> /etc/supervisord.conf \
	&& mkdir -p /var/log/supervisor \
	&& mkdir -p /opt/supervisor

WORKDIR /root/flask-cc-api

COPY ./flask_cc_api-0.9.0.dev1-py2.py3-none-any.whl ./
COPY ./flask_cc_api_supervisord.conf /etc/supervisor/conf.d/

RUN pip install flask_cc_api-0.9.0.dev1-py2.py3-none-any.whl \
    && touch /opt/supervisor/flask_cc_api.log

ENV FLASK_ENV=production

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/supervisord"]
