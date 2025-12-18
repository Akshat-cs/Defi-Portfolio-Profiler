#!/usr/bin/env python3
"""
Flask web application for DeFi Portfolio Tracker
"""

from flask import Flask, render_template, request, jsonify
import os
import json
from dotenv import load_dotenv
from defi_tracker import calculate_defi_score

# Load environment variables
load_dotenv()

# Application root path for subpath deployment
# Can be overridden via SCRIPT_NAME environment variable
# Defaults to empty for local development, set to '/ethereum-wallet-defi-score' in production
APPLICATION_ROOT = os.environ.get('SCRIPT_NAME', '')

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = APPLICATION_ROOT

# File path for storing recent wallets
RECENT_WALLETS_FILE = 'recent_wallets.json'

def load_recent_wallets():
    """Load recent wallets from JSON file"""
    if os.path.exists(RECENT_WALLETS_FILE):
        try:
            with open(RECENT_WALLETS_FILE, 'r') as f:
                data = json.load(f)
                # Ensure we only return the most recent 5
                return data[:5] if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading recent wallets: {e}")
            return []
    return []

def save_recent_wallets(wallets):
    """Save recent wallets to JSON file (keep only most recent 5)"""
    try:
        # Ensure we only save the most recent 5
        wallets_to_save = wallets[:5] if len(wallets) > 5 else wallets
        with open(RECENT_WALLETS_FILE, 'w') as f:
            json.dump(wallets_to_save, f, indent=2)
    except IOError as e:
        print(f"Error saving recent wallets: {e}")

# Load recent wallets on startup
recent_wallets = load_recent_wallets()

@app.route('/')
def index():
    """Main page with search form"""
    return render_template('index.html', application_root=APPLICATION_ROOT)

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
        # NOTE: we store both scores and key metric counts so that
        # previously analyzed wallets can be quickly reloaded on the UI
        # without needing to call the API again.
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
        
        # Save to file
        save_recent_wallets(recent_wallets)
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"ERROR in calculate endpoint: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        # Ensure we return a proper error message
        return jsonify({'error': error_msg}), 500

@app.route('/api/recent', methods=['GET'])
def get_recent():
    """API endpoint to get recent wallet results"""
    return jsonify({
        'success': True,
        'data': list(recent_wallets)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

