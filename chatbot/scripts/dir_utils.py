from pathlib import Path

def find_project_root(this_dir: Path) -> Path:
    """Recursively search for project root directory.
    
    Define root as the directory containing a .git directory.
    
    Args:
        this_dir (Path): The directory to start the search from.
        
    Returns:
        Path: The path to the project root directory.
        
    Raises:
        FileNotFoundError: If the project root directory is not found.
    """
    while this_dir != this_dir.parent:
        if (this_dir / '.git').exists():
            return this_dir
        this_dir = this_dir.parent
        
    raise FileNotFoundError("Could not find project root")

def find_env_file(root_dir: Path) -> Path:
    """Recursively search for .env file in project.
    
    Args:
        root_dir (Path): The root directory of the project.
        
    Returns:
        Path: The path to the .env file.
        
    Raises:
        FileNotFoundError: If the .env file is not found.
    """
    for path in root_dir.rglob('.env'):
        return path
    raise FileNotFoundError("Could not find .env file")

def get_vector_db_dir(start_dir: Path, target_dir: str) -> Path:
    """Recursively search for target directory.
    
    Intended to start at chatbot/ directory from the makeVDB.py script and find the VectorDB directory.
    
    Args:
        start_dir (Path): The directory to start the search from.
        target_dir (str): The name of the target directory.
        
    Returns:
        Path: The path to the target directory.
        
    Raises:
        FileNotFoundError: If the target directory is not found.
    """
    while start_dir != start_dir.parent:
        if (start_dir / target_dir).exists():
            return start_dir / target_dir
        start_dir = start_dir.parent
    raise FileNotFoundError(f"Could not find {target_dir} directory")
    