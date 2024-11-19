# scripts/setup_test.py

import subprocess
import time
import sys

def run_command(command: str) -> int:
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True)
    return process.returncode

def main():
    print("Setting up test environment...")
    
    # Stop any existing containers
    run_command("docker compose -f docker-compose.test.yaml down -v")
    
    # Start test databases
    print("Starting test databases...")
    if run_command("docker compose -f docker-compose.test.yaml up -d") != 0:
        print("Failed to start test databases")
        return 1

    # Wait for databases to be ready
    print("Waiting for databases to be ready...")
    time.sleep(10)  # Give more time for both databases to start

    # Verify auth_db_test is ready
    if run_command("docker compose -f docker-compose.test.yaml exec auth_db_test pg_isready -U test_user -d auth_test_db") != 0:
        print("Auth test database is not ready")
        return 1

    # Verify user_db_test is ready
    if run_command("docker compose -f docker-compose.test.yaml exec user_db_test pg_isready -U test_user -d user_test_db") != 0:
        print("User test database is not ready")
        return 1

    print("Test environment is ready!")
    return 0

if __name__ == "__main__":
    sys.exit(main())