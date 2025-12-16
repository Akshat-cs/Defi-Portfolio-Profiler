# DeFi Address Profiler

A web application that analyzes Ethereum wallet addresses and calculates a DeFi Strategy Score based on transaction patterns, protocol interactions, and asset holdings.

## Features

- **DeFi Strategy Score**: Calculate a score from 25-100 based on four key pillars
- **Real-time Analysis**: Uses Bitquery APIs to fetch live blockchain data
- **Comprehensive Metrics**: 
  - Transaction count and activity level
  - Diversity of DeFi interactions (8 activity types)
  - Protocol usage across major DeFi platforms
  - Asset portfolio diversity (ERC-20 tokens and NFTs)
- **Modern Web Interface**: Clean, minimal UI with detailed explanations and FAQ

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:
```
BITQUERY_API_KEY=your_bitquery_api_key_here
```

3. Run the Flask application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Web Interface

1. Enter an Ethereum address in the search box
2. Click "Analyze" to calculate the DeFi Strategy Score
3. View detailed breakdown of all four pillars (P1-P4)
4. Read the FAQ section for more information

### Command Line

You can also use the CLI tool directly:

```bash
python defi_tracker.py 0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862
```

## How It Works

The DeFi Strategy Score is calculated using:

**Formula**: `25 (Base Score) + (Average Pillar Score × 0.75)`

**Four Pillars**:
- **P1: Transaction Count** - Measures overall activity (0-10 TXs = 0 points, 100+ TXs = 100 points)
- **P2: Transaction Types** - Measures diversity (1 type = 0 points, 5+ types = 100 points)
- **P3: Protocols Used** - Measures ecosystem engagement (1 protocol = 0 points, 8+ protocols = 100 points)
- **P4: Assets Held** - Measures portfolio diversity (1 asset = 0 points, 15+ assets = 100 points)

## Data Source

All blockchain data is sourced from [Bitquery](https://bitquery.io/), a leading blockchain data analytics platform. The application queries Ethereum mainnet data including:
- Transaction history
- Smart contract interactions
- Token balances
- NFT holdings

## Privacy

- No wallet addresses are stored or logged
- All analysis is performed in real-time
- Only publicly available on-chain data is accessed

## Requirements

- Python 3.7+
- Bitquery API key
- Internet connection for API calls

## License

This project is provided as-is for analysis purposes.

