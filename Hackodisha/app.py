import sys
import os
import traceback

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
import numpy as np
import pandas as pd
from datetime import datetime
import joblib

# Import configuration
try:
    from config import Config
    print("✅ Config imported successfully")
except ImportError as e:
    print(f"❌ Error importing config: {e}")
    sys.exit(1)

# ML Predictor Class
class MLInvestmentPredictor:
    """ML-powered investment predictor using saved pickle files"""
    
    def __init__(self):
        self.models = None
        self.scaler = None
        self.feature_names = None
        self.metadata = None
        self.ml_available = False
        self.load_models()
    
    def load_models(self):
        """Load all ML models from pickle files"""
        try:
            # Resolve model path relative to this file to avoid CWD issues
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, 'ml_models', 'saved_models')
            
            # Check if pickle files exist
            required_files = ['ml_models.pkl', 'scaler.pkl', 'feature_names.pkl', 'metadata.pkl']
            missing_files = []
            
            for file in required_files:
                if not os.path.exists(os.path.join(model_path, file)):
                    missing_files.append(file)
            
            if missing_files:
                print(f"⚠️ Missing ML files: {missing_files}")
                print("   Run pickle generation scripts first!")
                return False
            
            # Load all pickle files
            self.models = joblib.load(os.path.join(model_path, 'ml_models.pkl'))
            self.scaler = joblib.load(os.path.join(model_path, 'scaler.pkl'))
            self.feature_names = joblib.load(os.path.join(model_path, 'feature_names.pkl'))
            self.metadata = joblib.load(os.path.join(model_path, 'metadata.pkl'))
            
            self.ml_available = True
            print("✅ ML models loaded successfully!")
            print(f"📅 Models trained on: {self.metadata.get('training_date', 'Unknown')}")
            print(f"📊 Training samples: {self.metadata.get('training_samples', 'Unknown'):,}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading ML models: {e}")
            self.ml_available = False
            return False
    
    def extract_features(self, user_profile):
        """Extract and engineer features from user profile"""
        try:
            # Get basic info
            age = user_profile.get('age', 30)
            monthly_income = user_profile.get('avg_monthly_income', 50000)
            monthly_expenses = user_profile.get('monthly_expenses', 30000)
            surplus = monthly_income - monthly_expenses
            dependents = user_profile.get('dependents', 1)
            income_stability = user_profile.get('income_stability', 3)
            
            # Calculate derived features
            surplus_to_income_ratio = surplus / monthly_income if monthly_income > 0 else 0
            expense_ratio = monthly_expenses / monthly_income if monthly_income > 0 else 1
            
            # Calculate risk capacity
            risk_capacity = self.calculate_risk_capacity(age, income_stability, dependents, surplus)
            
            # Calculate interaction features
            age_income_interaction = age * monthly_income / 100000
            stability_surplus_interaction = income_stability * surplus / 1000
            
            # Create feature array in correct order
            features = [
                age,
                monthly_income,
                monthly_expenses,
                surplus,
                dependents,
                income_stability,
                surplus_to_income_ratio,
                expense_ratio,
                risk_capacity,
                age_income_interaction,
                stability_surplus_interaction
            ]
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def calculate_risk_capacity(self, age, income_stability, dependents, surplus):
        """Calculate risk capacity score (1-10 scale)"""
        risk_score = 5  # Start with neutral
        
        # Age factor (younger = higher risk tolerance)
        if age < 30:
            risk_score += 2
        elif age < 40:
            risk_score += 1
        elif age > 50:
            risk_score -= 1
        elif age > 55:
            risk_score -= 2
        
        # Income stability factor
        risk_score += (income_stability - 3)  # Stability around 3 is neutral
        
        # Dependents factor (more dependents = lower risk)
        risk_score -= dependents * 0.5
        
        # Surplus factor
        if surplus > 50000:
            risk_score += 2
        elif surplus > 20000:
            risk_score += 1
        elif surplus < 10000:
            risk_score -= 1
        
        # Ensure score is within bounds
        return max(1, min(10, risk_score))
    
    def predict_portfolio_allocation(self, user_profile):
        """Predict optimal portfolio allocation using ML"""
        if not self.ml_available:
            return None
        
        try:
            # Extract and scale features
            features = self.extract_features(user_profile)
            if features is None:
                return None
            
            features_scaled = self.scaler.transform(features)
            
            # Get predictions from portfolio models
            allocations = {}
            confidence_scores = {}
            
            portfolio_models = self.models.get('portfolio_allocator', {})
            
            for target, model_info in portfolio_models.items():
                model = model_info['model']
                prediction = model.predict(features_scaled)[0]
                
                # Ensure allocation is between 0 and 1
                allocation = max(0, min(1, prediction))
                allocations[target.replace('_allocation', '')] = allocation
                
                # Use CV score as confidence
                confidence_scores[target] = model_info.get('cv_score', 0.5)
            
            # Normalize allocations to sum to 1
            total_allocation = sum(allocations.values())
            if total_allocation > 0:
                for key in allocations:
                    allocations[key] = allocations[key] / total_allocation
            
            # Predict expected return
            expected_return = self.predict_expected_return(features_scaled)
            
            return {
                'allocations': allocations,
                'expected_return': expected_return,
                'confidence_scores': confidence_scores,
                'model_used': 'ML',
                'prediction_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"ML prediction error: {e}")
            return None
    
    def predict_expected_return(self, features_scaled):
        """Predict expected portfolio return"""
        try:
            return_model = self.models.get('return_predictor', {}).get('model')
            if return_model is None:
                return 8.0  # Default return
            
            predicted_return = return_model.predict(features_scaled)[0]
            
            # Ensure realistic return range (4-18%)
            return max(4.0, min(18.0, predicted_return))
            
        except Exception as e:
            print(f"Return prediction error: {e}")
            return 8.0
    
    def generate_ml_recommendations(self, user_profile):
        """Generate detailed investment recommendations using ML predictions"""
        ml_results = self.predict_portfolio_allocation(user_profile)
        
        if ml_results is None:
            return self.fallback_recommendation(user_profile)
        
        allocations = ml_results['allocations']
        expected_return = ml_results['expected_return']
        surplus = user_profile['avg_monthly_income'] - user_profile['monthly_expenses']
        
        recommendations = []
        priority = 1
        
        # Emergency Fund
        if allocations.get('emergency_fund', 0) > 0.05:
            amount = surplus * allocations['emergency_fund']
            recommendations.append({
                'priority': priority,
                'investment_type': 'emergency_fund',
                'amount': amount,
                'percentage': allocations['emergency_fund'] * 100,
                'reason': f'AI recommends {allocations["emergency_fund"]*100:.1f}% emergency fund based on your risk profile and income stability',
                'how_to_start': 'Keep in high-yield savings account or liquid mutual fund for immediate access',
                'expected_return': 4.0,
                'ml_confidence': ml_results['confidence_scores'].get('emergency_fund_allocation', 0.8)
            })
            priority += 1
        
        # Equity Investment
        if allocations.get('equity', 0) > 0.05:
            amount = surplus * allocations['equity']
            recommendations.append({
                'priority': priority,
                'investment_type': 'mutual_fund_sip',
                'amount': amount,
                'percentage': allocations['equity'] * 100,
                'reason': f'ML model suggests {allocations["equity"]*100:.1f}% equity allocation for optimal risk-adjusted returns based on your age and risk capacity',
                'how_to_start': 'Start SIP in diversified equity mutual funds through apps like Groww, Zerodha, or ET Money',
                'expected_return': 12.0,
                'ml_confidence': ml_results['confidence_scores'].get('equity_allocation', 0.8)
            })
            priority += 1
        
        # Debt Investment
        if allocations.get('debt', 0) > 0.05:
            amount = surplus * allocations['debt']
            investment_type = 'ppf' if amount > 12000 and user_profile.get('age', 30) < 50 else 'fd'
            recommendations.append({
                'priority': priority,
                'investment_type': investment_type,
                'amount': amount,
                'percentage': allocations['debt'] * 100,
                'reason': f'AI analysis recommends {allocations["debt"]*100:.1f}% debt allocation for portfolio stability and consistent returns',
                'how_to_start': 'Consider PPF for long-term tax benefits or FD for shorter duration with guaranteed returns',
                'expected_return': 7.1 if investment_type == 'ppf' else 6.8,
                'ml_confidence': ml_results['confidence_scores'].get('debt_allocation', 0.8)
            })
            priority += 1
        
        # Gold Investment
        if allocations.get('gold', 0) > 0.05:
            amount = surplus * allocations['gold']
            recommendations.append({
                'priority': priority,
                'investment_type': 'gold',
                'amount': amount,
                'percentage': allocations['gold'] * 100,
                'reason': f'Machine learning suggests {allocations["gold"]*100:.1f}% gold allocation for portfolio diversification and inflation protection',
                'how_to_start': 'Invest in digital gold through apps like Paytm, PhonePe, or Gold ETFs through mutual fund platforms',
                'expected_return': 8.0,
                'ml_confidence': ml_results['confidence_scores'].get('gold_allocation', 0.8)
            })
            priority += 1
        
        # Generate ML-powered summary
        summary = self.generate_ml_summary(recommendations, surplus, expected_return, ml_results)
        
        return {
            'status': 'success',
            'total_surplus': surplus,
            'recommendations': recommendations,
            'summary': summary,
            'ml_metadata': {
                'model_used': 'ML-Powered',
                'prediction_date': ml_results['prediction_date'],
                'expected_portfolio_return': expected_return,
                'overall_confidence': np.mean(list(ml_results['confidence_scores'].values())),
                'training_date': self.metadata.get('training_date', 'Unknown'),
                'training_samples': self.metadata.get('training_samples', 0)
            }
        }
    
    def generate_ml_summary(self, recommendations, total_surplus, expected_return, ml_results):
        """Generate AI-powered investment summary"""
        confidence = np.mean(list(ml_results['confidence_scores'].values()))
        
        summary = f"""
🤖 AI-Powered Investment Analysis:

💰 Total Investment Amount: ₹{total_surplus:,.0f}
📈 ML Predicted Portfolio Return: {expected_return:.1f}% per year
🎯 Investment Strategy: {"Conservative" if expected_return < 8 else "Moderate" if expected_return < 12 else "Aggressive"}
📊 AI Confidence Level: {confidence:.1%}

🧠 Machine Learning Insights:
• Model Type: Advanced ML (Random Forest + Gradient Boosting)
• Training Data: {self.metadata.get('training_samples', 0):,} historical investor profiles
• Feature Analysis: Analyzed {len(self.feature_names)} financial parameters
• Personalization: Custom allocation based on your unique risk profile

🔥 Key AI Recommendations:
• Emergency fund optimized for your income stability level
• Equity allocation calibrated to your age and risk capacity  
• Debt-equity balance calculated using machine learning algorithms
• Gold allocation for inflation hedging and portfolio diversification

💡 Smart Tip: AI recommends systematic monthly investments (SIP) for rupee cost averaging!

⚡ Model Performance: {confidence:.1%} confidence based on historical accuracy
        """
        
        return summary.strip()
    
    def fallback_recommendation(self, user_profile):
        """Fallback rule-based recommendation if ML fails"""
        print("🔄 Using fallback rule-based recommendation")
        
        income = user_profile.get('avg_monthly_income', 50000)
        expenses = user_profile.get('monthly_expenses', 30000)
        surplus = income - expenses
        age = user_profile.get('age', 30)
        stability = user_profile.get('income_stability', 3)
        
        recommendations = []
        
        # Emergency Fund
        emergency_amount = min(expenses * 3, surplus * 0.35)
        if emergency_amount >= 500:
            recommendations.append({
                'priority': 1,
                'investment_type': 'emergency_fund',
                'amount': emergency_amount,
                'percentage': (emergency_amount / surplus) * 100,
                'reason': 'Essential emergency fund for financial security',
                'how_to_start': 'Keep in easily accessible savings account',
                'expected_return': 4.0
            })
        
        remaining = surplus - emergency_amount
        
        # Basic allocation based on stability
        if stability <= 2:  # Low stability
            if remaining >= 1000:
                recommendations.append({
                    'priority': 2,
                    'investment_type': 'fd',
                    'amount': remaining * 0.8,
                    'percentage': (remaining * 0.8 / surplus) * 100,
                    'reason': 'Safe fixed deposits for irregular income',
                    'how_to_start': 'Open FD in reliable bank',
                    'expected_return': 6.8
                })
        else:  # Moderate to high stability
            if remaining >= 1500:
                recommendations.append({
                    'priority': 2,
                    'investment_type': 'mutual_fund_sip',
                    'amount': remaining * 0.6,
                    'percentage': (remaining * 0.6 / surplus) * 100,
                    'reason': 'Equity mutual funds for long-term growth',
                    'how_to_start': 'Start SIP through investment apps',
                    'expected_return': 12.0
                })
        
        return {
            'status': 'success',
            'total_surplus': surplus,
            'recommendations': recommendations,
            'summary': f"Rule-based recommendations for ₹{surplus:,} monthly surplus",
            'ml_metadata': {
                'model_used': 'Rule-based (ML unavailable)',
                'prediction_date': datetime.now().isoformat()
            }
        }

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize ML predictor
try:
    ml_predictor = MLInvestmentPredictor()
    if ml_predictor.ml_available:
        print("🤖 ML-powered advisor initialized successfully")
    else:
        print("📊 Using rule-based recommendations (ML models not available)")
except Exception as e:
    print(f"⚠️ Error initializing ML predictor: {e}")
    ml_predictor = None

@app.route('/')
def index():
    """Main page with investment calculator"""
    try:
        # Do not read from query params; use template defaults only
        return render_template('index.html', prefill={})
    except Exception:
        return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """Process user input and return investment recommendations"""
    try:
        # Get form data
        monthly_income = int(request.form.get('monthly_income', 0))
        monthly_expenses = int(request.form.get('monthly_expenses', 0))
        age = int(request.form.get('age', 25))
        dependents = int(request.form.get('dependents', 0))
        income_stability = int(request.form.get('income_stability', 3))
        
        # Validation
        if monthly_income <= 0:
            flash('Please enter a valid monthly income', 'error')
            return redirect(url_for('index'))
            
        if monthly_expenses < 0:
            flash('Monthly expenses cannot be negative', 'error')
            return redirect(url_for('index'))
            
        if monthly_expenses >= monthly_income:
            flash('Your expenses should be less than your income to have surplus for investment', 'error')
            return redirect(url_for('index'))
        
        # Create user profile
        user_profile = {
            'avg_monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'age': age,
            'dependents': dependents,
            'income_stability': income_stability
        }
        
        surplus = monthly_income - monthly_expenses
        
        if surplus <= 0:
            return render_template('recommendations.html', 
                                 data={
                                     'status': 'insufficient_surplus',
                                     'message': 'First reduce your expenses or increase income. You need surplus money to invest.',
                                     'suggestions': [
                                         'Track your monthly expenses carefully',
                                         'Cut down on unnecessary expenses', 
                                         'Look for additional income sources',
                                         'Develop skills to get better paying job'
                                     ]
                                 },
                                 config=Config)
        
        print(f"Processing investment recommendation for surplus: ₹{surplus:,}")
        
        # Generate recommendations using ML or fallback
        if ml_predictor and ml_predictor.ml_available:
            recommendations = ml_predictor.generate_ml_recommendations(user_profile)
        else:
            # Fallback logic
            recommendations = ml_predictor.fallback_recommendation(user_profile) if ml_predictor else {
                'status': 'error',
                'message': 'Recommendation system unavailable'
            }
        
        # Add user profile for display
        recommendations['user_profile'] = user_profile
        
        print(f"Generated {len(recommendations.get('recommendations', []))} investment recommendations")
        
        return render_template('recommendations.html', 
                             data=recommendations, 
                             config=Config)
        
    except ValueError as e:
        flash('Please enter valid numeric values for all fields', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        traceback.print_exc()
        flash(f'An error occurred while processing your request. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/recommendations', methods=['POST'])
def api_recommendations():
    """API endpoint for getting recommendations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        user_profile = {
            'avg_monthly_income': int(data.get('monthly_income', 0)),
            'monthly_expenses': int(data.get('monthly_expenses', 0)),
            'age': int(data.get('age', 25)),
            'dependents': int(data.get('dependents', 0)),
            'income_stability': int(data.get('income_stability', 3))
        }
        
        if user_profile['avg_monthly_income'] <= 0:
            return jsonify({
                'status': 'error',
                'message': 'Monthly income must be greater than 0'
            }), 400
        
        # Generate recommendations
        if ml_predictor and ml_predictor.ml_available:
            recommendations = ml_predictor.generate_ml_recommendations(user_profile)
        else:
            recommendations = {'status': 'error', 'message': 'ML models not available'}
        
        return jsonify({
            'status': 'success',
            'data': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/current_rates')
def current_rates():
    """Display current market rates"""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Current Market Rates</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background: linear-gradient(135deg, #0A0E1A 0%, #1E293B 100%); color: white; min-height: 100vh; }}
        .card {{ background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(74, 144, 226, 0.2); }}
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center text-primary mb-5">📊 Current Market Rates</h1>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5><i class="fas fa-university"></i> Fixed Deposit Rates</h5>
                    </div>
                    <div class="card-body">
                        <div class="list-group list-group-flush">
                            <div class="list-group-item d-flex justify-content-between" style="background: transparent; border-color: rgba(74, 144, 226, 0.2);">
                                <span>SBI</span>
                                <span class="badge bg-success">6.7% p.a.</span>
                            </div>
                            <div class="list-group-item d-flex justify-content-between" style="background: transparent; border-color: rgba(74, 144, 226, 0.2);">
                                <span>HDFC Bank</span>
                                <span class="badge bg-success">7.0% p.a.</span>
                            </div>
                            <div class="list-group-item d-flex justify-content-between" style="background: transparent; border-color: rgba(74, 144, 226, 0.2);">
                                <span>ICICI Bank</span>
                                <span class="badge bg-success">7.0% p.a.</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5><i class="fas fa-chart-line"></i> Other Rates</h5>
                    </div>
                    <div class="card-body">
                        <div class="list-group list-group-flush">
                            <div class="list-group-item d-flex justify-content-between" style="background: transparent; border-color: rgba(74, 144, 226, 0.2);">
                                <span>PPF</span>
                                <span class="badge bg-warning">7.1% p.a.</span>
                            </div>
                            <div class="list-group-item d-flex justify-content-between" style="background: transparent; border-color: rgba(74, 144, 226, 0.2);">
                                <span>Inflation Rate</span>
                                <span class="badge bg-danger">6.2% p.a.</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-4">
            <a href="{url_for('index')}" class="btn btn-primary btn-lg">
                <i class="fas fa-arrow-left"></i> Back to Calculator
            </a>
        </div>
    </div>
</body>
</html>"""
    return html_content

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    ml_status = "available" if ml_predictor and ml_predictor.ml_available else "unavailable"
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Simple Investment Advisor',
        'ml_models': ml_status,
        'model_info': {
            'training_date': ml_predictor.metadata.get('training_date') if ml_predictor and ml_predictor.ml_available else None,
            'training_samples': ml_predictor.metadata.get('training_samples') if ml_predictor and ml_predictor.ml_available else None
        } if ml_predictor and ml_predictor.ml_available else None
    })

