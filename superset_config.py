# ---------------------------------------------------------
# Superset specific config
# ---------------------------------------------------------
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

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
    
    # Add debugging output
    print(f"Fetched secret: {secret}")

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


# Fetch the general secret
SECRET_KEY = get_secret('superset_secret_key', 'us-east-1')
 
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

# Branding
LOGO_TARGET_PATH = 'https://sites.lsa.umich.edu/dcc-project/the-reckoning-project/'
APP_NAME = 'The Reckoing Project'
APP_LOGO = 'app/logo/TheReckoningProject_logo.png'
WELCOME_MESSAGE = 'Welcome!'
