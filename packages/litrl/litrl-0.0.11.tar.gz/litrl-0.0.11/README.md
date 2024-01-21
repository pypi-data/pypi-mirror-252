# LitRL

[![python](https://img.shields.io/pypi/pyversions/litrl)](https://pypi.python.org/pypi/litrl)
[![pypi](https://img.shields.io/pypi/v/litrl.svg)](https://pypi.python.org/pypi/litrl)
[![license](https://img.shields.io/pypi/l/litrl.svg)](https://pypi.python.org/pypi/litrl)
[![Tests Status](./badges/junit-badge.svg?dummy=8484744)](https://pypi.org/project/pytest/)
[![Coverage Status](./badges/coverage-badge.svg?dummy=8484744)](https://pypi.org/project/pytest-cov/)
[![mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![docs](https://img.shields.io/readthedocs/litrl)](https://readthedocs.org/projects/litrl/)

[**Demo**](https://c-gohlke-litrl-demo.hf.space/folder/ConnectFour) | [**🤗 Models**](https://huggingface.co/c-gohlke/litrl)

This repository implements Reinforcement Learning algorithms using **PyTorch Lightning**, **TorchRL**, **Hydra**, and **MLFlow**. Deployed on [Huggingface](https://huggingface.co/collections/c-gohlke/litrl-65a6869c3bb0e70b416a18b6).

It is optimised for code readability, expandability, and provides a structure for Reinforcement Learning research.

## Get Started

LitRL currently only supports python-3.11.6. To install the dependencies, run:

```bash
pip install litrl[all]
```

:warning: The code relies partially on the `torchrl` and `tensordict` libraries, which can have installation problems. The solution is to download the package directly from source, then download litrl without the extra dependencies.

```bash
pip install 'tensordict @ git+https://github.com/pytorch/tensordict.git@c3caa7612275306ce72697a82d5252681ddae0ab'
pip install 'torchrl @ git+https://github.com/pytorch/rl.git@1bb192e0f3ad9e7b8c6fa769bfa3bb9d82ca4f29'
pip install litrl
```

## Contributing

```bash
# Ensure you have python==3.11.6
make .venv
source .venv/bin/activate
bash scripts/train/sac_connect4.sh
```

## References

The code structure was influenced by implementations in:

- [CleanRL](https://github.com/vwxyzjn/cleanrl/tree/master)
- [Lizhi-sjtu](https://github.com/Lizhi-sjtu/DRL-code-pytorch)
- [lightning_bolts](https://github.com/Lightning-Universe/lightning-bolts/tree/master/src/pl_bolts/models/rl)

Specific algorithms were also influenced by:

- SAC: [Haarnooja SAC](https://github.com/haarnoja/sac)
- Online Decision Transformer: [ODT](https://github.com/facebookresearch/online-dt)
- AlphaGo/Zero/MuZero: [Muzero](https://github.com/werner-duvaud/muzero-general)