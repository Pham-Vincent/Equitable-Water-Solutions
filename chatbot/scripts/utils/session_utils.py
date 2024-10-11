import uuid


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())
