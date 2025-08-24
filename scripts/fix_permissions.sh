#!/bin/bash

# Fix permissions for the current directory and scripts
sudo chown -hR $USER:$USER .

# Make scripts executable
sudo chmod +x ./scripts/*.sh