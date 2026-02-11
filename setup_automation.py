"""
Windows Task Scheduler Setup Script for AMFI TER Daily Automation
Run this script with Administrator privileges to set up daily automation
"""

import subprocess
from pathlib import Path
import sys

def setup_task_scheduler():
    """Create Windows Task Scheduler task using schtasks command"""
    
    # Get paths
    script_dir = Path(__file__).parent.absolute()
    python_exe = Path(sys.executable)
    script_path = script_dir / 'ter_daily_automation.py'
    
    print("=" * 100)
    print("AMFI TER - Daily Automation Setup")
    print("=" * 100)
    print()
    print(f"Script Directory: {script_dir}")
    print(f"Python Executable: {python_exe}")
    print(f"Script Path: {script_path}")
    print()
    
    # Verify files exist
    if not python_exe.exists():
        print(f"❌ Error: Python executable not found at {python_exe}")
        return False
    
    if not script_path.exists():
        print(f"❌ Error: Script not found at {script_path}")
        return False
    
    # Create task using schtasks
    task_name = "AMFI-TER-Daily-Analysis"
    
    print(f"Creating scheduled task: {task_name}")
    print(f"  Trigger: Daily at 09:00 AM")
    print(f"  Script: {script_path}")
    print()
    
    try:
        # Delete existing task if it exists
        print("Checking for existing task...")
        subprocess.run(
            ['schtasks', '/delete', '/tn', task_name, '/f'],
            capture_output=True,
            timeout=10
        )
        
        # Create new task
        cmd = [
            'schtasks',
            '/create',
            '/tn', task_name,
            '/tr', f'"{python_exe}" "{script_path}"',
            '/sc', 'daily',
            '/st', '09:00:00',
            '/f'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print()
            print("=" * 100)
            print("✓ SETUP SUCCESSFUL")
            print("=" * 100)
            print()
            print("Task Configuration:")
            print(f"  Name: {task_name}")
            print(f"  Schedule: Daily at 09:00 AM")
            print(f"  Python: {python_exe}")
            print(f"  Script: {script_path}")
            print()
            print("What Happens:")
            print("  • Task runs daily at 9:00 AM")
            print("  • Downloads current month AMFI TER file")
            print("  • Compares with previous day data")
            print("  • When month changes, new file auto-downloads")
            print("  • Daily reports saved to output/ folder")
            print()
            print("Useful Commands:")
            print(f"  • Query task: schtasks /query /tn \"{task_name}\" /v")
            print(f"  • Run now: schtasks /run /tn \"{task_name}\"")
            print(f"  • Disable: schtasks /change /tn \"{task_name}\" /disable")
            print(f"  • Enable: schtasks /change /tn \"{task_name}\" /enable")
            print(f"  • Delete: schtasks /delete /tn \"{task_name}\" /f")
            print()
            print("=" * 100)
            
            # Verify task was created
            print("\nVerifying task creation...")
            verify = subprocess.run(
                ['schtasks', '/query', '/tn', task_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if verify.returncode == 0:
                print("✓ Task verified successfully!")
                print(verify.stdout)
            
            return True
        else:
            print(f"❌ Failed to create task (return code: {result.returncode})")
            return False
    
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_task_scheduler()
    print()
    if success:
        print("✓ Setup complete! Task scheduler is ready.")
    else:
        print("✗ Setup failed. Please check the errors above.")
    print()
    input("Press Enter to exit...")
