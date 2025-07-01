#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    # Get port from environment with fallback
    port = os.environ.get('PORT', '8080')
    
    # Validate port
    try:
        port_int = int(port)
        if port_int <= 0 or port_int > 65535:
            raise ValueError("Invalid port range")
    except ValueError:
        print(f"Invalid PORT value: {port}, using default 8080")
        port = '8080'
    
    print(f"Starting server on port {port}")
    
    # Start uvicorn with validated port
    cmd = [
        'uvicorn', 
        'main:app', 
        '--host', '0.0.0.0', 
        '--port', port,
        '--workers', '1'
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()