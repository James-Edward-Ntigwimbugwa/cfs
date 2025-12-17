#!/bin/bash
# Flutter pre-generation hook
# Creates a Flutter project using flutter create command

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating Flutter project...${NC}"

# Get variables from environment
PROJECT_NAME="${FLUTTER_PROJECT_NAME}"
PACKAGE_NAME="${FLUTTER_PACKAGE_NAME}"

# Validate required variables
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: PROJECT_NAME not set${NC}"
    exit 1
fi

if [ -z "$PACKAGE_NAME" ]; then
    echo -e "${RED}Error: PACKAGE_NAME not set${NC}"
    exit 1
fi

# Extract organization from package name (e.g., com.example.app -> com.example)
# Flutter --org expects reverse domain notation without the app name
ORG_PARTS=$(echo "$PACKAGE_NAME" | tr '.' '\n' | head -n -1 | paste -sd '.')

if [ -z "$ORG_PARTS" ]; then
    # If no dots in package name, use it as is
    ORG="$PACKAGE_NAME"
else
    ORG="$ORG_PARTS"
fi

echo -e "${BLUE}Project details:${NC}"
echo -e "  Name: ${GREEN}$PROJECT_NAME${NC}"
echo -e "  Package: ${GREEN}$PACKAGE_NAME${NC}"
echo -e "  Organization: ${GREEN}$ORG${NC}"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo -e "${RED}Error: Flutter is not installed or not in PATH${NC}"
    echo "Please install Flutter from: https://flutter.dev/docs/get-started/install"
    exit 1
fi

# Check Flutter version
echo -e "${BLUE}Flutter version:${NC}"
flutter --version | head -n 1

# Create Flutter project with organization
echo -e "${BLUE}Running: flutter create --org $ORG $PROJECT_NAME${NC}"

# Run flutter create
if flutter create --org "$ORG" "$PROJECT_NAME"; then
    echo -e "${GREEN}✓ Flutter project created successfully${NC}"
else
    echo -e "${RED}✗ Failed to create Flutter project${NC}"
    exit 1
fi

# Verify project was created
if [ ! -d "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: Project directory was not created${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-generation setup complete${NC}"