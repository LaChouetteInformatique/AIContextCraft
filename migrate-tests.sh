#!/bin/bash
# Script to migrate to simplified test structure

set -e

echo "🔄 Migrating to simplified test structure..."

# Backup current tests
echo "📦 Creating backup..."
cp -r tests tests_backup_$(date +%Y%m%d_%H%M%S)

# Remove unnecessary files
echo "🗑️  Removing redundant files..."
rm -rf tests/test_runner.py
rm -rf tests/test_groups/
rm -f tests/test_example.py
rm -f tests/Dockerfile.test
rm -f tests/requirements-test.txt
rm -f docker-compose.test.yml
rm -f run-tests.sh
rm -f create-test-structure.sh

# Keep only essential files
echo "✅ Keeping essential files:"
ls tests/test*.py tests/*.sh tests/pytest.ini tests/conftest.py 2>/dev/null || true

# Clean Docker
echo "🐳 Cleaning Docker..."
docker rmi aicc-test-runner:latest 2>/dev/null || true

echo ""
echo "✨ Migration complete!"
echo ""
echo "📝 Next steps:"
echo "1. Replace Dockerfile with the fixed version"
echo "2. Replace Makefile with the simplified version"
echo "3. Copy test_aicontextcraft.py from the artifacts"
echo "4. Run: make clean-all && make test"
echo ""
echo "🎯 New test commands:"
echo "  make test           # All tests"
echo "  make test-quick     # Quick tests"
echo "  make test-basic     # Basic tests only"
echo "  make test-features  # Feature tests only"
echo "  make test-one TEST=test_name  # One specific test"
echo ""