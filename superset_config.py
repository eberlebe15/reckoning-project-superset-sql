# ---------------------------------------------------------
# Superset specific config
# ---------------------------------------------------------
import logging
from logging.handlers import TimedRotatingFileHandler
import json
import base64
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from cachelib.redis import RedisCache

# Ensure the log directory exists
log_dir = '/var/log/superset'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure Logging
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        TimedRotatingFileHandler(
            os.path.join(log_dir, 'superset.log'),
            when="midnight",
            backupCount=30
        )
    ]
)

# AWS Secret Manager get_secret function
def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise RuntimeError(f"AWS credentials error: {str(e)}")
    except client.exceptions.ResourceNotFoundException:
        raise RuntimeError(f"Secret {secret_name} not found")
    except client.exceptions.ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Ensure we return the parsed JSON
    return json.loads(secret)

superset_metadata_config = get_secret('superset_metadata_config', 'us-east-1')
superset_metadata_username = superset_metadata_config['username']
superset_metadata_password = superset_metadata_config['password']
superset_metadata_host = superset_metadata_config['host']
superset_metadata_port = superset_metadata_config['port']
superset_metadata_name = superset_metadata_config['dbInstanceIdentifier']

# Construct the SQLAlchemy connection string for MySQL
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{superset_metadata_username}:{superset_metadata_password}@{superset_metadata_host}:{superset_metadata_port}/{superset_metadata_name}"

# Rotate previous secret key
PREVIOUS_SECRET_KEY = get_secret('superset_old_secret_key', 'us-east-1')

# Fetch the general secret
SECRET_KEY = get_secret('superset_secret_key', 'us-east-1')

# Handle binary secret
decoded_secret = base64.b64decode(secret_string).decode('utf-8')
secret_data = json.loads(decoded_secret)
 
# Fetch admin user details from AWS Secrets Manager
admin_secrets = get_secret('superset_admin_config', 'us-east-1')
ADMIN_USERNAME = admin_secrets['superset_admin_username']
ADMIN_FIRSTNAME = admin_secrets['superset_admin_firstname']
ADMIN_LASTNAME = admin_secrets['superset_admin_lastname']
ADMIN_EMAIL = admin_secrets['superset_admin_email']
ADMIN_PASSWORD = admin_secrets['superset_admin_password']

# Set row limit for improved performance
ROW_LIMIT = 5000

# Set number of workers
SUPERSET_WORKERS = 4

# Set Cookie Session Settings
SESSION_COOKIE_SAMESITE = None  # One of [None, 'Lax', 'Strict']

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = False

# Allow ADHOC Subqueries
ALLOW_ADHOC_SUBQUERY=True

# Production Mode
WTF_CSRF_ENABLED = True

# Configure Flask-AppBuilder
ENABLE_TIME_ROTATE = True

# Configure Redis Cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 0,
    'CACHE_REDIS_URL': None,
}

DATA_CACHE_CONFIG = CACHE_CONFIG
RESULTS_BACKEND = CACHE_CONFIG

# Branding
LOGO_TARGET_PATH = 'https://sites.lsa.umich.edu/dcc-project/the-reckoning-project/'
APP_NAME = 'The Reckoing Project'
APP_LOGO = 'app/logo/TheReckoningProject_logo.png'
WELCOME_MESSAGE = 'Welcome!'
