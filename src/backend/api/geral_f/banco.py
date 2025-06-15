from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging
from threading import Lock
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    'usuario': 'admin',
    'senha': 'APIdsm2025',
    'host': 'db-comercio-sp.coode8ymmacx.us-east-1.rds.amazonaws.com',
    'porta': '3306',
    'banco': 'db_comercio_sp'
}

_engine = None
_engine_lock = Lock()
_last_connection_time = 0
_connection_delay = 2

def get_db_engine():
    global _engine, _last_connection_time
    current_time = time.time()
    elapsed = current_time - _last_connection_time
    if elapsed < _connection_delay:
        time.sleep(_connection_delay - elapsed)
    with _engine_lock:
        _last_connection_time = time.time()
        if _engine is not None:
            try:
                with _engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return _engine
            except OperationalError as e:
                logger.warning(f"Conexão inválida, recriando engine: {str(e)}")
                _engine.dispose()
                _engine = None
        try:
            connection_string = (
                f"mysql+pymysql://{DB_CONFIG['usuario']}:{DB_CONFIG['senha']}"
                f"@{DB_CONFIG['host']}:{DB_CONFIG['porta']}/{DB_CONFIG['banco']}"
                "?charset=utf8mb4&connect_timeout=10"
            )
            _engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=5,      
                max_overflow=10,   
                pool_timeout=30,
                pool_recycle=3600,
                pool_pre_ping=True,
                isolation_level="READ COMMITTED"
            )
            logger.info("Engine do banco de dados criado com sucesso")
            return _engine
        except SQLAlchemyError as e:
            logger.error(f"Falha crítica ao criar engine: {str(e)}")
            raise

def close_db_engine():
    global _engine
    if _engine is not None:
        try:
            _engine.dispose()
            logger.info("Engine do banco de dados descartado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao descartar engine: {str(e)}")
        finally:
            _engine = None
