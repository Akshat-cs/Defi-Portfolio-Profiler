#!/usr/bin/env python3
"""
Flask web application for DeFi Portfolio Tracker
"""

from flask import Flask, render_template, request, jsonify
import os
from collections import deque
from dotenv import load_dotenv
from defi_tracker import calculate_defi_score

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Store recent 5 wallet results in memory
recent_wallets = deque(maxlen=5)

@app.route('/')
def index():
    """Main page with search form"""
    return render_template('index.html')

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
        
        # Calculate score (suppress console output for web app)
        result = calculate_defi_score(address, api_key, verbose=False)
        
        # Store in recent wallets (adds to front, automatically removes oldest if > 5)
        recent_wallets.appendleft({
            'address': result['address'],
            'p1': result['p1']['score'],
            'p2': result['p2']['score'],
            'p3': result['p3']['score'],
            'p4': result['p4']['score'],
            'final_score': result['final_score_rounded']
        })
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent', methods=['GET'])
def get_recent():
    """API endpoint to get recent wallet results"""
    return jsonify({
        'success': True,
        'data': list(recent_wallets)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

