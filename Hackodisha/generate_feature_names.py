# generate_feature_names.py
import joblib
import os

def create_feature_names():
    """Generate and save feature_names.pkl"""
    print("📝 Creating feature_names.pkl...")
    
    # Create directories
    os.makedirs('ml_models/saved_models', exist_ok=True)
    
    # Define comprehensive feature names
    feature_names = [
        # Basic demographic features
        'age',
        'monthly_income', 
        'monthly_expenses',
        'surplus',
        'dependents',
        'income_stability',
        
        # Calculated ratio features
        'surplus_to_income_ratio',
        'expense_ratio',
        'risk_capacity',
        
        # Interaction features
        'age_income_interaction',
        'stability_surplus_interaction'
    ]
    
    print(f"📋 Feature names ({len(feature_names)} total):")
    for i, name in enumerate(feature_names, 1):
        print(f"   {i:2d}. {name}")
    
    # Save feature names
    joblib.dump(feature_names, 'ml_models/saved_models/feature_names.pkl')
    print("✅ feature_names.pkl saved!")
    
    # Test loading
    loaded_features = joblib.load('ml_models/saved_models/feature_names.pkl')
    print(f"✅ Verified: {len(loaded_features)} feature names loaded")
    
    # Show feature categories
    print("\n📊 Feature Categories:")
    basic_features = [f for f in feature_names if not ('_' in f and ('ratio' in f or 'interaction' in f))]
    ratio_features = [f for f in feature_names if 'ratio' in f]
    interaction_features = [f for f in feature_names if 'interaction' in f]
    
    print(f"   Basic Features ({len(basic_features)}): {', '.join(basic_features)}")
    print(f"   Ratio Features ({len(ratio_features)}): {', '.join(ratio_features)}")
    print(f"   Interaction Features ({len(interaction_features)}): {', '.join(interaction_features)}")
    
    return feature_names

if __name__ == "__main__":
    features = create_feature_names()
    print("🎉 feature_names.pkl generated successfully!")