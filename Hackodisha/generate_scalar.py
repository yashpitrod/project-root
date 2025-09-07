# generate_scaler.py
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import os

def create_scaler():
    """Generate and save scaler.pkl"""
    print("⚖️ Creating scaler.pkl...")
    
    # Create directories
    os.makedirs('ml_models/saved_models', exist_ok=True)
    
    # Generate sample data to fit the scaler
    print("📊 Generating sample data for scaler fitting...")
    
    n_samples = 1000
    np.random.seed(42)  # For reproducible results
    
    # Generate realistic feature ranges
    data = {
        'age': np.random.randint(22, 65, n_samples),
        'monthly_income': np.random.randint(20000, 200000, n_samples),
        'monthly_expenses': np.random.randint(15000, 150000, n_samples),
        'surplus': np.random.randint(0, 80000, n_samples),
        'dependents': np.random.randint(0, 5, n_samples),
        'income_stability': np.random.randint(1, 6, n_samples),
        'surplus_to_income_ratio': np.random.uniform(0, 0.6, n_samples),
        'expense_ratio': np.random.uniform(0.4, 0.9, n_samples),
        'risk_capacity': np.random.uniform(1, 10, n_samples),
        'age_income_interaction': np.random.uniform(0.5, 15, n_samples),
        'stability_surplus_interaction': np.random.uniform(0, 300, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Feature columns that will be scaled
    feature_names = [
        'age', 'monthly_income', 'monthly_expenses', 'surplus', 'dependents',
        'income_stability', 'surplus_to_income_ratio', 'expense_ratio', 
        'risk_capacity', 'age_income_interaction', 'stability_surplus_interaction'
    ]
    
    print(f"🔧 Fitting scaler on {len(feature_names)} features...")
    
    # Create and fit scaler
    scaler = StandardScaler()
    scaler.fit(df[feature_names])
    
    # Display scaler statistics
    print("📊 Scaler Statistics:")
    for i, feature in enumerate(feature_names):
        mean_val = scaler.mean_[i]
        scale_val = scaler.scale_[i]
        print(f"   {feature}: mean={mean_val:.2f}, std={scale_val:.2f}")
    
    # Save scaler
    joblib.dump(scaler, 'ml_models/saved_models/scaler.pkl')
    print("✅ scaler.pkl saved!")
    
    # Test loading and using scaler
    loaded_scaler = joblib.load('ml_models/saved_models/scaler.pkl')
    
    # Test with sample data
    test_data = np.array([[30, 50000, 35000, 15000, 2, 3, 0.3, 0.7, 5.5, 1.5, 45]])
    scaled_data = loaded_scaler.transform(test_data)
    
    print("🧪 Test transformation:")
    print(f"   Original: {test_data[0][:5]}")  # Show first 5 features
    print(f"   Scaled:   {scaled_data[0][:5]}")
    print("✅ Scaler working correctly!")
    
    return scaler

if __name__ == "__main__":
    scaler = create_scaler()
    print("🎉 scaler.pkl generated successfully!")