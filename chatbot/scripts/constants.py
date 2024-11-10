from pathlib import Path
from .dir_utils import get_vector_db_dir

_this_dir = Path(__file__).parent
_vector_db_parent_dir = get_vector_db_dir(start_dir=_this_dir, target_dir="VectorDB")
VECTOR_DB_DIR = _vector_db_parent_dir / "vectordb"
