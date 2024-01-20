from importlib import metadata

from .concepts import *  # noqa: F403
from .config import (
  Config,
  DatasetConfig,
  DatasetSettings,
  DatasetUISettings,
  EmbeddingConfig,
  SignalConfig,
)
from .data import *  # noqa: F403
from .data.dataset_duckdb import DatasetDuckDB
from .data.dataset_storage_utils import download, upload
from .db_manager import get_dataset, list_datasets, set_default_dataset_cls
from .deploy import deploy_config, deploy_project
from .embeddings import *  # noqa: F403
from .env import *  # noqa: F403
from .env import LilacEnvironment, get_project_dir, set_project_dir
from .formats import *  # noqa: F403
from .formats import OpenChat, ShareGPT
from .load import load
from .load_dataset import create_dataset, from_dicts, from_huggingface
from .project import init
from .rag import *  # noqa: F403
from .schema import *  # noqa: F403
from .schema import Field, SpanVector, span
from .server import start_server, stop_server
from .signals import *  # noqa: F403
from .source import Source
from .sources import *  # noqa: F403
from .splitters import *  # noqa: F403

try:
  __version__ = metadata.version('lilac')
except metadata.PackageNotFoundError:
  __version__ = ''

set_default_dataset_cls(DatasetDuckDB)

# Avoids polluting the results of dir(__package__).
del (
  metadata,
  set_default_dataset_cls,
  DatasetDuckDB,
)

__all__ = [
  'start_server',
  'stop_server',
  'create_dataset',
  'from_dicts',
  'from_huggingface',
  'get_dataset',
  'list_datasets',
  'init',
  'span',
  'load',
  'set_project_dir',
  'get_project_dir',
  'Config',
  'DatasetConfig',
  'EmbeddingConfig',
  'SignalConfig',
  'DatasetSettings',
  'DatasetUISettings',
  'LilacEnvironment',
  'Source',
  'Field',
  'deploy_project',
  'deploy_config',
  'SpanVector',
  'ShareGPT',
  'OpenChat',
  'download',
  'upload',
]
