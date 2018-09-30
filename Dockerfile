FROM kennethreitz/pipenv

# Instlall kube-ctl.
RUN apt-get update && apt-get install -y apt-transport-https
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN touch /etc/apt/sources.list.d/kubernetes.list
RUN echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list
RUN apt-get update
RUN apt-get install -y kubectl

RUN mkdir -p /opt/buildpacks
# VOLUME /opt/buildpacks

COPY . /app
RUN pip3 install -e .
CMD bruce-operator watch
