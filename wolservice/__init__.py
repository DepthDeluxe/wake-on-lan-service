from .app import app
from .config import load_config_from_file, load_default_configuration
import wolservice.api as api
    
try:
    load_config_from_file(app)
except ValueError:
    load_default_configuration(app)

import wolservice.models as models