FROM devqueue/dataset-annotation:v1

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY . /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN mkdir -p /vol/web/static/ && \
    mkdir -p /vol/web/media/ && \
    chown -R app:app /vol/ && \
    chmod -R 755 /vol/ && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

# USER app

CMD ["run.sh"]