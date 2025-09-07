import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Investment options for low-income users (English)
    INVESTMENT_OPTIONS = {
        'emergency_fund': {
            'name': 'Emergency Fund',
            'name_hindi': 'Emergency Fund',
            'description': 'Money for immediate withdrawal (Savings Account)',
            'min_amount': 500,
            'expected_return': 4.0,
            'risk': 'Very Low',
            'liquidity': 'Immediate',
            'icon': '🚨'
        },
        'fd': {
            'name': 'Fixed Deposit (FD)',
            'name_hindi': 'Fixed Deposit',
            'description': 'Safe bank investment with guaranteed returns',
            'min_amount': 1000,
            'expected_return': 6.8,
            'risk': 'Very Low',
            'liquidity': 'Low',
            'icon': '🏦'
        },
        'mutual_fund_sip': {
            'name': 'Mutual Fund SIP',
            'name_hindi': 'Mutual Fund SIP',
            'description': 'Stock market investment, moderate risk but better returns',
            'min_amount': 500,
            'expected_return': 12.0,
            'risk': 'Medium',
            'liquidity': 'Medium',
            'icon': '📈'
        },
        'gold': {
            'name': 'Digital Gold',
            'name_hindi': 'Digital Gold',
            'description': 'Buy gold to hedge against inflation',
            'min_amount': 100,
            'expected_return': 8.0,
            'risk': 'Low',
            'liquidity': 'High',
            'icon': '🥇'
        },
        'ppf': {
            'name': 'PPF (Public Provident Fund)',
            'name_hindi': 'PPF',
            'description': 'Tax savings + good returns, 15-year lock-in',
            'min_amount': 500,
            'expected_return': 7.1,
            'risk': 'Very Low',
            'liquidity': 'Very Low',
            'icon': '💰'
        },
        'recurring_deposit': {
            'name': 'Recurring Deposit (RD)',
            'name_hindi': 'Recurring Deposit',
            'description': 'Deposit fixed amount every month',
            'min_amount': 500,
            'expected_return': 6.5,
            'risk': 'Very Low',
            'liquidity': 'Medium',
            'icon': '📅'
        }
    }
    
    # Current market rates
    CURRENT_RATES = {
        'inflation': 6.2,
        'repo_rate': 6.5,
        'savings_rate': 4.0,
        'fd_rates': {
            'sbi': 6.7,
            'hdfc': 7.0,
            'icici': 7.0,
            'post_office': 6.9
        }
    }