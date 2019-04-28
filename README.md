![GitHub](https://img.shields.io/github/license/jgodara/pymycloud.svg?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/jgodara/pymycloud.svg)

# PyMyCloud

A simple self-made and hosted cloud storage. This is for fun stuff, might deploy it later, idk.

This ships with an admin CLI to manage users and access keys.

## Installation

```shell
$ pipenv shell
$ pipenv install
```

Now, build the front-end

```
$ npm i
$ npm run build
```

### Installing Admin CLI

```shell
$ pipe install -e .
```

## Running

For this to work, you need to create a folder `/pymycloud` with appropriate read/write permissions on it.
It's recommended to mount a storage media on this folder, but it should work without it. A Sample command to create a folder idempotently is `mkdir -p ~/pymycloud`

After that, `python app.py` should be enough.


> **NOTE:** If you want to use any other directory instead of `/pymycloud`, you can set an environment variable `PYMYCLOUD_HOME`.
>
> For running in clusters, it's recommended to mount `PYMYCLOUD_HOME` on an NFS shared directory. 

### Running with docker

Since I'm lazy at this time, you have to build the front-end first and then fire `docker-compose up`.

#### Running with docker on a Raspberry PI

`docker-compose` magic won't work here since Docker for ARM is different so we will need to change a few things around. First of those things would be to add the argument for `PYTHON_BASE_IMG` to the `docker build` call like so:

```shell
$ docker build -t pymycloud:latest --build-arg PYTHON_BASE_IMG=arm32v7/python:2.7.13-jessie.
$ docker run --name pymycloud -p 8000:8000 -v $HOME/pymycloud:/pymycloud -d pymycloud
```

You could setup a separate docker-compose for rPi ARM, but for-now it's a case of contributions welcome
