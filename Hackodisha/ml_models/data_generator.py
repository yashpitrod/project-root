#!/usr/bin/env python3
"""
Investment Data Generator
Generates realistic training data for ML investment advisor
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import json
import warnings
warnings.filterwarnings('ignore')

class InvestmentDataGenerator:
    """Generate realistic investment data for training ML models"""
    
    def __init__(self):
        self.market_data = {}
        self.economic_indicators = {}
        
    def generate_realistic_users(self, n_samples=15000):
        """Generate realistic user profiles with investment outcomes"""
        print(f"🏗️ Generating {n_samples} realistic user profiles...")
        
        # Create output directory
        os.makedirs('data/training_data', exist_ok=True)
        
        data = []
        
        for i in range(n_samples):
            # Generate user demographics with realistic distributions
            profile = self._generate_user_profile()
            
            # Calculate derived features
            derived_features = self._calculate_derived_features(profile)
            
            # Generate investment outcomes based on profile
            investment_outcomes = self._generate_investment_outcomes(profile, derived_features)
            
            # Combine all data
            complete_profile = {**profile, **derived_features, **investment_outcomes}
            data.append(complete_profile)
            
            # Progress indicator
            if (i + 1) % 1000 == 0:
                print(f"   Generated {i + 1} profiles...")
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Add data quality checks
        df = self._apply_data_quality_checks(df)
        
        # Save to CSV
        output_file = 'data/training_data/user_profiles.csv'
        df.to_csv(output_file, index=False)
        
        print(f"✅ Training data saved: {output_file}")
        print(f"📊 Dataset shape: {df.shape}")
        print(f"📈 Features: {len(df.columns)} columns")
        
        # Display sample statistics
        self._display_dataset_statistics(df)
        
        return df
    
    def _generate_user_profile(self):
        """Generate realistic user demographic profile"""
        # Age distribution (working population)
        age = int(np.random.beta(2, 3) * 40 + 22)  # Ages 22-62, skewed younger
        
        # Income based on age and career progression
        base_income = self._calculate_realistic_income(age)
        monthly_income = int(base_income + np.random.normal(0, base_income * 0.2))
        monthly_income = max(15000, monthly_income)  # Minimum wage floor
        
        # Expenses based on income and lifestyle
        expense_ratio = self._calculate_expense_ratio(monthly_income, age)
        monthly_expenses = int(monthly_income * expense_ratio)
        
        # Family situation
        dependents = self._generate_dependents(age)
        
        # Employment stability
        income_stability = self._generate_income_stability(age, monthly_income)
        
        # Education and location (affecting financial literacy)
        education_score = np.random.choice([1, 2, 3], p=[0.25, 0.50, 0.25])  # School, Graduate, PostGrad
        location_score = np.random.choice([1, 2, 3], p=[0.30, 0.40, 0.30])   # Tier3, Tier2, Metro
        
        return {
            'age': age,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'dependents': dependents,
            'income_stability': income_stability,
            'education_score': education_score,
            'location_score': location_score
        }
    
    def _calculate_realistic_income(self, age):
        """Calculate realistic income based on age and career stage"""
        if age < 25:
            return np.random.uniform(20000, 45000)
        elif age < 30:
            return np.random.uniform(35000, 80000)
        elif age < 35:
            return np.random.uniform(50000, 120000)
        elif age < 40:
            return np.random.uniform(60000, 150000)
        elif age < 50:
            return np.random.uniform(70000, 200000)
        else:
            return np.random.uniform(60000, 180000)  # Post-peak earnings
    
    def _calculate_expense_ratio(self, income, age):
        """Calculate realistic expense ratio based on income and age"""
        # Lower income = higher expense ratio (less disposable income)
        if income < 30000:
            base_ratio = np.random.uniform(0.85, 0.95)
        elif income < 50000:
            base_ratio = np.random.uniform(0.75, 0.88)
        elif income < 100000:
            base_ratio = np.random.uniform(0.65, 0.80)
        else:
            base_ratio = np.random.uniform(0.55, 0.75)
        
        # Age adjustments (young adults and families spend more)
        if age < 28:
            base_ratio += np.random.uniform(0.02, 0.08)  # Young adult lifestyle
        elif age > 50:
            base_ratio -= np.random.uniform(0.02, 0.05)  # Empty nesters
        
        return min(0.95, max(0.50, base_ratio))
    
    def _generate_dependents(self, age):
        """Generate realistic number of dependents based on age"""
        if age < 25:
            return np.random.choice([0, 1], p=[0.8, 0.2])
        elif age < 35:
            return np.random.choice([0, 1, 2], p=[0.4, 0.4, 0.2])
        elif age < 45:
            return np.random.choice([0, 1, 2, 3], p=[0.2, 0.3, 0.4, 0.1])
        else:
            return np.random.choice([0, 1, 2], p=[0.5, 0.3, 0.2])  # Kids grown up
    
    def _generate_income_stability(self, age, income):
        """Generate income stability score based on age and income"""
        # Higher income and older age generally mean more stability
        base_stability = 3  # Neutral
        
        # Age factor
        if age > 35:
            base_stability += 0.5
        if age > 45:
            base_stability += 0.5
        
        # Income factor
        if income > 75000:
            base_stability += 0.5
        if income > 150000:
            base_stability += 0.5
        
        # Add randomness
        stability = base_stability + np.random.uniform(-1, 1)
        
        # Convert to discrete scale
        return max(1, min(5, int(round(stability))))
    
    def _calculate_derived_features(self, profile):
        """Calculate derived features from basic profile"""
        surplus = profile['monthly_income'] - profile['monthly_expenses']
        
        derived = {
            'surplus': surplus,
            'surplus_to_income_ratio': surplus / profile['monthly_income'] if profile['monthly_income'] > 0 else 0,
            'expense_ratio': profile['monthly_expenses'] / profile['monthly_income'] if profile['monthly_income'] > 0 else 1,
            'income_per_dependent': profile['monthly_income'] / (profile['dependents'] + 1),
            'age_income_interaction': profile['age'] * profile['monthly_income'] / 100000,
            'stability_surplus_interaction': profile['income_stability'] * surplus / 1000,
        }
        
        # Risk capacity calculation
        derived['risk_capacity'] = self._calculate_risk_capacity(profile, derived)
        
        return derived
    
    def _calculate_risk_capacity(self, profile, derived):
        """Calculate comprehensive risk capacity score"""
        risk_score = 5  # Start neutral
        
        # Age factor (younger = higher risk tolerance)
        if profile['age'] < 30:
            risk_score += 2
        elif profile['age'] < 40:
            risk_score += 1
        elif profile['age'] > 50:
            risk_score -= 1
        elif profile['age'] > 55:
            risk_score -= 2
        
        # Income stability factor
        risk_score += (profile['income_stability'] - 3)
        
        # Dependents factor (more dependents = lower risk)
        risk_score -= profile['dependents'] * 0.7
        
        # Surplus factor
        if derived['surplus'] > 50000:
            risk_score += 2
        elif derived['surplus'] > 25000:
            risk_score += 1
        elif derived['surplus'] < 10000:
            risk_score -= 1.5
        
        # Education factor (higher education = slightly higher risk tolerance)
        risk_score += (profile['education_score'] - 2) * 0.5
        
        # Location factor (metro = slightly higher risk tolerance)
        risk_score += (profile['location_score'] - 2) * 0.3
        
        # Ensure realistic bounds
        return max(1.0, min(10.0, risk_score))
    
    def _generate_investment_outcomes(self, profile, derived):
        """Generate realistic investment allocations and outcomes"""
        risk_capacity = derived['risk_capacity']
        surplus = derived['surplus']
        
        # Emergency fund allocation (always needed)
        emergency_base = 0.35 if profile['income_stability'] <= 2 else 0.25
        emergency_fund = max(0.15, min(0.50, emergency_base + np.random.uniform(-0.08, 0.08)))
        
        # Remaining allocation for investments
        remaining = 1 - emergency_fund
        
        # Allocation strategy based on risk capacity
        if risk_capacity <= 3:  # Conservative
            equity_base, debt_base, gold_base = 0.25, 0.60, 0.15
        elif risk_capacity <= 6:  # Moderate
            equity_base, debt_base, gold_base = 0.50, 0.35, 0.15
        elif risk_capacity <= 8:  # Moderate-Aggressive
            equity_base, debt_base, gold_base = 0.65, 0.25, 0.10
        else:  # Aggressive
            equity_base, debt_base, gold_base = 0.75, 0.20, 0.05
        
        # Add realistic randomness
        equity = max(0.1, min(0.8, equity_base + np.random.uniform(-0.15, 0.15)))
        debt = max(0.1, min(0.6, debt_base + np.random.uniform(-0.12, 0.12)))
        gold = max(0.02, min(0.25, gold_base + np.random.uniform(-0.08, 0.08)))
        
        # Normalize to remaining allocation
        total = equity + debt + gold
        if total > 0:
            equity = (equity / total) * remaining
            debt = (debt / total) * remaining
            gold = (gold / total) * remaining
        
        # Calculate expected return
        expected_return = (
            emergency_fund * 4.0 +
            equity * np.random.uniform(10.0, 14.0) +
            debt * np.random.uniform(6.0, 8.0) +
            gold * np.random.uniform(6.0, 10.0)
        )
        
        # User satisfaction (simulated based on returns and risk alignment)
        satisfaction = self._calculate_satisfaction(risk_capacity, expected_return, profile)
        
        return {
            'emergency_fund_allocation': emergency_fund,
            'equity_allocation': equity,
            'debt_allocation': debt,
            'gold_allocation': gold,
            'expected_return': expected_return,
            'user_satisfaction': satisfaction,
            'portfolio_volatility': self._calculate_portfolio_volatility(equity, debt, gold),
            'time_horizon': self._estimate_investment_horizon(profile['age'])
        }
    
    def _calculate_satisfaction(self, risk_capacity, expected_return, profile):
        """Calculate user satisfaction with investment strategy"""
        # Base satisfaction
        satisfaction = 0.7
        
        # Return satisfaction (higher returns = higher satisfaction, but diminishing)
        return_satisfaction = min(1.0, expected_return / 15.0)
        satisfaction += return_satisfaction * 0.2
        
        # Risk alignment (satisfaction higher when risk matches capacity)
        if 8 <= expected_return <= 10 and risk_capacity <= 4:  # Conservative match
            satisfaction += 0.1
        elif 10 <= expected_return <= 13 and 4 <= risk_capacity <= 7:  # Moderate match
            satisfaction += 0.1
        elif expected_return >= 12 and risk_capacity >= 7:  # Aggressive match
            satisfaction += 0.1
        
        # Add some randomness
        satisfaction += np.random.uniform(-0.1, 0.1)
        
        return max(0.3, min(1.0, satisfaction))
    
    def _calculate_portfolio_volatility(self, equity, debt, gold):
        """Calculate portfolio volatility based on allocation"""
        # Volatility assumptions (standard deviations)
        equity_vol = 0.18  # 18% volatility for equity
        debt_vol = 0.05    # 5% volatility for debt
        gold_vol = 0.15    # 15% volatility for gold
        
        # Simplified portfolio volatility (assuming some correlation)
        portfolio_vol = (equity * equity_vol + debt * debt_vol + gold * gold_vol) * 0.9
        return portfolio_vol
    
    def _estimate_investment_horizon(self, age):
        """Estimate investment time horizon based on age"""
        if age < 30:
            return np.random.choice(['long', 'very_long'], p=[0.3, 0.7])
        elif age < 45:
            return np.random.choice(['medium', 'long'], p=[0.4, 0.6])
        elif age < 55:
            return np.random.choice(['short', 'medium'], p=[0.6, 0.4])
        else:
            return np.random.choice(['short', 'medium'], p=[0.8, 0.2])
    
    def _apply_data_quality_checks(self, df):
        """Apply data quality checks and corrections"""
        print("🔍 Applying data quality checks...")
        
        # Remove impossible combinations
        df = df[df['monthly_expenses'] >= 0]
        df = df[df['surplus'] >= -50000]  # Allow some negative surplus (debt situations)
        df = df[df['expected_return'] > 0]
        
        # Fix allocation constraints
        allocation_cols = ['emergency_fund_allocation', 'equity_allocation', 'debt_allocation', 'gold_allocation']
        for col in allocation_cols:
            df[col] = df[col].clip(0, 1)
        
        # Ensure allocations sum to approximately 1
        df['allocation_sum'] = df[allocation_cols].sum(axis=1)
        mask = df['allocation_sum'] > 0.1  # Valid allocations
        df = df[mask].copy()
        
        # Renormalize allocations
        for col in allocation_cols:
            df[col] = df[col] / df['allocation_sum']
        
        df = df.drop('allocation_sum', axis=1)
        
        print(f"✅ Data quality checks complete. Remaining samples: {len(df)}")
        return df
    
    def _display_dataset_statistics(self, df):
        """Display comprehensive dataset statistics"""
        print("\n📊 Dataset Statistics:")
        print("=" * 50)
        
        # Basic statistics
        print(f"Total samples: {len(df):,}")
        print(f"Features: {len(df.columns)}")
        
        # Income distribution
        print(f"\n💰 Income Distribution:")
        print(f"  Mean: ₹{df['monthly_income'].mean():,.0f}")
        print(f"  Median: ₹{df['monthly_income'].median():,.0f}")
        print(f"  Range: ₹{df['monthly_income'].min():,.0f} - ₹{df['monthly_income'].max():,.0f}")
        
        # Age distribution
        print(f"\n👥 Age Distribution:")
        print(f"  Mean: {df['age'].mean():.1f} years")
        print(f"  Range: {df['age'].min()} - {df['age'].max()} years")
        
        # Risk capacity
        print(f"\n🎯 Risk Capacity Distribution:")
        risk_dist = df['risk_capacity'].value_counts().sort_index()
        for risk, count in risk_dist.head().items():
            percentage = (count / len(df)) * 100
            print(f"  {risk:.1f}: {count:,} ({percentage:.1f}%)")
        
        # Expected returns
        print(f"\n📈 Expected Returns:")
        print(f"  Mean: {df['expected_return'].mean():.2f}%")
        print(f"  Range: {df['expected_return'].min():.2f}% - {df['expected_return'].max():.2f}%")
        
        # Portfolio allocations
        print(f"\n🏦 Average Portfolio Allocation:")
        allocation_cols = ['emergency_fund_allocation', 'equity_allocation', 'debt_allocation', 'gold_allocation']
        for col in allocation_cols:
            mean_allocation = df[col].mean()
            print(f"  {col.replace('_allocation', '').title()}: {mean_allocation:.1%}")
    
    def generate_market_scenarios(self, n_scenarios=1000):
        """Generate market scenarios for robust training"""
        print(f"📈 Generating {n_scenarios} market scenarios...")
        
        scenarios = []
        for i in range(n_scenarios):
            scenario = {
                'scenario_id': i,
                'date': datetime.now() - timedelta(days=random.randint(0, 365*5)),
                'inflation_rate': np.random.uniform(3.0, 9.0),
                'repo_rate': np.random.uniform(4.0, 8.0),
                'equity_market_return': np.random.normal(12.0, 8.0),
                'debt_market_return': np.random.uniform(5.0, 9.0),
                'gold_return': np.random.normal(8.0, 6.0),
                'market_volatility': np.random.uniform(0.12, 0.35),
                'economic_growth': np.random.uniform(-1.0, 8.0),
                'market_sentiment': np.random.choice(['bearish', 'neutral', 'bullish'], p=[0.2, 0.6, 0.2])
            }
            scenarios.append(scenario)
        
        # Save market scenarios
        scenarios_df = pd.DataFrame(scenarios)
        scenarios_df.to_csv('data/training_data/market_scenarios.csv', index=False)
        
        print(f"✅ Market scenarios saved: data/training_data/market_scenarios.csv")
        return scenarios_df

def main():
    """Main function to generate all training data"""
    print("🚀 Investment Data Generator")
    print("=" * 50)
    
    # Initialize generator
    generator = InvestmentDataGenerator()
    
    # Generate user profiles
    user_data = generator.generate_realistic_users(15000)
    
    # Generate market scenarios
    market_data = generator.generate_market_scenarios(1000)
    
    print("\n🎉 Data Generation Complete!")
    print(f"📊 User profiles: {len(user_data):,}")
    print(f"📈 Market scenarios: {len(market_data):,}")
    print("\n📁 Files created:")
    print("  • data/training_data/user_profiles.csv")
    print("  • data/training_data/market_scenarios.csv")

if __name__ == "__main__":
    main()