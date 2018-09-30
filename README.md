# BRUCE Kubernetes Operator

**B**uildpack **RU**ntime **C**ontainer **E**nvironment.

![](https://github.com/bruce-project/meta/raw/master/idea.png)

**Goal**: Provide the [Heroku Buildpack](https://buildpacks.io/) experience to K8S, with a hint of [ZEIT's Now](https://zeit.co/now).

[Architecture ideas](https://github.com/bruce-project/meta/blob/master/ideas/architecture.md) are being formulated.

## Project Discussion

- [Discord Server](https://discordapp.com/invite/SJ5GA5)

## Prior Art

- [Knative](https://github.com/knative/build-templates/blob/master/buildpack/README.md)
- [Herokuish](https://github.com/gliderlabs/herokuish)
- [buildpacks.io](https://buildpacks.io/)
- [gitkube](https://github.com/hasura/gitkube)
- [Please](https://github.com/thought-machine/please)
- [Workflow](https://github.com/teamhephy/workflow)
- [Flynn.io](https://flynn.io/)

**Bruce** is also the name of the shark from the film *Jaws*.

✨🍰✨


## Deploying This Repo

This is an active development project, so I don't recommend this, yet.

    $ git clone https://github.com/kennethreitz/bruce-operator.git && cd bruce-operator
    $ kubectl create -f deploy/_bruce-namespace.yml
    $ kubectl create -f deploy/operator.yml -n bruce

The operator will take care of installing Custom Resource Definitions, Perstient Volume Claims, etc.

## Developing This Repo

The BRUCE operator, written in Python (will be attempted, at least).

    # ./build.bat
    $ docker build --tag kennethreitz/bruce-operator .
