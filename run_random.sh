#!/bin/bash

# List of directories
dirs=("gotham" "naboo" "winterfell")

# Array to store process IDs
pids=()

# Function to kill all child processes on exit
cleanup() {
    echo "Stopping all processes..."
    for pid in "${pids[@]}"; do
        kill "$pid" 2>/dev/null
    done
    wait  # Wait for all child processes to exit
    echo "All processes stopped."
}

# Trap SIGINT (Ctrl+C) and SIGTERM to run cleanup function
trap cleanup SIGINT SIGTERM

# Loop through each directory and run the script
for dir in "${dirs[@]}"; do
    echo "Running algo.py in $dir..."
    (cd "$dir" && python3 algo.py) &  # Run in a subshell
    pids+=($!)  # Store the PID of the last background process
done

echo "All scripts executed!"

# Wait for all background processes
wait