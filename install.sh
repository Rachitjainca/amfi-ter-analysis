#!/bin/bash
# AMFI TER Analysis - Installation Script

echo "=========================================="
echo "AMFI TER Analysis - Package Installation"
echo "=========================================="

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if Python 3.8+
if ! python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python 3.8 or higher is required"
    exit 1
fi

# Install from PyPI
echo ""
echo "Installing amfi-ter-analysis from PyPI..."
pip install amfi-ter-analysis

# Verify installation
echo ""
echo "Verifying installation..."
if python -c "from amfi_ter_analysis import download_ter_file, read_ter_file, analyze_ter_changes"; then
    echo "✅ Installation successful!"
    echo ""
    echo "Quick start:"
    echo "  python -c \"from amfi_ter_analysis import download_ter_file; download_ter_file(2, 2026)\""
else
    echo "❌ Installation failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "For usage examples, see:"
echo "  https://github.com/Rachitjainca/amfi-ter-analysis#readme"
echo "=========================================="
