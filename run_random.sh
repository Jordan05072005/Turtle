#!/bin/bash

# List of directories
dirs=("gotham" "naboo" "winterfell")

# Loop through each directory and run the script
for dir in "${dirs[@]}"; do
    echo "Running algo.py in $dir..."
    (cd "$dir" && python3 algo.py) &  # Run in a subshell to avoid changing the main directory
done

echo "All scripts executed!"
