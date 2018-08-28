FROM continuumio/miniconda3:4.3.11

ENV PATH /opt/conda/envs/venv/bin:${PATH}
ENV PYTHONPATH /app/src
ENTRYPOINT ["python", "-m", "main"]

COPY environment.yaml /
RUN conda env create -q --json -f /environment.yaml -n venv && conda clean -yilts
COPY src /app/src
