FROM python:3.9

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src/ /code/src
WORKDIR /code
CMD ["python", "/code/src/main.py"]
