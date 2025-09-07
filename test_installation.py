#!/usr/bin/env python3
"""
Test script to verify all dependencies are installed correctly
"""

def test_imports():
    try:
        import flask
        print(f"✅ Flask {flask.__version__} - OK")
    except ImportError as e:
        print(f"❌ Flask - FAILED: {e}")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy {numpy.__version__} - OK")
    except ImportError as e:
        print(f"❌ NumPy - FAILED: {e}")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__} - OK")
    except ImportError as e:
        print(f"❌ Pandas - FAILED: {e}")
        return False
    
    try:
        import sklearn
        print(f"✅ Scikit-learn {sklearn.__version__} - OK")
    except ImportError as e:
        print(f"❌ Scikit-learn - FAILED: {e}")
        return False
    
    try:
        import joblib
        print(f"✅ Joblib {joblib.__version__} - OK")
    except ImportError as e:
        print(f"❌ Joblib - FAILED: {e}")
        return False
    
    try:
        import werkzeug
        print(f"✅ Werkzeug {werkzeug.__version__} - OK")
    except ImportError as e:
        print(f"❌ Werkzeug - FAILED: {e}")
        return False
    
    try:
        import jinja2
        print(f"✅ Jinja2 {jinja2.__version__} - OK")
    except ImportError as e:
        print(f"❌ Jinja2 - FAILED: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("    Testing Python Dependencies")
    print("=" * 50)
    print()
    
    if test_imports():
        print()
        print("🎉 All dependencies are installed successfully!")
        print("You can now run your Flask application!")
    else:
        print()
        print("❌ Some dependencies are missing. Please install them first.")



