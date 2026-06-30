# DEPRECATED: This file is kept for backward compatibility
# Use config/settings/development.py or config/settings/production.py instead

from decouple import config
import os

# Determine which settings to use
ENVIRONMENT = config('DJANGO_SETTINGS_MODULE', default='config.settings.development')

if 'production' in ENVIRONMENT:
    from .settings.production import *
else:
    from .settings.development import *
