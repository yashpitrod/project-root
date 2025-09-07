# generate_all_pickles.py
import subprocess
import sys

def run_all_generators():
    """Run all pickle generators"""
    scripts = [
        'generate_ml_models.py',
        'generate_scaler.py', 
        'generate_feature_names.py',
        'generate_metadata.py'
    ]
    
    print("🚀 Generating all pickle files...")
    
    for script in scripts:
        print(f"\n{'='*50}")
        print(f"Running {script}...")
        try:
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {script} completed successfully")
            else:
                print(f"❌ {script} failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Error running {script}: {e}")
    
    print(f"\n{'='*50}")
    print("🎉 All pickle files generated!")
    
    # Verify all files exist
    import os
    files = ['ml_models.pkl', 'scaler.pkl', 'feature_names.pkl', 'metadata.pkl']
    print("\n📁 Generated files:")
    for file in files:
        path = f'ml_models/saved_models/{file}'
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024  # KB
            print(f"   ✅ {file} ({size:.1f} KB)")
        else:
            print(f"   ❌ {file} - NOT FOUND")

if __name__ == "__main__":
    run_all_generators()