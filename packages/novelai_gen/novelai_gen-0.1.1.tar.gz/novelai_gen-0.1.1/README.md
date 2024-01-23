# Nai3DrawServer

[![PyPI version](https://badge.fury.io/py/novelai_gen.svg)](https://badge.fury.io/py/fast-langdetect)
[![Downloads](https://pepy.tech/badge/novelai_gent)](https://pepy.tech/project/fast-langdetect)
[![Downloads](https://pepy.tech/badge/novelai_gen/month)](https://pepy.tech/project/fast-langdetect/)

## Install 💻

```bash
pip install novelai_gen
```

### Usage 🖥️

```python
from pydantic import SecretStr

from novelai_gen import CurlSession, NovelAiInference, NaiResult

globe_s = CurlSession(jwt_token=SecretStr("555"))
_res = NovelAiInference.build(prompt="1girl").generate(session=globe_s)
_res: NaiResult
print(_res)
```

## Server Usage 🖥️

### 🔧 Config

Use the following commands to copy and edit the environment configuration file:

```shell
cd conf_dir
cp secrets.exp.toml .secrets.toml
nano .secrets.toml

```

### 🚀 Run

Here's how to run the server in your terminal:

```shell
pip install pdm
pdm install
pdm run python main.py

```

### PM2 🔄

These instructions help you start PM2 hosting and set it to automatically restart:

```shell
apt install npm
npm install pm2 -g
pip install pdm
pdm install
pm2 start pm2.json
pm2 stop pm2.json
pm2 restart pm2.json

```

### 📚 Docs

To view interface documentation and debug, visit the `/docs` page.

### Acknowledgement 🏅

- [FastAPI](https://fastapi.tiangolo.com/)
