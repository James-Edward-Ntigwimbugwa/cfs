#!/bin/bash
# Django post-generation hook
# Installs dependencies and runs initial setup

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up Django project dependencies...${NC}"

# Get variables from environment
PROJECT_NAME="${DJANGO_PROJECT_NAME}"
DATABASE_ENGINE="${DJANGO_DATABASE_ENGINE:-postgresql}"
USE_GRAPHQL="${DJANGO_USE_GRAPHQL:-true}"
USE_CELERY="${DJANGO_USE_CELERY:-true}"

# Validate project directory
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: PROJECT_NAME not set${NC}"
    exit 1
fi

if [ ! -d "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: Project directory not found: $PROJECT_NAME${NC}"
    exit 1
fi

cd "$PROJECT_NAME"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found${NC}"
    exit 1
fi

source venv/bin/activate

echo -e "${BLUE}Installing core Django packages...${NC}"

# Core packages
CORE_PACKAGES=(
    "django"
    "djangorestframework"
    "django-cors-headers"
    "django-environ"
    "python-decouple"
    "psycopg2-binary"
    "Pillow"
    "python-dotenv"
    "django_celery_beat"
    "ldap3"

    "celery[redis]"  # Celery with Redis transport
    "redis"          # Redis client (often used by Celery)
    "geopy"          # Geocoding library
    "weasyprint"     # HTML to PDF generation
    "xmltodict"      # XML to dictionary conversion
    "pyAesCrypt"     # AES file encryption
    "graphene-django" #django_graphql
    "django-debug-toolbar" #debugger
    "django-oauth-toolkit" #oauth2
    "Jinja2" #Python Jinja
    "django-cors-middleware" #cors-middleware
    "django-cors-headers>=4.3,<5.0"
)
for package in "${CORE_PACKAGES[@]}"; do
    echo -e "  ${YELLOW}→${NC} Installing $package..."
    if pip install "$package" > /dev/null 2>&1; then
        echo -e "    ${GREEN}✓${NC} Installed $package"
    else
        echo -e "    ${YELLOW}⚠${NC} Failed to install $package"
    fi
done

# Database-specific packages
echo -e "${BLUE}Installing database adapter for $DATABASE_ENGINE...${NC}"
case "$DATABASE_ENGINE" in
    "postgresql")
        pip install psycopg2-binary > /dev/null 2>&1 && echo -e "${GREEN}✓ PostgreSQL adapter installed${NC}"
        ;;
    "mysql")
        pip install mysqlclient > /dev/null 2>&1 && echo -e "${GREEN}✓ MySQL adapter installed${NC}"
        ;;
    "sqlite")
        echo -e "${GREEN}✓ SQLite (built-in)${NC}"
        ;;
esac

# GraphQL packages
if [ "$USE_GRAPHQL" = "true" ]; then
    echo -e "${BLUE}Installing GraphQL packages...${NC}"
    GRAPHQL_PACKAGES=(
        "graphene-django"
        "django-graphql-jwt"
        "graphene-file-upload"
    )

    for package in "${GRAPHQL_PACKAGES[@]}"; do
        echo -e "  ${YELLOW}→${NC} Installing $package..."
        if pip install "$package" > /dev/null 2>&1; then
            echo -e "    ${GREEN}✓${NC} Installed $package"
        else
            echo -e "    ${YELLOW}⚠${NC} Failed to install $package"
        fi
    done
fi

# Celery packages
if [ "$USE_CELERY" = "true" ]; then
    echo -e "${BLUE}Installing Celery packages...${NC}"
    CELERY_PACKAGES=(
        "celery"
        "redis"
        "django-celery-beat"
        "django-celery-results"
    )

    for package in "${CELERY_PACKAGES[@]}"; do
        echo -e "  ${YELLOW}→${NC} Installing $package..."
        if pip install "$package" > /dev/null 2>&1; then
            echo -e "    ${GREEN}✓${NC} Installed $package"
        else
            echo -e "    ${YELLOW}⚠${NC} Failed to install $package"
        fi
    done
