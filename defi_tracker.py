#!/usr/bin/env python3
"""
DeFi Portfolio Tracker - Calculates DeFi Strategy Score for Ethereum addresses
"""

import os
import sys
import argparse
import requests
from typing import Dict, List, Optional, Set, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bitquery endpoint
BITQUERY_ENDPOINT = "https://streaming.bitquery.io/graphql"

# Protocol addresses organized by category
PROTOCOL_ADDRESSES = {
    "lending": [
        # Aave v3
        "0xd01607c3C5eCABa394D8be377a08590149325722",
        "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        # Aave v2
        "0xa0d9C1E9E48Ca30c8d8C3B5D69FF5dc1f6DFfC24",
        "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
        # Compound v2
        "0xe65cdB6479BaC1e22340E4E755fAE7E509EcD06c",
        "0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E",
        "0x70e36f6BF80a52b3B46b3aF8e106CC0ed743E8e4",
        "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643",
        "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5",
        "0x7713DD9Ca933848F6819F38B8352D9A15EA73F67",
        "0xFAce851a4921ce59e912d19329929CE6da6EB0c7",
        "0x95b4eF2869eBD94BEb4eEE400a99824BF5DC325b",
        "0x158079Ee67Fce2f58472A96584A73C7Ab9AC95c1",
        "0xF5DCe57282A584D2746FaF1593d3121Fcac444dC",
        "0x4B0181102A0112A2ef11AbEE5563bb4a3176c9d7",
        "0x12392F67bdf24faE0AF363c24aC620a2f67DAd86",
        "0x35A18000230DA775CAc24873d00Ff85BccdeD550",
        "0x39AA39c021dfbaE8faC545936693aC917d5E7563",
        "0x041171993284df560249B57358F931D9eB7b925D",
        "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9",
        "0xC11b1268C1A384e55C48c2391d8d480264A3A7F4",
        "0xccF4429DB6322D5C611ee964527D42E5d685DD6a",
        "0x80a2AE356fc9ef4305676f7a3E2Ed04e12C33946",
        "0xB3319f5D18Bc0D84dD1b4825Dcde5d5f7266d407",
        "0xc00e94Cb662C3520282E6f5717214004A7f26888",
        "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B",
        "0xc0Da02939E1441F497fd74F78cE7Decb17B66529",
        "0x6d903f6003cca6255D85CcA4D3B5E5146dC33925",
        # Compound v3
        "0xc3d688B66703497DAA19211EEdff47f25384cdc3",
        "0xA17581A9E3356d9A858b789D68B4d866e593aE94",
        "0x3Afdc9BCA9213A35503b077a6072F3D0d5AB0840",
        "0x3D0bb1ccaB520A66e607822fC55BC921738fAFE3",
        "0x5D409e56D886231aDAf00c8775665AD0f9897b56",
        # Sparklend
        "0xC13e21B648A5Ee794902342038FF3aDAB66BE987",
        # Morpho
        "0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb",
    ],
    "staking": [
        # Ethereum 2.0
        "0x00000000219ab540356cBB839Cbe05303d7705Fa",
        # Lido
        "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
        "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
        # RocketPool
        "0xDD3f50F8A6CafbE9b31a427582963f465E745AF8",
        # Swell
        "0xFAe103DC9cf190eD75350761e95403b7b8aFa6c0",
        # Coinbase cbETH
        "0xBe9895146f7AF43049ca1c1AE358B0541Ea49704",
        # Frax Ether
        "0xac3E018457B222d93114458476f3E3416Abbe38F",
    ],
    "liquidity": [
        # Uniswap v3
        "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
    ],
    "bridging": [
        # Across
        "0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5",
        # Stargate
        "0x8731d54E9D02c286767d56ac03e8037C07e01e98",
        "0x150f94B44927F078737562f0fcF3C95c01Cc2376",
    ],
    "yield_farming": [
        # Yearn Finance
        "0xdA816459F1AB5631232FE5e97a05BBBb94970c95",
        "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9",
        "0x7Da96a3891Add058AdA2E826306D812C638D87A7",
        "0xa258C4606Ca8206D8aA700cE2143D7db854D168c",
        # Convex Finance
        "0xF403C135812408BFbE8713b5A23a04b3D48AAE31",
    ],
}

# Get all protocol addresses for P3
ALL_PROTOCOL_ADDRESSES = []
for addresses in PROTOCOL_ADDRESSES.values():
    ALL_PROTOCOL_ADDRESSES.extend(addresses)


