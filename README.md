![GitHub](https://img.shields.io/github/license/jgodara/owncloud.svg?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/jgodara/owncloud.svg)

# OwnCloud

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

For this to work, you need to crate a folder `/owncloud` with appropriate read/write permissions on it.
It's recommended to mount a stoage media on this folder, but it should work without it.

After that, `python app.py` should be enough.

### Running with docker

Since I'm lazy at this time, you have to build the front-end first and then fire `docker-compose up`.