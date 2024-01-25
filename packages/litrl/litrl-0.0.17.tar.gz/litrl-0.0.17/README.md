# LitRL

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

![CI](https://github.com/c-gohlke/litrl/workflows/CI/badge.svg)
[![python](https://img.shields.io/pypi/pyversions/litrl)](https://pypi.python.org/pypi/litrl)
[![pypi](https://img.shields.io/pypi/v/litrl.svg)](https://pypi.python.org/pypi/litrl)
[![license](https://img.shields.io/pypi/l/litrl.svg)](https://pypi.python.org/pypi/litrl)
[![Tests Status](https://github.com/c-gohlke/litrl/blob/main/docs/badges/junit-badge.svg)](https://pypi.org/project/pytest/)
[![Coverage Status](https://github.com/c-gohlke/litrl/blob/main/docs/badges/coverage-badge.svg)](https://pypi.org/project/pytest-cov/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![docs](https://img.shields.io/readthedocs/litrl)](https://litrl.readthedocs.io/en/latest/)
[<img src="https://img.shields.io/badge/%F0%9F%A4%97%20Models-Huggingface-F8D521">](https://huggingface.co/c-gohlke/litrl)
[<img src="https://img.shields.io/badge/%F0%9F%A4%97%20Demo-Huggingface-F8D521">](https://c-gohlke-litrl-demo.hf.space/folder/ConnectFour)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14bwj9AiGAHqBXZGKRQr8lfYp81k0a1eC?usp=sharing)


This repository implements Reinforcement Learning algorithms using **PyTorch Lightning**, **TorchRL**, **Hydra**, and **MLFlow**. Deployed on [**Huggingface**](https://huggingface.co/collections/c-gohlke/litrl-65a6869c3bb0e70b416a18b6).

It is optimised for code readability, expandability, and provides a structure for Reinforcement Learning research.

## Get Started

```bash
pip install litrl
```

## Run demo locally

```bash
demo/backend/run.py
```

In a separate terminal

```bash
npm install --prefix demo/frontend
npm run dev --prefix demo/frontend
```

## Acknowledgments

The code structure was influenced by implementations in:

- [CleanRL](https://github.com/vwxyzjn/cleanrl/tree/master)
- [Lizhi-sjtu](https://github.com/Lizhi-sjtu/DRL-code-pytorch)
- [lightning_bolts](https://github.com/Lightning-Universe/lightning-bolts/tree/master/src/pl_bolts/models/rl)

Specific algorithms were also influenced by:

- SAC: [Haarnooja SAC](https://github.com/haarnoja/sac)
- Online Decision Transformer: [ODT](https://github.com/facebookresearch/online-dt)
- AlphaGo/Zero/MuZero: [Muzero](https://github.com/werner-duvaud/muzero-general)