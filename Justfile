# Default recipe to run when just is called without arguments
default:
    @just --list

# Start the development server
dev:
    npm run dev

# Install dependencies
install:
    npm install

# Build the project
build:
    npm run build

# Start the production server
start:
    npm run preview

# Clean build artifacts
clean:
    rm -rf dist
    rm -rf node_modules

# Run tests
test:
    npm test

# Format code
format:
    npm run format

# Lint code
lint:
    npm run lint 