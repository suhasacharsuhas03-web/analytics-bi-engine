from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create limiter instance
# Default: 30 requests per minute for all endpoints
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

def init_limiter(app):
    """
    Attach the limiter to the Flask app.
    Call this in app.py during setup.
    """
    limiter.init_app(app)
    return limiter