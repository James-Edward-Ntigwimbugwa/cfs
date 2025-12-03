#!/bin/bash
# Flutter post-generation hook
# Installs packages for GraphQL, routing, and state management

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
# shellcheck disable=SC2034
API_PROTOCOL="${FLUTTER_API_PROTOCOL:-graphql}"

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

echo -e "${BLUE}Installing core packages...${NC}"

# Core packages for GraphQL + go_router architecture
CORE_PACKAGES=(
    "graphql_flutter"       # GraphQL client
    "go_router"            # Declarative routing
    "provider"             # State management
    "shared_preferences"   # Local storage
    "intl"                # Internationalization
    "flutter_dotenv"      # Environment variables
    "equatable"           # Value equality
    "toastification"      #toastnotification
    "flutter_secure_storage" #flutter_secure_storage
    "sizer"               #sizer_package
    "hugeicons"           #hugeicons
    "image_picker"
    "flutter_platform_widgets"
    "flutter_spinkit"
    "syncfusion_flutter_charts"
    "device_safety_info"
    "get_it"
)

# Install core packages
for package in "${CORE_PACKAGES[@]}"; do
    echo -e "  ${YELLOW}→${NC} Adding $package..."
    if flutter pub add "$package" > /dev/null 2>&1; then
        echo -e "    ${GREEN}✓${NC} Added $package"
    else
        echo -e "    ${YELLOW}⚠${NC} Failed to add $package"
    fi
done

# Install dev dependencies
echo -e "${BLUE}Installing dev dependencies...${NC}"

DEV_PACKAGES=(
    "flutter_lints"       # Linting
    "build_runner"        # Code generation
)

for package in "${DEV_PACKAGES[@]}"; do
    echo -e "  ${YELLOW}→${NC} Adding $package..."
    if flutter pub add dev:"$package" > /dev/null 2>&1; then
        echo -e "    ${GREEN}✓${NC} Added $package"
    else
        echo -e "    ${YELLOW}⚠${NC} Failed to add $package"
    fi
done

# Get dependencies
echo -e "${BLUE}Fetching dependencies...${NC}"
if flutter pub get > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Dependencies fetched successfully${NC}"
else
    echo -e "${YELLOW}⚠ Some dependencies may have issues${NC}"
fi

# Update pubspec.yaml to include assets
echo -e "${BLUE}Configuring assets in pubspec.yaml...${NC}"

# Add flutter_dotenv configuration
if ! grep -q "flutter_dotenv" pubspec.yaml; then
    echo -e "${YELLOW}Note: Add .env to assets in pubspec.yaml manually if needed${NC}"
fi

# Run flutter analyze to check for issues
echo -e "${BLUE}Analyzing project...${NC}"
if flutter analyze --no-fatal-infos > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Project analysis passed${NC}"
else
    echo -e "${YELLOW}⚠ Project has some analysis warnings (non-critical)${NC}"
fi

# Format the generated code
echo -e "${BLUE}Formatting code...${NC}"
if dart format lib/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Code formatted${NC}"
else
    echo -e "${YELLOW}⚠ Code formatting had some issues${NC}"
fi

echo -e "${GREEN}✓ Post-generation setup complete${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Your Flutter project is ready!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Architecture:${NC}"
echo -e "  • Modular structure with feature-based organization"
echo -e "  • GraphQL integration with graphql_flutter"
echo -e "  • go_router for declarative navigation"
echo -e "  • Provider for state management"
echo ""
echo -e "${YELLOW}Demo Modules:${NC}"
echo -e "  • Authentication module with login/signup"
echo -e "  • Onboarding module with splash screen"
echo -e "  • Clean architecture (data/presentation/routes)"
echo ""
echo -e "${YELLOW}To get started:${NC}"
echo -e "  ${GREEN}cd $PROJECT_NAME${NC}"
echo -e "  ${GREEN}# Update .env.example with your GraphQL endpoint${NC}"
echo -e "  ${GREEN}# Copy .env.example to .env${NC}"
echo -e "  ${GREEN}flutter run${NC}"
echo ""
echo -e "${YELLOW}Key files to configure:${NC}"
echo -e "  • .env - Environment variables"
echo -e "  • lib/core/constants/api_constants.dart - API endpoints"
echo -e "  • lib/core/api_config/graphql_config.dart - GraphQL client"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"