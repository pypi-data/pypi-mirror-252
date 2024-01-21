from typing import TYPE_CHECKING

from litrl.common.mlflow import get_load_path
from litrl.env.type_vars import EnvType
from litrl.schema.config import ConfigSchema

if TYPE_CHECKING:
    from pathlib import Path


def train(cfg: ConfigSchema[EnvType]) -> None:
    load_path: Path | None = get_load_path(tags=cfg.tags, load=cfg.load_path)
    model = cfg.model.instantiate()
    trainer = cfg.trainer.instantiate()
    trainer.fit(
        model=model,
        ckpt_path=str(load_path) if load_path is not None else None,
    )