class BitqueryClient:
    """Client for interacting with Bitquery GraphQL API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = BITQUERY_ENDPOINT
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
    
    def execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query"""
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=self.headers,
                timeout=200
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                raise Exception(f"GraphQL errors: {data['errors']}")
            
            return data.get("data", {})
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")


def calculate_p1_score(tx_count: int) -> float:
    """Calculate P1 score based on transaction count"""
    if tx_count <= 10:
        return 0.0
    if tx_count >= 100:
        return 100.0
    
    # Linear interpolation between 10 and 100
    return min(100.0, ((tx_count - 10) / (100 - 10)) * 100.0)


def calculate_p2_score(unique_types: int) -> float:
    """Calculate P2 score based on unique transaction types"""
    if unique_types <= 1:
        return 0.0
    if unique_types >= 5:
        return 100.0
    
    # Linear interpolation between 1 and 5
    return min(100.0, ((unique_types - 1) / (5 - 1)) * 100.0)


def calculate_p3_score(unique_protocols: int) -> float:
    """Calculate P3 score based on unique protocols used"""
    if unique_protocols <= 1:
        return 0.0
    if unique_protocols >= 8:
        return 100.0
    
    # Linear interpolation between 1 and 8
    return min(100.0, ((unique_protocols - 1) / (8 - 1)) * 100.0)


def calculate_p4_score(unique_assets: int) -> float:
    """Calculate P4 score based on unique assets held"""
    if unique_assets <= 1:
        return 0.0
    if unique_assets >= 15:
        return 100.0
    
    # Linear interpolation between 1 and 15
    return min(100.0, ((unique_assets - 1) / (15 - 1)) * 100.0)


def get_p1_transaction_count(client: BitqueryClient, address: str) -> int:
    """Get transaction count for P1"""
    query = """
    query MyQuery($address: String) {
      EVM(network: eth, dataset: combined) {
        Transactions(
          where: {Transaction: {From: {is: $address}}, Block: {Time: {since_relative: {years_ago: 1}}}, TransactionStatus: {Success: true}}
        ){
          count
        }
      }
    }
    """
    
    variables = {"address": address}
    data = client.execute_query(query, variables)
    
    try:
        count = data.get("EVM", {}).get("Transactions", [{}])[0].get("count", 0)
        return int(count) if count else 0
    except (KeyError, IndexError, ValueError):
        return 0


def get_p2_p3_data(client: BitqueryClient, address: str) -> Tuple[Set[str], Set[str]]:
    """Get transaction types and protocols for P2 and P3"""
    query = """
    query MyQuery($protocols: [String!], $address: String) {
      EVM(network: eth, dataset: combined) {
        Calls(
          where: {Block:{Time:{since_relative:{years_ago:1}}} Call: {To: {in: $protocols }}, TransactionStatus: {Success: true}, Transaction: {From: {is:$address}}}
        ) {
          Call {
            To
          }
          count(distinct:Transaction_Hash)
        }
      }
    }
    """
    
    variables = {
        "address": address,
        "protocols": ALL_PROTOCOL_ADDRESSES
    }
    
    data = client.execute_query(query, variables)
    
    interacted_protocols = set()
    activity_types = set()
    
    try:
        calls = data.get("EVM", {}).get("Calls", [])
        for call in calls:
            protocol_address = call.get("Call", {}).get("To", "")
            if protocol_address:
                # Normalize address to lowercase for comparison and storage
                protocol_address_lower = protocol_address.lower()
                interacted_protocols.add(protocol_address_lower)
                
                # Determine activity type based on protocol (check lowercase)
                if any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["lending"]):
                    activity_types.add("Lending")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["staking"]):
                    activity_types.add("Staking")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["liquidity"]):
                    activity_types.add("Liquidity")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["bridging"]):
                    activity_types.add("Bridging")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["yield_farming"]):
                    activity_types.add("Yield Farming")
    except (KeyError, TypeError):
        pass
    
    return activity_types, interacted_protocols


