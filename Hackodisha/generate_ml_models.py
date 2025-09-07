# generate_ml_models.py
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
import os

def create_ml_models():
    """Generate and save ml_models.pkl"""
    print("🤖 Creating ml_models.pkl...")
    
    # Create directories
    os.makedirs('ml_models/saved_models', exist_ok=True)
    
    # Generate sample training data
    print("📊 Generating training data...")
    n_samples = 5000
    data = []
    
    for i in range(n_samples):
        age = np.random.randint(25, 60)
        income = np.random.randint(30000, 150000)
        expenses = int(income * np.random.uniform(0.6, 0.85))
        surplus = income - expenses
        dependents = np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1])
        stability = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.4, 0.2, 0.1])
        
        # Calculate features
        surplus_ratio = surplus / income if income > 0 else 0
        risk_capacity = min(10, max(1, 5 + (stability - 3) + (60 - age) // 10 - dependents))
        
        # Generate realistic allocations based on risk
        if risk_capacity <= 3:  # Conservative
            emergency = 0.35
            equity = 0.25
            debt = 0.3
            gold = 0.1
        elif risk_capacity <= 7:  # Moderate
            emergency = 0.3
            equity = 0.45
            debt = 0.2
            gold = 0.05
        else:  # Aggressive
            emergency = 0.25
            equity = 0.6
            debt = 0.1
            gold = 0.05
        
        # Add some randomness
        emergency += np.random.uniform(-0.05, 0.05)
        equity += np.random.uniform(-0.1, 0.1)
        debt += np.random.uniform(-0.05, 0.05)
        gold += np.random.uniform(-0.02, 0.02)
        
        # Normalize
        total = emergency + equity + debt + gold
        emergency, equity, debt, gold = [x/total for x in [emergency, equity, debt, gold]]
        
        # Expected return
        expected_return = emergency * 4 + equity * 12 + debt * 7 + gold * 8
        
        data.append({
            'age': age,
            'monthly_income': income,
            'monthly_expenses': expenses,
            'surplus': surplus,
            'dependents': dependents,
            'income_stability': stability,
            'surplus_to_income_ratio': surplus_ratio,
            'expense_ratio': expenses / income,
            'risk_capacity': risk_capacity,
            'age_income_interaction': age * income / 100000,
            'stability_surplus_interaction': stability * surplus / 1000,
            'emergency_fund_allocation': emergency,
            'equity_allocation': equity,
            'debt_allocation': debt,
            'gold_allocation': gold,
            'expected_return': expected_return
        })
    
    df = pd.DataFrame(data)
    
    # Prepare features and targets
    feature_cols = [
        'age', 'monthly_income', 'monthly_expenses', 'surplus', 'dependents',
        'income_stability', 'surplus_to_income_ratio', 'expense_ratio', 
        'risk_capacity', 'age_income_interaction', 'stability_surplus_interaction'
    ]
    
    target_cols = [
        'emergency_fund_allocation', 'equity_allocation', 'debt_allocation', 
        'gold_allocation', 'expected_return'
    ]
    
    X = df[feature_cols]
    y = df[target_cols]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("🎯 Training ML models...")
    models = {}
    
    # Train portfolio allocation models
    portfolio_models = {}
    allocation_targets = ['emergency_fund_allocation', 'equity_allocation', 'debt_allocation', 'gold_allocation']
    
    for target in allocation_targets:
        print(f"   Training {target} model...")
        
        # Try different models
        rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        gb_model = GradientBoostingRegressor(n_estimators=100, max_depth=6, random_state=42)
        
        # Cross-validation scores
        rf_score = cross_val_score(rf_model, X_train_scaled, y_train[target], cv=5, scoring='r2').mean()
        gb_score = cross_val_score(gb_model, X_train_scaled, y_train[target], cv=5, scoring='r2').mean()
        
        # Choose best model
        if rf_score > gb_score:
            best_model = rf_model
            best_name = 'RandomForest'
            best_score = rf_score
        else:
            best_model = gb_model
            best_name = 'GradientBoosting'
            best_score = gb_score
        
        # Train best model
        best_model.fit(X_train_scaled, y_train[target])
        
        # Test performance
        y_pred = best_model.predict(X_test_scaled)
        test_r2 = r2_score(y_test[target], y_pred)
        test_mae = mean_absolute_error(y_test[target], y_pred)
        
        portfolio_models[target] = {
            'model': best_model,
            'algorithm': best_name,
            'cv_score': best_score,
            'test_r2': test_r2,
            'test_mae': test_mae
        }
        
        print(f"     ✅ {best_name} - CV: {best_score:.4f}, Test R²: {test_r2:.4f}")
    
    models['portfolio_allocator'] = portfolio_models
    
    # Train return predictor
    print("   Training return predictor...")
    rf_return = RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42)
    gb_return = GradientBoostingRegressor(n_estimators=150, max_depth=8, random_state=42)
    
    rf_return_score = cross_val_score(rf_return, X_train_scaled, y_train['expected_return'], cv=5, scoring='r2').mean()
    gb_return_score = cross_val_score(gb_return, X_train_scaled, y_train['expected_return'], cv=5, scoring='r2').mean()
    
    if rf_return_score > gb_return_score:
        best_return_model = rf_return
        best_return_name = 'RandomForest'
        best_return_score = rf_return_score
    else:
        best_return_model = gb_return
        best_return_name = 'GradientBoosting'
        best_return_score = gb_return_score
    
    best_return_model.fit(X_train_scaled, y_train['expected_return'])
    
    # Test return predictor
    y_return_pred = best_return_model.predict(X_test_scaled)
    return_test_r2 = r2_score(y_test['expected_return'], y_return_pred)
    return_test_mae = mean_absolute_error(y_test['expected_return'], y_return_pred)
    
    models['return_predictor'] = {
        'model': best_return_model,
        'algorithm': best_return_name,
        'cv_score': best_return_score,
        'test_r2': return_test_r2,
        'test_mae': return_test_mae
    }
    
    print(f"     ✅ {best_return_name} - CV: {best_return_score:.4f}, Test R²: {return_test_r2:.4f}")
    
    # Save models
    joblib.dump(models, 'ml_models/saved_models/ml_models.pkl')
    print("✅ ml_models.pkl saved!")
    
    # Test loading
    loaded_models = joblib.load('ml_models/saved_models/ml_models.pkl')
    print(f"✅ Verified: Contains {len(loaded_models)} model groups")
    
    return models

if __name__ == "__main__":
    models = create_ml_models()
    print("🎉 ml_models.pkl generated successfully!")