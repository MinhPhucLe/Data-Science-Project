FROM apache/superset:latest

USER root
RUN pip install psycopg2-binary
USER superset
