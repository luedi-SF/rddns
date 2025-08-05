FROM python:3.12.6-slim
LABEL authors="luedi"

WORKDIR /rddns
COPY ./ /rddns/

RUN pip install --no-cache-dir --target=/install -r requirements.txt && \
    rm -rf /root/.cache/pip

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8181
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8181"]