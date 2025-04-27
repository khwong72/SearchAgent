import os
import sys
import subprocess

def main():
    """Run the complete test workflow in one step"""
    print("Starting test workflow...")
    
    # Create directories
    os.makedirs("semrush_reports", exist_ok=True)
    os.makedirs("email_previews", exist_ok=True)
    
    # Step 1: Create test image
    print("\n=== Creating test image ===")
    test_image_script = "create_test_image.py"
    test_image_path = os.path.join("semrush_reports", "test_image.png")
    
    try:
        print(f"Running: python3 {test_image_script}")
        subprocess.run(["python3", test_image_script], check=True)
        
        if not os.path.exists(test_image_path):
            print(f"Error: Test image was not created at {test_image_path}")
            return 1
            
        print(f"Test image created successfully at {test_image_path}")
    except Exception as e:
        print(f"Error creating test image: {e}")
        return 1
    
    # Step 2: Run email workflow test
    print("\n=== Running email workflow test ===")
    workflow_script = "simple_workflow_test.py"
    csv_file = "test_contact.csv"
    
    try:
        print(f"Running: python3 {workflow_script} {csv_file} {test_image_path}")
        subprocess.run(["python3", workflow_script, csv_file, test_image_path], check=True)
    except Exception as e:
        print(f"Error running workflow test: {e}")
        return 1
        
    print("\n=== Test workflow completed ===")
    print("Check email_previews folder for the generated email HTML")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 