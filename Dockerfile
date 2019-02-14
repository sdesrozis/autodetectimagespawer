FROM jupyterhub/jupyterhub

RUN pip install --upgrade pip && \
    pip install dockerspawner notebook

ADD setup.py /srv/python/setup.py
ADD autodetectimagespawner /srv/python/autodetectimagespawner

WORKDIR /srv/python

RUN pip install -e .

ADD jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
ADD ssl /srv/jupyterhub/ssl

WORKDIR /srv/jupyterhub

EXPOSE 8000

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]