@app.route('/model_info')
def model_info():
    """Display ML model information"""
    if not ml_predictor or not ml_predictor.ml_available:
        return jsonify({'error': 'ML models not available'}), 404
    
    return jsonify({
        'model_metadata': ml_predictor.metadata,
        'feature_names': ml_predictor.feature_names,
        'model_performance': ml_predictor.metadata.get('model_performance', {}),
        'load_status': 'success'
    })

@app.route('/investment_guide/<investment_type>')
def investment_guide(investment_type):
    """Detailed guide for a specific investment type."""
    try:
        option = Config.INVESTMENT_OPTIONS.get(investment_type)
        if not option:
            flash('Unknown investment type selected.', 'error')
            return redirect(url_for('index'))
        return render_template('investment_guide.html', 
                               investment_type=investment_type,
                               option=option,
                               config=Config)
    except Exception as e:
        print(f"Error rendering investment guide for {investment_type}: {e}")
        traceback.print_exc()
        flash('Could not open the investment guide. Please try again.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return f"""<!DOCTYPE html>
<html><head><title>Page Not Found</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body {{ background: #0A0E1A; color: white; }}</style>
</head><body>
<div class="container mt-5 text-center">
    <h1 class="text-danger">404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="{url_for('index')}" class="btn btn-primary">Go Home</a>
</div></body></html>""", 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return f"""<!DOCTYPE html>
<html><head><title>Server Error</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body {{ background: #0A0E1A; color: white; }}</style>
</head><body>
<div class="container mt-5 text-center">
    <h1 class="text-danger">500 - Server Error</h1>
    <p>Something went wrong. Please try again.</p>
    <a href="{url_for('index')}" class="btn btn-primary">Go Home</a>
</div></body></html>""", 500

if __name__ == '__main__':
    print("🚀 Starting Simple Investment Advisor...")
    print(f"📂 Current directory: {os.getcwd()}")
    
    # Check for ML models
    if ml_predictor and ml_predictor.ml_available:
        print("🤖 ML-powered recommendations enabled")
        print(f"📊 Model confidence: {ml_predictor.metadata.get('validation_results', {}).get('overall_model_score', 'Unknown')}")
    else:
        print("📊 Using rule-based recommendations (generate ML models for enhanced features)")
    
    print("🌐 Server starting on http://localhost:5000")
    print("=" * 60)
    
        port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
