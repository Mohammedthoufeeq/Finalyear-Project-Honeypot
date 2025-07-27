#!/bin/bash

# ---------------------------------------------------
# Script: enable_clipboard_virtualbox.sh
# Purpose: Ensure VirtualBox Guest Additions is installed
#          and clipboard sharing is functional in Ubuntu
# ---------------------------------------------------

set -e

log() {
    echo -e "\n[INFO] $1"
}

warn() {
    echo -e "\n[WARNING] $1"
}

error() {
    echo -e "\n[ERROR] $1" >&2
}

check_clipboard_setting_instruction() {
    warn "Clipboard sharing must be enabled in the VirtualBox GUI before starting the VM."
    echo "Steps:"
    echo "1. Power off the VM if it is running."
    echo "2. Open VirtualBox Manager on the host machine."
    echo "3. Select your VM → Settings → General → Advanced"
    echo "4. Set 'Shared Clipboard' and 'Drag and Drop' to 'Bidirectional'"
    read -p "Have you already completed the above steps? (y/n): " response
    if [[ "$response" != "y" ]]; then
        error "Please enable clipboard sharing in VM settings and rerun this script."
        exit 1
    fi
}

check_guest_additions_loaded() {
    if lsmod | grep -q vboxguest; then
        log "Guest Additions kernel module is already loaded."
        return 0
    fi
    return 1
}

install_required_packages() {
    log "Installing required system packages..."
    sudo apt update
    sudo apt install -y build-essential dkms linux-headers-$(uname -r)
}

verify_iso_mount_and_run() {
    log "Checking if Guest Additions ISO is mounted..."
    if ! mount | grep -q /mnt; then
        warn "Guest Additions ISO not mounted."
        echo "Please do the following before continuing:"
        echo "1. In the VirtualBox VM window, go to: Devices → Insert Guest Additions CD image..."
        echo "2. Wait a few seconds for the CD to mount or mount it manually using:"
        echo "     sudo mount /dev/cdrom /mnt"
        exit 1
    fi

    if [[ ! -f /mnt/VBoxLinuxAdditions.run ]]; then
        error "Guest Additions installer not found in /mnt. Please ensure the ISO is mounted correctly."
        exit 1
    fi

    log "Running Guest Additions installer..."
    sudo /mnt/VBoxLinuxAdditions.run || {
        error "Installer encountered an error. Check the log output above."
        exit 1
    }
}

verify_installation_success() {
    log "Verifying if Guest Additions module is now loaded..."
    sleep 2
    if lsmod | grep -q vboxguest; then
        log "Guest Additions module successfully loaded."
    else
        warn "Guest Additions installed but kernel module not loaded."
        echo "A reboot may be required to complete installation."
    fi
}

final_instructions() {
    echo
    echo "Guest Additions installation process is complete."
    echo "Please reboot your VM to apply changes:"
    echo "    sudo reboot"
    echo "After reboot, clipboard sharing between host and guest should be functional."
}

# Main execution

log "Starting VirtualBox Guest Additions setup for clipboard support..."

check_clipboard_setting_instruction

if check_guest_additions_loaded; then
    log "Guest Additions already installed and active. No further action needed."
    exit 0
fi

install_required_packages
verify_iso_mount_and_run
verify_installation_success
final_instructions
