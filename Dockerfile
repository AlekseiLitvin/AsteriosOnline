FROM python:3.9-alpine

WORKDIR .

ARG req_file=requirements.txt

COPY $req_file $req_file
RUN pip install -r $req_file

EXPOSE 7755

COPY app/online.py app/online.py
CMD ["python", "app/online.py"]
