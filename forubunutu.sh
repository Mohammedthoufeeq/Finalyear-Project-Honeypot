#!/bin/bash

# ---------------------------------------------------------------------------
# Script Name   : configure_python_alias.sh
# Purpose       : Ensure `python` command maps to `python3` on Ubuntu systems
#
# Context:
#   - By default, Ubuntu does not link the `python` command to `python3`.
#   - Many tools, scripts, and environments (including honeypots and legacy apps)
#     still expect the `python` command to exist.
#   - This script safely configures the `python` command to point to `python3`
#     using the system's `update-alternatives` mechanism.
#
# Use Cases:
#   - Honeypot systems requiring `python` for startup scripts
#   - Lab setups where older tools call `python` but only `python3` is available
#   - Preventing command-not-found issues for scripts expecting `/usr/bin/python`
#
# Actions:
#   - Checks for existing `python3` installation
#   - Warns if `python` already points to a different binary
#   - Uses `update-alternatives` to safely configure `python` → `python3`
#   - Verifies and logs success or failure
#
# Author        : Senior DevOps Automation Style
# Compatibility : Ubuntu 18.04, 20.04, 22.04, 24.04+
# ---------------------------------------------------------------------------

set -euo pipefail

log() {
    echo -e "[INFO] $*"
}

warn() {
    echo -e "[WARN] $*" >&2
}

error() {
    echo -e "[ERROR] $*" >&2
    exit 1
}

check_python3_exists() {
    if ! command -v python3 >/dev/null 2>&1; then
        error "python3 is not installed. Please install it first: sudo apt install python3"
    fi
}

check_existing_python_cmd() {
    if command -v python >/dev/null 2>&1; then
        current_path=$(readlink -f "$(command -v python)")
        log "Current 'python' points to: $current_path"
        if [[ "$current_path" == "$(command -v python3)" ]]; then
            log "'python' already points to 'python3'. No action needed."
            exit 0
        else
            warn "'python' points to something other than 'python3'."
            echo "Configuring update-alternatives to safely override this."
        fi
    else
        log "'python' command not found. It will be created via update-alternatives."
    fi
}

configure_update_alternatives() {
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1

    python_alternatives=$(update-alternatives --list python 2>/dev/null || true)
    if [[ -n "$python_alternatives" ]]; then
        log "Available python alternatives:"
        echo "$python_alternatives"
        log "Setting /usr/bin/python3 as the default for 'python'..."
        sudo update-alternatives --set python /usr/bin/python3
    fi
}

verify_python_alias() {
    resolved=$(readlink -f "$(command -v python)")
    expected=$(command -v python3)

    if [[ "$resolved" == "$expected" ]]; then
        log "Successfully configured 'python' to point to 'python3': $resolved"
    else
        error "Failed to configure 'python' correctly. It currently points to: $resolved"
    fi
}

# -----------------------------
# Main script execution
# -----------------------------
log "Starting python3-to-python configuration..."

check_python3_exists
check_existing_python_cmd
configure_update_alternatives
verify_python_alias

log "All done. You can now use 'python' as an alias for Python 3."
