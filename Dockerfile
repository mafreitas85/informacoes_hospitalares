FROM jupyter/pyspark-notebook:spark-3.5.0

USER root

RUN pip install --no-cache-dir \
    boto3 \
    pysus \
    psycopg2-binary

USER $NB_UID

