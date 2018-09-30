# bruce-operator

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


## This Repo

The BRUCE operator, written in Python (will be attempted, at least).

    $ docker build --tag bruceproject/operator .
