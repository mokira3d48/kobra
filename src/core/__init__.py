import logging  # Redirect ALL standard logging through Loguru..
from .logging import configure_logging, InterceptHandler  # Make sure this runs very early.

__version__ = '0.1.0'

configure_logging()

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

# Optional: silence noisy loggers or set them explicitly
logging.getLogger("django").setLevel("INFO")
logging.getLogger("django.request").setLevel("WARNING")
logging.getLogger("urllib3").setLevel("WARNING")
logging.getLogger("asyncio").setLevel("WARNING")
