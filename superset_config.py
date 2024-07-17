# ---------------------------------------------------------
# Superset specific config
# ---------------------------------------------------------
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name):

    region_name = 'us-east-1'

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
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

# Example usage
SECRET_KEY = get_secret('superset_secret_key', 'us-east-1')

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

# Fetch admin user details from AWS Secrets Manager
admin_secrets = get_secret('superset_admin_config')

# Ensure all required admin secrets are available
required_admin_keys = ['admin_username', 'admin_firstname', 'admin_lastname', 'admin_email', 'admin_password']
missing_keys = [key for key in required_admin_keys if key not in admin_secrets]
if missing_keys:
    raise RuntimeError(f"Missing required admin secrets: {', '.join(missing_keys)}")

ADMIN_USERNAME = admin_secrets['admin_username']
ADMIN_FIRSTNAME = admin_secrets['admin_firstname']
ADMIN_LASTNAME = admin_secrets['admin_lastname']
ADMIN_EMAIL = admin_secrets['admin_email']
ADMIN_PASSWORD = admin_secrets['admin_password']