def get_dex_and_nft_activity(client: BitqueryClient, address: str) -> Tuple[bool, bool]:
    """Get DEX swaps and NFT trading activity"""
    query = """
    query MyQuery($address: String) {
      EVM(network: eth, dataset: combined) {
        DEXTrades(
          where: {Block: {Time: {since_relative: {years_ago: 1}}}, Transaction: {From: {is: $address}}, TransactionStatus: {Success: true}}
        ) {
          dex_count_fungible:count(distinct:Trade_Dex_ProtocolName if:{Trade:{Buy:{Currency:{Fungible:true}}}})
          dex_count_nonfungible:count(distinct:Trade_Dex_ProtocolName if:{Trade:{Buy:{Currency:{Fungible:false}}}})
        }
      }
    }
    """
    
    variables = {"address": address}
    data = client.execute_query(query, variables)
    
    has_dex = False
    has_nft_trading = False
    
    try:
        trades = data.get("EVM", {}).get("DEXTrades", [{}])[0]
        if trades.get("dex_count_fungible", 0) > 0:
            has_dex = True
        if trades.get("dex_count_nonfungible", 0) > 0:
            has_nft_trading = True
    except (KeyError, IndexError, TypeError):
        pass
    
    return has_dex, has_nft_trading


def get_governance_activity(client: BitqueryClient, address: str) -> bool:
    """Check for governance activity"""
    query = """
    query MyQuery($address: String) {
      EVM(network: eth, dataset: combined) {
        Calls(
          where: {Block: {Time: {since_relative: {years_ago: 1}}}, Call: {Signature: {Name: {includesCaseInsensitive: "vote"}}}, Transaction:{From:{is:$address}} ,TransactionStatus: {Success: true}}
        ) {
          count
        }
      }
    }
    """
    
    variables = {"address": address}
    data = client.execute_query(query, variables)
    
    try:
        count = data.get("EVM", {}).get("Calls", [{}])[0].get("count", 0)
        return int(count) > 0 if count else False
    except (KeyError, IndexError, TypeError):
        return False


def get_p4_assets(client: BitqueryClient, address: str) -> int:
    """Get unique assets count for P4 (ERC-20 > $10 + NFTs)"""
    # Get ERC-20 tokens with balance > $10 using BalanceUpdates
    erc20_query = """
    query MyQuery($address: String) {
      EVM(network: eth, dataset: combined) {
        BalanceUpdates(
          orderBy: {descendingByField: "Balance_usd"}
          where: {BalanceUpdate: {Address: {is: $address}}, Currency: {Fungible: true}}
        ) {
          BalanceUpdate {
            Address
          }
          Currency{
            Name
            Symbol
            SmartContract
          }
          Balance:sum(of:BalanceUpdate_Amount selectWhere:{gt:"0"})
          Balance_usd:sum(of:BalanceUpdate_AmountInUSD selectWhere:{ge:"10"})
        }
      }
    }
    """
    
    # Get NFT balances
    nft_query = """
    query MyQuery($address: String) {
      EVM(dataset: combined, network: eth) {
        BalanceUpdates(
          where: {BalanceUpdate: {Address: {is: $address}}, Currency: {Fungible: false}}
          orderBy: {descendingByField: "balance"}
        ) {
          Currency {
            Name
            Symbol
            SmartContract
          }
          balance: sum(of: BalanceUpdate_Amount)
        }
      }
    }
    """
    
    unique_assets = set()
    nft_count = 0
    
    # Get ERC-20 tokens
    try:
        erc20_data = client.execute_query(erc20_query, {"address": address})
        balances = erc20_data.get("EVM", {}).get("BalanceUpdates", [])
        for balance in balances:
            # Only count if Balance_usd exists (meaning >= $10)
            balance_usd = balance.get("Balance_usd")
            if balance_usd:
                currency = balance.get("Currency", {})
                contract = currency.get("SmartContract", "")
                if contract:
                    unique_assets.add(contract)
    except Exception:
        pass
    
    # Get NFTs - count individual NFTs (sum of balances), not collections
    try:
        nft_data = client.execute_query(nft_query, {"address": address})
        nft_balances = nft_data.get("EVM", {}).get("BalanceUpdates", [])
        for nft_balance in nft_balances:
            balance_str = nft_balance.get("balance", "0")
            try:
                balance_value = int(float(balance_str))
                nft_count += balance_value
            except (ValueError, TypeError):
                pass
    except Exception:
        pass
    
    # Total assets = ERC-20 tokens + individual NFT count
    # According to the doc: "Holding any NFT adds 1 to the asset count" but the example shows
    # counting individual NFTs (29 NFTs), so we'll use the sum of NFT balances
    total_assets = len(unique_assets) + nft_count
    
    return total_assets


