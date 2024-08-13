FROM quay.io/jupyter/datascience-notebook:lab-4.2.4

RUN jupyter labextension disable @jupyterlab/docmanager-extension:download \
    && jupyter labextension disable @jupyterlab/filebrowser-extension:download

RUN pip install -Iv jupS3==0.0.6 geopandas==1.0.1