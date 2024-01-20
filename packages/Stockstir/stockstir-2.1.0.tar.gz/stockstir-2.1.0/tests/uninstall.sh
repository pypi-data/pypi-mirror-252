#!/bin/bash

# Simple script that uninstalls StockstirClassTesting and then reinstalls it for testing purposes.

# Uninstall the package
pip3 uninstall -y stockstir

# Reinstall the package
pip3 install -e .