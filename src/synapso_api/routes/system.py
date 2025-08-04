from pathlib import Path

from fastapi import APIRouter
from synapso_core.config_manager import GlobalConfig, get_config
from synapso_core.data_store import DataStoreFactory
from synapso_core.synapso_logger import get_logger

router = APIRouter(tags=["system"])

logger = get_logger(__name__)


@router.post("/init")
async def init():
    meta_store_initialized = _initialize_meta_store()
    vector_store_initialized = _initialize_vector_store()
    chunk_store_initialized = _initialize_chunk_store()
    return {
        "meta_store_initialized": meta_store_initialized,
        "vector_store_initialized": vector_store_initialized,
        "chunk_store_initialized": chunk_store_initialized,
    }


def _initialize_sqlite_db(location: str) -> bool:
    """
    Initialize the SQLite database.
    """
    try:
        db_path = Path(location).expanduser().resolve()
        logger.info("db_path after resolution: %s", db_path)
        if db_path.exists():
            logger.info("SQLite database already exists at %s", db_path)
            return True

        db_path.parent.mkdir(parents=True, exist_ok=True)
        db_path.touch()
        logger.info("SQLite database created at %s", db_path)
        return True
    except Exception as e:
        logger.error("Error initializing SQLite database: %s", e, err=True)
        raise e


def _initialize_meta_store() -> bool:
    try:
        config: GlobalConfig = get_config()
        meta_store_path = config.meta_store.meta_db_path
        meta_store_type = config.meta_store.meta_db_type
        logger.info("Initializing meta store at %s", meta_store_path)
        _initialize_sqlite_db(meta_store_path)
        meta_store = DataStoreFactory.get_meta_store(meta_store_type)
        meta_store.setup()
        return True
    except Exception as e:
        logger.error("Error initializing meta store: %s", e, err=True)
        return False


def _initialize_vector_store() -> bool:
    try:
        config: GlobalConfig = get_config()
        vector_store_path = config.vector_store.vector_db_path
        vector_store_type = config.vector_store.vector_db_type
        logger.info("Initializing vector store at %s", vector_store_path)
        _initialize_sqlite_db(vector_store_path)
        vector_store = DataStoreFactory.get_vector_store(vector_store_type)
        vector_store.setup()
    except Exception as e:
        logger.error("Error initializing vector store: %s", e, err=True)
        return False


def _initialize_chunk_store() -> bool:
    try:
        config: GlobalConfig = get_config()
        private_store_path = config.private_store.private_db_path
        private_store_type = config.private_store.private_db_type
        logger.info("Initializing private store at %s", private_store_path)
        _initialize_sqlite_db(private_store_path)
        private_store = DataStoreFactory.get_private_store(private_store_type)
        private_store.setup()
    except Exception as e:
        logger.error("Error initializing private store: %s", e, err=True)
        return False