fi

# Additional utility packages
echo -e "${BLUE}Installing utility packages...${NC}"
UTIL_PACKAGES=(
    "requests"
    "PyJWT"
    "python-multipart"
    "gunicorn"
    "whitenoise"
    "django-redis"
)

for package in "${UTIL_PACKAGES[@]}"; do
    echo -e "  ${YELLOW}→${NC} Installing $package..."
    if pip install "$package" > /dev/null 2>&1; then
        echo -e "    ${GREEN}✓${NC} Installed $package"
    else
        echo -e "    ${YELLOW}⚠${NC} Failed to install $package"
    fi
done

# Development packages
echo -e "${BLUE}Installing development packages...${NC}"
DEV_PACKAGES=(
    "black"
    "flake8"
    "pytest"
    "pytest-django"
    "factory-boy"
    "faker"
)

for package in "${DEV_PACKAGES[@]}"; do
    echo -e "  ${YELLOW}→${NC} Installing $package..."
    if pip install "$package" > /dev/null 2>&1; then
        echo -e "    ${GREEN}✓${NC} Installed $package"
    else
        echo -e "    ${YELLOW}⚠${NC} Failed to install $package"
    fi
done

# Generate requirements.txt
echo -e "${BLUE}Generating requirements.txt...${NC}"
pip freeze > requirements.txt
echo -e "${GREEN}✓ requirements.txt generated${NC}"

# Check if manage.py exists before running migrations
if [ -f "manage.py" ]; then
    echo -e "${BLUE}Running initial migrations...${NC}"
    if python manage.py makemigrations > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Migrations created${NC}"
    else
        echo -e "${YELLOW}⚠ No migrations to create${NC}"
    fi

    if python manage.py migrate > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Migrations applied${NC}"
    else
        echo -e "${YELLOW}⚠ Could not apply migrations (database not configured yet)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ manage.py not found, skipping migrations${NC}"
fi

# Deactivate virtual environment
deactivate

echo -e "${GREEN}✓ Post-generation setup complete${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Your Django project is ready!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Architecture:${NC}"
echo -e "  • Modular Django apps with clean separation"
echo -e "  • GraphQL API with Graphene-Django"
echo -e "  • Celery for async task processing"
echo -e "  • Redis for caching and message broker"
echo ""
echo -e "${YELLOW}Django Apps Created:${NC}"
echo -e "  • ${PACKAGE_NAME}_auth - Authentication & user management"
echo -e "  • ${PACKAGE_NAME}_audit_logs - Audit logging"
echo -e "  • ${PACKAGE_NAME}_notifications - Notification system"
echo -e "  • ${PACKAGE_NAME}_settings - App settings & configuration"
echo -e "  • ${PACKAGE_NAME}_files - File management"
echo -e "  • ${PACKAGE_NAME}_cache_core - Caching utilities"
echo ""
echo -e "${YELLOW}To get started:${NC}"
echo -e "  ${GREEN}cd $PROJECT_NAME${NC}"
echo -e "  ${GREEN}source venv/bin/activate${NC}"
echo -e "  ${GREEN}# Configure .env file with database credentials${NC}"
echo -e "  ${GREEN}python manage.py runserver${NC}"
echo ""
echo -e "${YELLOW}Key files to configure:${NC}"
echo -e "  • .env - Environment variables & secrets"
echo -e "  • ${PACKAGE_NAME}_backend/settings/base.py - Django settings"
echo -e "  • ${PACKAGE_NAME}_backend/urls.py - URL routing"
echo ""
echo -e "${YELLOW}Database: ${GREEN}$DATABASE_ENGINE${NC}"
echo -e "${YELLOW}GraphQL: ${GREEN}$USE_GRAPHQL${NC}"
echo -e "${YELLOW}Celery: ${GREEN}$USE_CELERY${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"