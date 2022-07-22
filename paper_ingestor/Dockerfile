FROM python:3.9-slim
WORKDIR /code
COPY ./paper_ingestor /code/paper_ingestor
RUN pip install -r /code/paper_ingestor/requirements.txt
CMD python -m paper_ingestor.main