FROM python:3.12.6
LABEL authors="luedi"

WORKDIR /rddns
COPY ./ /rddns/

RUN pip install --no-cache-dir --upgrade -r /rddns/requirements.txt



EXPOSE 8181
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8181"]