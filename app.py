#!/usr/bin/env python3
"""
Flask web application for DeFi Portfolio Tracker
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from defi_tracker import calculate_defi_score

# Load environment variables
load_dotenv()

# Application root path for subpath deployment
# Can be overridden via SCRIPT_NAME environment variable
APPLICATION_ROOT = os.environ.get('SCRIPT_NAME', '/ethereum-wallet-defi-score')

app = Flask(__name__)

# Configure application root for subpath deployment
app.config['APPLICATION_ROOT'] = APPLICATION_ROOT

# In-memory storage for recent wallets (max 5)
recent_wallets = []


def get_base_path():
    """Get the base path from request or use default."""
    # Try to get from SCRIPT_NAME (set by reverse proxy)
    script_name = request.environ.get('SCRIPT_NAME', '')
    if script_name:
        return script_name
    # Try to get from HTTP_X_SCRIPT_NAME (some proxies use this)
    http_script_name = request.environ.get('HTTP_X_SCRIPT_NAME', '')
    if http_script_name:
        return http_script_name
    # Try to detect from request path
    path = request.path
    if path.startswith('/ethereum-wallet-defi-score'):
        return '/ethereum-wallet-defi-score'
    # Fallback to configured APPLICATION_ROOT
    return APPLICATION_ROOT


# ============================================================================
# ROUTES - Dual registration for subpath deployment
# ============================================================================

@app.route(f'{APPLICATION_ROOT}/')
@app.route('/')
def index():
    """Main page with search form"""
    base_path = get_base_path()
    return render_template('index.html', base_path=base_path)


@app.route(f'{APPLICATION_ROOT}/api/calculate', methods=['POST'])
@app.route('/api/calculate', methods=['POST'])
def calculate():
    """API endpoint to calculate DeFi score"""
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        # Validate address format
        if not address.startswith('0x') or len(address) != 42:
            return jsonify({'error': 'Invalid Ethereum address format'}), 400
        
        # Get API key
        api_key = os.getenv('BITQUERY_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500
        
        # Calculate score with debug output
        print(f"\n{'='*80}")
        print(f"DEBUG: Calculating DeFi Score for {address}")
        print(f"{'='*80}")
        result = calculate_defi_score(address, api_key, verbose=True)
        
        # Create new wallet entry
        new_wallet = {
            'address': result['address'],
            'p1': result['p1']['score'],
            'p1_tx_count': result['p1'].get('tx_count'),
            'p2': result['p2']['score'],
            'p2_unique_types': result['p2'].get('unique_types'),
            'p3': result['p3']['score'],
            'p3_unique_protocols': result['p3'].get('unique_protocols'),
            'p4': result['p4']['score'],
            'p4_unique_assets': result['p4'].get('unique_assets'),
            'final_score': result['final_score_rounded']
        }
        
        # Update module-level recent_wallets list
        global recent_wallets
        
        # Remove any existing entry with the same address to avoid duplicates
        recent_wallets = [w for w in recent_wallets if w['address'].lower() != address.lower()]
        
        # Add new entry to the front
        recent_wallets.insert(0, new_wallet)
        
        # Keep only the most recent 5
        recent_wallets = recent_wallets[:5]
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"ERROR in calculate endpoint: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': error_msg}), 500


@app.route(f'{APPLICATION_ROOT}/api/recent', methods=['GET'])
@app.route('/api/recent', methods=['GET'])
def get_recent():
    """API endpoint to get recent wallet results"""
    return jsonify({
        'success': True,
        'data': list(recent_wallets)
    })


if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f"Ethereum Wallet DeFi Score")
    print(f"APPLICATION_ROOT: {APPLICATION_ROOT}")
    print(f"Access at: http://localhost:5001/")
    print(f"      or: http://localhost:5001{APPLICATION_ROOT}/")
    print(f"{'='*60}\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
