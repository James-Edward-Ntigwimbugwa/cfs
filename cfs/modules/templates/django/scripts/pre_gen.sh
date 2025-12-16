#!/bin/bash
# Django pre-generation hook
# Creates Django project and initial apps

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating Django project...${NC}"

# Get variables from environment
PROJECT_NAME="${DJANGO_PROJECT_NAME}"
PACKAGE_NAME="${DJANGO_PACKAGE_NAME}"
DATABASE_ENGINE="${DJANGO_DATABASE_ENGINE:-postgresql}"
PYTHON_VERSION="${DJANGO_PYTHON_VERSION:-3.11}"

# Validate required variables
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: PROJECT_NAME not set${NC}"
    exit 1
fi

if [ -z "$PACKAGE_NAME" ]; then
    echo -e "${RED}Error: PACKAGE_NAME not set${NC}"
    exit 1
fi

echo -e "${BLUE}Project details:${NC}"
echo -e "  Name: ${GREEN}$PROJECT_NAME${NC}"
echo -e "  Package: ${GREEN}$PACKAGE_NAME${NC}"
echo -e "  Database: ${GREEN}$DATABASE_ENGINE${NC}"
echo -e "  Python: ${GREEN}$PYTHON_VERSION${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    echo "Please install Python from: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
echo -e "${BLUE}Python version:${NC}"
python3 --version

# Create project directory
echo -e "${BLUE}Creating project directory: $PROJECT_NAME${NC}"
if [ -d "$PROJECT_NAME" ]; then
    echo -e "${YELLOW} Project directory already exists${NC}"
else
    mkdir -p "$PROJECT_NAME"
    echo -e "${GREEN}✓ Project directory created${NC}"
fi

cd "$PROJECT_NAME"

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install Django
echo -e "${BLUE}Installing Django...${NC}"
pip install django > /dev/null 2>&1
echo -e "${GREEN}✓ Django installed${NC}"

# Create Django project structure
echo -e "${BLUE}Creating Django project structure...${NC}"

# List of Django apps to create based on manifest
APPS=(
    "${PACKAGE_NAME}_assets"
    "${PACKAGE_NAME}_audit_logs"
    "${PACKAGE_NAME}_auth"
    "${PACKAGE_NAME}_cache_core"
    "${PACKAGE_NAME}_notifications"
    "${PACKAGE_NAME}_settings"
    "${PACKAGE_NAME}_files"
)

# Create each app
for app in "${APPS[@]}"; do
    if [ -d "$app" ]; then
        echo -e "${YELLOW}  App $app already exists${NC}"
    else
        echo -e "  ${BLUE}→${NC} Creating app: $app"
        django-admin startapp "$app" > /dev/null 2>&1
        echo -e "    ${GREEN}✓${NC} Created $app"
    fi
done

# Create non-app directories
echo -e "${BLUE}Creating utility directories...${NC}"

UTIL_DIRS=(
    "${PACKAGE_NAME}_dto"
    "${PACKAGE_NAME}_dto_builders"
    "${PACKAGE_NAME}_mixins"
    "${PACKAGE_NAME}_htmls"
    "${PACKAGE_NAME}_utils"

)

for dir in "${UTIL_DIRS[@]}"; do
    mkdir -p "$dir"
    touch "$dir/__init__.py" 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Created $dir"
done

# Create nested utility directories
mkdir -p "${PACKAGE_NAME}_utils/cache"
mkdir -p "${PACKAGE_NAME}_utils/decorators"
mkdir -p "${PACKAGE_NAME}_utils/validators"

# Create __init__.py files
find "${PACKAGE_NAME}_utils" -type d -exec touch {}/__init__.py \; 2>/dev/null || true

echo -e "${GREEN}✓ Django project structure created${NC}"

# Deactivate virtual environment
deactivate

cd ..

echo -e "${GREEN}✓ Pre-generation setup complete${NC}"