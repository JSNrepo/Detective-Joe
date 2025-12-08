#!/bin/bash
# Detective Joe v1.5 - Tool Installation Script for Kali Linux
# This script helps install all required reconnaissance tools

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         Detective Joe v1.5 - Tool Installation              ║"
echo "║              Kali Linux Setup Assistant                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  Warning: This script is optimized for Kali Linux"
    echo "   It may work on other Debian-based systems but is not guaranteed."
    read -p "   Continue anyway? (y/N): " choice
    if [[ ! "$choice" =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Check if running with sudo/root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script requires root privileges to install system packages."
    echo "   Please run with: sudo ./install_tools.sh"
    exit 1
fi

echo "📦 Installing reconnaissance tools..."
echo ""

# Update package lists
echo "🔄 Updating package lists..."
apt update -qq

# Install basic system tools (usually already present)
echo "✓ Installing core tools (nmap, whois, dnsutils)..."
apt install -y nmap whois dnsutils > /dev/null 2>&1 || echo "⚠️  Some core tools may already be installed"

# Install SSL/TLS tools
echo "✓ Installing SSL/TLS analysis tools (sslscan)..."
apt install -y sslscan > /dev/null 2>&1 || echo "⚠️  sslscan may already be installed"

# Install DNSRecon
echo "✓ Installing DNS enumeration tools (dnsrecon)..."
apt install -y dnsrecon > /dev/null 2>&1 || echo "⚠️  dnsrecon may already be installed"

# Install theHarvester
echo "✓ Installing OSINT tools (theharvester)..."
apt install -y theharvester > /dev/null 2>&1 || {
    echo "⚠️  theHarvester not found in apt, trying pip..."
    su - $SUDO_USER -c "pip3 install theHarvester" > /dev/null 2>&1 || echo "⚠️  Failed to install theHarvester via pip"
}

# Install Sublist3r
echo "✓ Installing subdomain enumeration tools (sublist3r)..."
apt install -y sublist3r > /dev/null 2>&1 || {
    echo "⚠️  Sublist3r not found in apt, trying pip..."
    su - $SUDO_USER -c "pip3 install sublist3r" > /dev/null 2>&1 || echo "⚠️  Failed to install Sublist3r via pip"
}

# Install WhatWeb
echo "✓ Installing web fingerprinting tools (whatweb)..."
apt install -y whatweb > /dev/null 2>&1 || echo "⚠️  whatweb may already be installed"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Tool installation completed!"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Verify installations
echo "🔍 Verifying tool installations..."
echo ""

tools=("nmap" "whois" "dnsrecon" "sslscan" "theharvester" "sublist3r" "whatweb")
missing_tools=()

for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        version=$(command -v "$tool")
        echo "  ✓ $tool: $version"
    else
        echo "  ✗ $tool: NOT FOUND"
        missing_tools+=("$tool")
    fi
done

echo ""

if [ ${#missing_tools[@]} -eq 0 ]; then
    echo "🎉 All tools successfully installed!"
    echo ""
    echo "Next steps:"
    echo "  1. Exit root: exit"
    echo "  2. Activate virtual environment: source .venv/bin/activate"
    echo "  3. Run Detective Joe: python3 detectivejoe.py --list-plugins"
    echo "  4. Start investigating: python3 detectivejoe.py -c website -t example.com"
else
    echo "⚠️  Warning: Some tools could not be installed:"
    for tool in "${missing_tools[@]}"; do
        echo "     - $tool"
    done
    echo ""
    echo "You can still use Detective Joe with available tools."
    echo "To install missing tools manually, refer to:"
    echo "  - theHarvester: git clone https://github.com/laramies/theHarvester"
    echo "  - Sublist3r: git clone https://github.com/aboul3la/Sublist3r"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
