from datetime import timedelta

from pathlib import Path
import os
import environ
from dotenv import load_dotenv
import sys
import dj_database_url

# Define BASE_DIR before using it
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv()

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Only in development
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",
    ]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    # for security
    'axes',
    # apis
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',

    # my apps
    'users',
    'transactions',
    'goals',
    'notifications',
    'mpesa',
    'analytics',
    'budget',
    'testimonials',
    'core',
    'wallet',
]

SITE_ID = 1  # Add this line

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesStandaloneBackend',
)

# login security
AXES_FAILURE_LIMIT = 5  
AXES_COOLOFF_TIME = 1  


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# admin dashborad - Jazzmin Configuration
JAZZMIN_SETTINGS = {
    # Site Information
    "site_title": "Mo-Wallet Admin",
    "site_header": "Mo-Wallet Admin Dashboard",
    "site_brand": "Mo-Wallet",
    "site_logo": None,  # Add path to your logo image if available
    "login_logo": None,
    "welcome_sign": "Welcome to Mo-Wallet Admin Dashboard 🚀",
    "copyright": "© 2024 Mo-Wallet by PurpleStack",
    
    # UI Configuration
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["rest_framework"],  # Hide DRF admin
    "hide_models": [],
    
    # App Ordering
    "order_with_respect_to": [
        "users",
        "transactions",
        "budget",
        "goals",
        "wallet",
        "mpesa",
        "analytics",
        "notifications",
        "testimonials",
        "core",
        "auth",
    ],
    
    # App Icons - Enhanced with more comprehensive coverage
    "app_icons": {
        "users": "fas fa-users",
        "transactions": "fas fa-exchange-alt",
        "budget": "fas fa-coins",
        "goals": "fas fa-piggy-bank",
        "wallet": "fas fa-wallet",
        "mpesa": "fas fa-mobile-alt",
        "analytics": "fas fa-chart-bar",
        "notifications": "fas fa-bell",
        "testimonials": "fas fa-comment-dots",
        "core": "fas fa-cog",
        "auth": "fas fa-lock",
    },
    
    # Model Icons - Detailed icons for each model
    "icons": {
        "auth.user": "fas fa-user-shield",
        "auth.group": "fas fa-users-cog",
        "auth.permission": "fas fa-lock-open",
        "users.user": "fas fa-user-shield",
        "users.profile": "fas fa-id-badge",
        "transactions.transaction": "fas fa-exchange-alt",
        "budget.budget": "fas fa-coins",
        "goals.savingsgoal": "fas fa-piggy-bank",
        "goals.goalcontribution": "fas fa-hand-holding-usd",
        "wallet.wallet": "fas fa-wallet",
        "wallet.paymentmethod": "fas fa-credit-card",
        "wallet.prediction": "fas fa-crystal-ball",
        "wallet.invoice": "fas fa-file-invoice",
        "wallet.bill": "fas fa-receipt",
        "mpesa.mpesatransaction": "fas fa-mobile-alt",
        "analytics.analytics": "fas fa-chart-bar",
        "notifications.notification": "fas fa-bell",
        "testimonials.testimonial": "fas fa-comment-dots",
    },
    
    # Custom Links
    "custom_links": {
        "users": [
            {
                "name": "User Reports",
                "url": "/admin/",
                "icon": "fas fa-file-pdf",
                "permissions": ["auth.view_user"],
            }
        ],
        "transactions": [
            {
                "name": "Transaction Reports",
                "url": "/admin/",
                "icon": "fas fa-file-export",
                "permissions": ["transactions.view_transaction"],
            }
        ],
    },
    
    # Search Bar Configuration
    "search_model": ["users.User", "transactions.Transaction"],
    
    # Related Model Configuration
    "related_modal_active": True,
    "show_ui_builder": DEBUG,  # Only show UI builder in development
    
    # Default Icon Pack - Font Awesome 6
    "default_icon_parents": "fas fa-chevron-right",
    "default_icon_children": "fas fa-arrow-right",
    
    # Collapse on Modal Toggle
    "collapse_on_modal_toggle": True,
    
    # Show Admin Object Permissions
    "show_model_permissions": True,
}

JAZZMIN_UI_TWEAKS = {
    # Theme selection - "default", "flatly", "cosmo", "cyborg", "darkly", "journal", 
    # "litera", "lumen", "lux", "materia", "minty", "pulse", "sandstone", "simplex", 
    # "slate", "solar", "spacelab", "superhero", "united", "yeti"
    "theme": "darkly",
    "dark_mode_theme": "slate",
    
    # Navbar styling
    "navbar": "navbar-dark navbar-expand-md",
    "navbar_fixed": False,
    "sidebar": "sidebar-dark-purple",
    "sidebar_fixed": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_granular_toggle": True,
    "sidebar_disable_expand": False,
    
    # Accent color
    "accent": "accent-purple",
    "brand_colour": "navbar-purple",
    
    # Text sizing
    "body_small_text": False,
    "body_medium_text": False,
    "footer_small_text": False,
    "navbar_small_text": False,
    "sidebar_small_text": True,
    "sidebar_nav_small_text": True,
    
    # Horizontal layout
    "layout_boxed": False,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

ROOT_URLCONF = 'Mowallet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notifications_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'Mowallet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if os.getenv('DATABASE_URL'):
    # Production: Use PostgreSQL (Railway automatically sets DATABASE_URL)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Use SQLite for testing to avoid PostgreSQL collation issues
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Mpesa API credentials
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT')

SESSION_COOKIE_AGE = 1800  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

# Authentication settings
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