def calculate_defi_score(address: str, api_key: str, verbose: bool = True) -> Dict:
    """Calculate DeFi Strategy Score for an address"""
    client = BitqueryClient(api_key)
    
    if verbose:
        print(f"Calculating DeFi Score for {address}...")
    
    # P1: Transaction Count
    if verbose:
        print("  → Fetching transaction count (P1)...")
    try:
        tx_count = get_p1_transaction_count(client, address)
        p1_score = calculate_p1_score(tx_count)
        if verbose:
            print(f"  ✓ P1 calculated: {tx_count} transactions → {p1_score:.2f} points")
    except Exception as e:
        if verbose:
            print(f"  ✗ Error calculating P1: {str(e)}")
        tx_count = 0
        p1_score = 0.0
    
    # P2 & P3: Transaction Types and Protocols
    if verbose:
        print("  → Fetching protocol interactions (P2 & P3)...")
    try:
        activity_types, interacted_protocols = get_p2_p3_data(client, address)
        
        # Check for DEX and NFT trading
        has_dex, has_nft_trading = get_dex_and_nft_activity(client, address)
        if has_dex:
            activity_types.add("DEX Swaps")
        if has_nft_trading:
            activity_types.add("NFT Trading")
        
        # Check for governance
        has_governance = get_governance_activity(client, address)
        if has_governance:
            activity_types.add("Governance")
        
        unique_types = len(activity_types)
        unique_protocols = len(interacted_protocols)
        
        p2_score = calculate_p2_score(unique_types)
        p3_score = calculate_p3_score(unique_protocols)
        
        if verbose:
            print(f"  ✓ P2 calculated: {unique_types} types → {p2_score:.2f} points")
            print(f"  ✓ P3 calculated: {unique_protocols} protocols → {p3_score:.2f} points")
    except Exception as e:
        if verbose:
            print(f"  ✗ Error calculating P2/P3: {str(e)}")
        unique_types = 0
        unique_protocols = 0
        p2_score = 0.0
        p3_score = 0.0
    
    # P4: Assets Held
    if verbose:
        print("  → Fetching asset holdings (P4)...")
    try:
        unique_assets = get_p4_assets(client, address)
        p4_score = calculate_p4_score(unique_assets)
        if verbose:
            print(f"  ✓ P4 calculated: {unique_assets} assets → {p4_score:.2f} points")
    except Exception as e:
        if verbose:
            print(f"  ✗ Error calculating P4: {str(e)}")
        unique_assets = 0
        p4_score = 0.0
    
    # Calculate final score
    avg_pillar_score = (p1_score + p2_score + p3_score + p4_score) / 4.0
    final_score = 25 + (avg_pillar_score * 0.75)
    final_score_rounded = round(final_score)
    
    return {
        "address": address,
        "p1": {
            "tx_count": tx_count,
            "score": p1_score
        },
        "p2": {
            "unique_types": unique_types,
            "score": p2_score
        },
        "p3": {
            "unique_protocols": unique_protocols,
            "score": p3_score
        },
        "p4": {
            "unique_assets": unique_assets,
            "score": p4_score
        },
        "average_pillar_score": avg_pillar_score,
        "final_score": final_score,
        "final_score_rounded": final_score_rounded
    }


def main():
    parser = argparse.ArgumentParser(
        description="Calculate DeFi Strategy Score for an Ethereum address"
    )
    parser.add_argument(
        "address",
        type=str,
        help="Ethereum address to analyze"
    )
    
    args = parser.parse_args()
    address = args.address.strip()
    
    # Validate address format (basic check)
    if not address.startswith("0x") or len(address) != 42:
        print("Error: Invalid Ethereum address format")
        sys.exit(1)
    
    # Get API key from environment
    api_key = os.getenv("BITQUERY_API_KEY")
    if not api_key:
        print("Error: BITQUERY_API_KEY not found in environment variables")
        print("Please create a .env file with: BITQUERY_API_KEY=your_api_key")
        sys.exit(1)
    
    try:
        result = calculate_defi_score(address, api_key)
        
        print("\n" + "="*60)
        print("DEFI STRATEGY SCORE RESULTS")
        print("="*60)
        print(f"Address: {result['address']}")
        print(f"\nPillar Scores:")
        print(f"  P1 (Transaction Count): {result['p1']['score']:.2f} points ({result['p1']['tx_count']} transactions)")
        print(f"  P2 (Transaction Types): {result['p2']['score']:.2f} points ({result['p2']['unique_types']} types)")
        print(f"  P3 (Protocols Used): {result['p3']['score']:.2f} points ({result['p3']['unique_protocols']} protocols)")
        print(f"  P4 (Assets Held): {result['p4']['score']:.2f} points ({result['p4']['unique_assets']} assets)")
        print(f"\nAverage Pillar Score: {result['average_pillar_score']:.2f}")
        print(f"\nFinal DeFi Strategy Score: {result['final_score_rounded']}")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

