# ---------------------------------------------------------
# Superset specific config
# ---------------------------------------------------------

# Set row limit for improved performance
ROW_LIMIT = 5000

# Set number of workers
SUPERSET_WORKERS = 4

# Set Secret Key
SECRET_KEY = 'ACpAhrXUZDkY1WH73qR0ZQ'

# 
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