#!/bin/bash
# Flutter post-generation hook
# Installs basic Flutter packages based on API protocol

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up Flutter project dependencies...${NC}"

# Get variables from environment
PROJECT_NAME="${FLUTTER_PROJECT_NAME}"
API_PROTOCOL="${FLUTTER_API_PROTOCOL:-rest}"

# Validate project directory
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: PROJECT_NAME not set${NC}"
    exit 1
fi

if [ ! -d "$PROJECT_NAME" ]; then
    echo -e "${RED}Error: Project directory not found: $PROJECT_NAME${NC}"
    exit 1
fi

# Change to project directory
cd "$PROJECT_NAME"

echo -e "${BLUE}Installing common packages...${NC}"

# Common packages for all projects
COMMON_PACKAGES=(
    "provider"           # State management
    "shared_preferences" # Local storage
    "intl"              # Internationalization
)

# Install common packages
for package in "${COMMON_PACKAGES[@]}"; do
    echo -e "  ${YELLOW}→${NC} Adding $package..."
    flutter pub add "$package" > /dev/null 2>&1 || echo -e "    ${YELLOW}⚠${NC} Failed to add $package"
done

# Install API protocol specific packages
echo -e "${BLUE}Installing packages for API protocol: $API_PROTOCOL${NC}"

case "$API_PROTOCOL" in
    "rest")
        echo -e "  ${YELLOW}→${NC} Adding http..."
        flutter pub add http > /dev/null 2>&1 || echo -e "    ${YELLOW}⚠${NC} Failed to add http"
        
        echo -e "  ${YELLOW}→${NC} Adding dio..."
        flutter pub add dio > /dev/null 2>&1 || echo -e "    ${YELLOW}⚠${NC} Failed to add dio"
        ;;
        
    "graphql")
        echo -e "  ${YELLOW}→${NC} Adding graphql_flutter..."
        flutter pub add graphql_flutter > /dev/null 2>&1 || echo -e "    ${YELLOW}⚠${NC} Failed to add graphql_flutter"
        ;;
        
    "websocket")
        echo -e "  ${YELLOW}→${NC} Adding web_socket_channel..."
        flutter pub add web_socket_channel > /dev/null 2>&1 || echo -e "    ${YELLOW}⚠${NC} Failed to add web_socket_channel"
        ;;
        
    *)
        echo -e "${YELLOW}Unknown API protocol: $API_PROTOCOL${NC}"
        ;;
esac

# Install dev dependencies
echo -e "${BLUE}Installing dev dependencies...${NC}"

DEV_PACKAGES=(
    "flutter_lints"  # Linting
)

for package in "${DEV_PACKAGES[@]}"; do
    echo -e "  ${YELLOW}→${NC} Adding $package..."
    flutter pub add dev:"$package" > /dev/null 2>&1 || echo -e "    ${YELLOW}⚠${NC} Failed to add $package"
done

# Get dependencies
echo -e "${BLUE}Fetching dependencies...${NC}"
flutter pub get > /dev/null 2>&1

# Run flutter analyze to check for issues
echo -e "${BLUE}Analyzing project...${NC}"
if flutter analyze --no-fatal-infos > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Project analysis passed${NC}"
else
    echo -e "${YELLOW}⚠ Project has some analysis warnings (non-critical)${NC}"
fi

# Create basic directory structure for clean architecture
echo -e "${BLUE}Creating directory structure...${NC}"

DIRS=(
    "lib/core/constants"
    "lib/core/utils"
    "lib/features"
    "lib/shared/widgets"
    "lib/shared/models"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
    echo -e "  ${GREEN}✓${NC} Created $dir"
done

# Create .gitkeep files to preserve empty directories
for dir in "${DIRS[@]}"; do
    touch "$dir/.gitkeep"
done

echo -e "${GREEN}✓ Post-generation setup complete${NC}"
echo ""
echo -e "${BLUE}Your Flutter project is ready!${NC}"
echo -e "To get started:"
echo -e "  ${YELLOW}cd $PROJECT_NAME${NC}"
echo -e "  ${YELLOW}flutter run${NC}"
echo ""
echo -e "API Protocol: ${GREEN}$API_PROTOCOL${NC}"
echo -e "Packages installed based on your selection."