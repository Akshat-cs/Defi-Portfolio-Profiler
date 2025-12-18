#!/usr/bin/env python3
"""
DeFi Portfolio Tracker - Calculates DeFi Strategy Score for Ethereum addresses
"""

import os
import sys
import argparse
import requests
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bitquery endpoints
BITQUERY_ENDPOINT_V1 = "https://graphql.bitquery.io"  # For Ethereum v1 queries
BITQUERY_ENDPOINT_V2 = "https://streaming.bitquery.io/graphql"  # For EVM v2 queries

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
        # Lido
        "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
        "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
        # RocketPool
        "0xDD3f50F8A6CafbE9b31a427582963f465E745AF8"
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
    ]
}

# Get all protocol addresses for P3
ALL_PROTOCOL_ADDRESSES = []
for addresses in PROTOCOL_ADDRESSES.values():
    ALL_PROTOCOL_ADDRESSES.extend(addresses)

# Presaved response for sample wallet (to avoid API calls)
SAMPLE_WALLET_ADDRESS = "0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862"
SAMPLE_WALLET_RESPONSE = {
    "address": SAMPLE_WALLET_ADDRESS,
    "p1": {
        "tx_count": 156,
        "score": 100.0
    },
    "p2": {
        "unique_types": 2,
        "score": 25.0
    },
    "p3": {
        "unique_protocols": 3,
        "score": 28.57
    },
    "p4": {
        "unique_assets": 29,
        "score": 100.0
    },
    "average_pillar_score": 63.3925,
    "final_score": 72.544375,
    "final_score_rounded": 73
}


def get_time_3_years_ago() -> str:
    """Get ISO8601 timestamp for 3 years ago"""
    three_years_ago = datetime.utcnow() - timedelta(days=3*365)
    return three_years_ago.strftime("%Y-%m-%dT00:00:00Z")


class BitqueryClient:
    """Client for interacting with Bitquery GraphQL API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
    
    def execute_query(self, query: str, variables: Optional[Dict] = None, endpoint: Optional[str] = None) -> Tuple[Dict, float]:
        """Execute a GraphQL query and return result with timing"""
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        # Use v2 endpoint by default, or specified endpoint
        endpoint = endpoint or BITQUERY_ENDPOINT_V2
        
        start_time = time.time()
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=200
            )
            response.raise_for_status()
            data = response.json()
            
            elapsed_time = time.time() - start_time
            
            if "errors" in data:
                error_msg = str(data['errors'])
                raise Exception(f"GraphQL errors: {error_msg}")
            
            return data.get("data", {}), elapsed_time
        except requests.exceptions.RequestException as e:
            elapsed_time = time.time() - start_time
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            elapsed_time = time.time() - start_time
            # Re-raise with proper error message
            raise Exception(f"Query execution failed: {str(e)}")


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


def get_p1_transaction_count(client: BitqueryClient, address: str, time_3yr_ago: str) -> Tuple[int, float]:
    """Get transaction count for P1 using v1 API"""
    query = """
    query MyQuery($address: String, $time3yr_ago: ISO8601DateTime) {
      ethereum {
        transactions(
          txSender: {is: $address}
          time: {since: $time3yr_ago}
        ) {
          count
        }
      }
    }
    """
    
    variables = {
        "address": address,
        "time3yr_ago": time_3yr_ago
    }
    
    print(f"\n  [DEBUG] P1 Transaction Count Query (v1 API) for address: {address}")
    print(f"  [DEBUG] Time filter: {time_3yr_ago}")
    
    try:
        data, elapsed_time = client.execute_query(query, variables, endpoint=BITQUERY_ENDPOINT_V1)
    except Exception as e:
        print(f"  [DEBUG] Error executing P1 query: {str(e)}")
        return 0, 0.0
    
    # Debug: Print raw response
    import json
    print(f"  [DEBUG] P1 Raw API Response:")
    print(f"  {json.dumps(data, indent=2)}")
    print(f"  [DEBUG] P1 Query took: {elapsed_time:.2f}s")
    
    try:
        count = data.get("ethereum", {}).get("transactions", [{}])[0].get("count", 0)
        tx_count = int(count) if count else 0
        print(f"  [DEBUG] Transaction count: {tx_count}")
        return tx_count, elapsed_time
    except (KeyError, IndexError, ValueError) as e:
        print(f"  [DEBUG] Error parsing P1 data: {e}")
        return 0, elapsed_time


def get_p2_p3_data(client: BitqueryClient, address: str, time_3yr_ago: str) -> Tuple[Set[str], Set[str], float]:
    """Get transaction types and protocols for P2 and P3 using v1 API"""
    query = """
    query MyQuery($time3yr_ago: ISO8601DateTime, $protocols: [String!], $address: String) {
      ethereum(network: ethereum) {
        smartContractCalls(
          txFrom: {is: $address}
          smartContractAddress: {in: $protocols}
          time: {since: $time3yr_ago}
        ) {
          smartContract {
            address {
              address
            }
          }
          txc: count
        }
      }
    }
    """
    
    variables = {
        "address": address,
        "protocols": ALL_PROTOCOL_ADDRESSES,
        "time3yr_ago": time_3yr_ago
    }
    
    print(f"\n  [DEBUG] P2/P3 Query (v1 API) - Checking {len(ALL_PROTOCOL_ADDRESSES)} protocol addresses")
    print(f"  [DEBUG] Time filter: {time_3yr_ago}")
    
    try:
        data, elapsed_time = client.execute_query(query, variables, endpoint=BITQUERY_ENDPOINT_V1)
    except Exception as e:
        print(f"  [DEBUG] Error executing P2/P3 query: {str(e)}")
        return set(), set(), 0.0
    
    # Debug: Print raw response
    import json
    print(f"  [DEBUG] P2/P3 Raw API Response:")
    print(f"  {json.dumps(data, indent=2)}")
    print(f"  [DEBUG] P2/P3 Query took: {elapsed_time:.2f}s")
    
    interacted_protocols = set()
    activity_types = set()
    
    try:
        calls = data.get("ethereum", {}).get("smartContractCalls", [])
        print(f"  [DEBUG] Found {len(calls)} protocol interactions")
        
        for call in calls:
            protocol_address = call.get("smartContract", {}).get("address", {}).get("address", "")
            tx_count = call.get("txc", 0)
            if protocol_address:
                # Normalize address to lowercase for comparison and storage
                protocol_address_lower = protocol_address.lower()
                interacted_protocols.add(protocol_address_lower)
                
                print(f"    → Protocol: {protocol_address_lower} ({tx_count} transactions)")
                
                # Determine activity type based on protocol (check lowercase)
                if any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["lending"]):
                    activity_types.add("Lending")
                    print(f"      ✓ Categorized as: Lending")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["staking"]):
                    activity_types.add("Staking")
                    print(f"      ✓ Categorized as: Staking")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["liquidity"]):
                    activity_types.add("Liquidity")
                    print(f"      ✓ Categorized as: Liquidity")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["bridging"]):
                    activity_types.add("Bridging")
                    print(f"      ✓ Categorized as: Bridging")
                elif any(addr.lower() == protocol_address_lower for addr in PROTOCOL_ADDRESSES["yield_farming"]):
                    activity_types.add("Yield Farming")
                    print(f"      ✓ Categorized as: Yield Farming")
                else:
                    print(f"      ⚠ Not categorized (not in protocol list)")
    except (KeyError, TypeError) as e:
        print(f"  [DEBUG] Error parsing P2/P3 data: {e}")
    
    print(f"  [DEBUG] Final P2 Activity Types: {list(activity_types)}")
    print(f"  [DEBUG] Final P3 Protocols Count: {len(interacted_protocols)}")
    print(f"  [DEBUG] P3 Protocol Addresses: {list(interacted_protocols)}")
    
    return activity_types, interacted_protocols, elapsed_time


def get_dex_and_nft_activity(client: BitqueryClient, address: str) -> Tuple[int, int, Set[str], float]:
    """Get DEX swaps and NFT trading activity using v2 API
    Returns: (dex_count_fungible, dex_count_nonfungible, dex_protocols, elapsed_time)
    Query: https://ide.bitquery.io/Get-DEX-swaps-and-NFT-trading-activity-using-v2-API
    """
    query = """
    query TraderDexMarketsEvm($network: evm_network!, $trader: String!) {
      EVM(network: $network) {
        DEXTradeByTokens(
          where: {TransactionStatus: {Success: true}, Block: {Time: {since_relative: {years_ago: 3}}}, any: [{Trade: {Seller: {is: $trader}}}, {Trade: {Buyer: {is: $trader}}}]}
        ) {
          dex_count_fungible: count(
            distinct: Trade_Dex_ProtocolName
            if: {Trade: {Currency: {Fungible: true}}}
          )
          dex_count_nonfungible: count(
            distinct: Trade_Dex_ProtocolName
            if: {Trade: {Currency: {Fungible: false}}}
          )
        }
      }
    }
    """
    
    variables = {"network": "eth", "trader": address}
    print(f"\n  [DEBUG] DEX/NFT Query (v2 API) for address: {address}")
    
    try:
        data, elapsed_time = client.execute_query(query, variables, endpoint=BITQUERY_ENDPOINT_V2)
    except Exception as e:
        print(f"  [DEBUG] Error executing DEX/NFT query: {str(e)}")
        return 0, 0, set(), 0.0
    
    # Debug: Print raw response
    import json
    print(f"  [DEBUG] DEX/NFT Raw API Response:")
    print(f"  {json.dumps(data, indent=2)}")
    print(f"  [DEBUG] DEX/NFT Query took: {elapsed_time:.2f}s")
    
    dex_count_fungible = 0
    dex_count_nonfungible = 0
    dex_protocols = set()
    
    try:
        trades = data.get("EVM", {}).get("DEXTradeByTokens", [{}])[0]
        dex_count_fungible_str = trades.get("dex_count_fungible", "0")
        dex_count_nonfungible_str = trades.get("dex_count_nonfungible", "0")
        
        # Convert strings to integers
        try:
            dex_count_fungible = int(dex_count_fungible_str) if dex_count_fungible_str else 0
        except (ValueError, TypeError):
            dex_count_fungible = 0
            
        try:
            dex_count_nonfungible = int(dex_count_nonfungible_str) if dex_count_nonfungible_str else 0
        except (ValueError, TypeError):
            dex_count_nonfungible = 0
        
        # Use counts to add generic protocol identifiers for P3
        # Each distinct DEX protocol counts as 1 protocol in P3
        if dex_count_fungible > 0:
            for i in range(dex_count_fungible):
                dex_protocols.add(f"dex_erc20_{i+1}")
        if dex_count_nonfungible > 0:
            for i in range(dex_count_nonfungible):
                dex_protocols.add(f"dex_nft_{i+1}")
        
        print(f"  [DEBUG] DEX Count (Fungible): {dex_count_fungible}")
        print(f"  [DEBUG] NFT Count (Non-Fungible): {dex_count_nonfungible}")
        print(f"  [DEBUG] DEX Protocols: {list(dex_protocols)}")
        
        if dex_count_fungible > 0:
            print(f"  [DEBUG] ✓ DEX Swaps detected!")
        else:
            print(f"  [DEBUG] ✗ No DEX swaps found")
            
        if dex_count_nonfungible > 0:
            print(f"  [DEBUG] ✓ NFT Trading detected!")
        else:
            print(f"  [DEBUG] ✗ No NFT trading found")
    except (KeyError, IndexError, TypeError) as e:
        print(f"  [DEBUG] Error parsing DEX/NFT data: {e}")
    
    return dex_count_fungible, dex_count_nonfungible, dex_protocols, elapsed_time


def get_governance_activity(client: BitqueryClient, address: str) -> Tuple[bool, float]:
    """Check for governance activity using v2 API"""
    query = """
    query MyQuery($address: String) {
      EVM(network: eth, dataset: combined) {
        Calls(
          where: {Block: {Time: {since_relative: {years_ago: 3}}}, Call: {Signature: {Name: {includesCaseInsensitive: "vote"}}}, Transaction:{From:{is:$address}}, TransactionStatus: {Success: true}}
        ) {
          count
        }
      }
    }
    """
    
    variables = {"address": address}
    print(f"\n  [DEBUG] Governance Query (v2 API) for address: {address}")
    
    try:
        data, elapsed_time = client.execute_query(query, variables, endpoint=BITQUERY_ENDPOINT_V2)
    except Exception as e:
        print(f"  [DEBUG] Error executing Governance query: {str(e)}")
        return False, 0.0
    
    # Debug: Print raw response
    import json
    print(f"  [DEBUG] Governance Raw API Response:")
    print(f"  {json.dumps(data, indent=2)}")
    print(f"  [DEBUG] Governance Query took: {elapsed_time:.2f}s")
    
    try:
        count = data.get("EVM", {}).get("Calls", [{}])[0].get("count", 0)
        has_governance = int(count) > 0 if count else False
        print(f"  [DEBUG] Governance calls count: {count}")
        if has_governance:
            print(f"  [DEBUG] ✓ Governance activity detected!")
        else:
            print(f"  [DEBUG] ✗ No governance activity found")
        return has_governance, elapsed_time
    except (KeyError, IndexError, TypeError) as e:
        print(f"  [DEBUG] Error parsing governance data: {e}")
        return False, elapsed_time


def get_p4_assets(client: BitqueryClient, address: str) -> Tuple[int, float]:
    """Get unique assets count for P4 (ERC-20 > $10 + NFTs) using v2 API"""
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
    
    print(f"\n  [DEBUG] P4 Assets Query (v2 API) for address: {address}")
    
    unique_assets = set()
    nft_count = 0
    total_time = 0.0
    
    # Get ERC-20 tokens
    try:
        erc20_data, erc20_time = client.execute_query(erc20_query, {"address": address}, endpoint=BITQUERY_ENDPOINT_V2)
        total_time += erc20_time
        print(f"  [DEBUG] ERC-20 Query took: {erc20_time:.2f}s")
        balances = erc20_data.get("EVM", {}).get("BalanceUpdates", [])
        for balance in balances:
            # Only count if Balance_usd exists (meaning >= $10)
            balance_usd = balance.get("Balance_usd")
            if balance_usd:
                currency = balance.get("Currency", {})
                contract = currency.get("SmartContract", "")
                if contract:
                    unique_assets.add(contract)
    except Exception as e:
        print(f"  [DEBUG] Error getting ERC-20 tokens: {str(e)}")
        # Return 0 for assets if query fails
        erc20_time = 0.0
        total_time += erc20_time
    
    # Get NFTs - count individual NFTs (sum of balances), not collections
    try:
        nft_data, nft_time = client.execute_query(nft_query, {"address": address}, endpoint=BITQUERY_ENDPOINT_V2)
        total_time += nft_time
        print(f"  [DEBUG] NFT Query took: {nft_time:.2f}s")
        nft_balances = nft_data.get("EVM", {}).get("BalanceUpdates", [])
        for nft_balance in nft_balances:
            balance_str = nft_balance.get("balance", "0")
            try:
                balance_value = int(float(balance_str))
                nft_count += balance_value
            except (ValueError, TypeError):
                pass
    except Exception as e:
        print(f"  [DEBUG] Error getting NFTs: {str(e)}")
        # Continue with nft_count = 0 if query fails
        nft_time = 0.0
        total_time += nft_time
    
    # Total assets = ERC-20 tokens + individual NFT count
    total_assets = len(unique_assets) + nft_count
    print(f"  [DEBUG] P4 Total Query Time: {total_time:.2f}s")
    print(f"  [DEBUG] ERC-20 tokens (>= $10): {len(unique_assets)}, NFTs: {nft_count}, Total: {total_assets}")
    
    return total_assets, total_time


def calculate_defi_score(address: str, api_key: str, verbose: bool = True) -> Dict:
    """Calculate DeFi Strategy Score for an address"""
    # Check if this is the sample wallet and return presaved response
    if address.lower() == SAMPLE_WALLET_ADDRESS.lower():
        if verbose:
            print(f"Using presaved response for sample wallet: {address}")
            print(f"  ✓ P1: {SAMPLE_WALLET_RESPONSE['p1']['tx_count']} transactions → {SAMPLE_WALLET_RESPONSE['p1']['score']:.2f} points")
            print(f"  ✓ P2: {SAMPLE_WALLET_RESPONSE['p2']['unique_types']} types → {SAMPLE_WALLET_RESPONSE['p2']['score']:.2f} points")
            print(f"  ✓ P3: {SAMPLE_WALLET_RESPONSE['p3']['unique_protocols']} protocols → {SAMPLE_WALLET_RESPONSE['p3']['score']:.2f} points")
            print(f"  ✓ P4: {SAMPLE_WALLET_RESPONSE['p4']['unique_assets']} assets → {SAMPLE_WALLET_RESPONSE['p4']['score']:.2f} points")
        return SAMPLE_WALLET_RESPONSE.copy()
    
    client = BitqueryClient(api_key)
    time_3yr_ago = get_time_3_years_ago()
    
    if verbose:
        print(f"Calculating DeFi Score for {address}...")
        print(f"Time filter: 3 years ago ({time_3yr_ago})")
    
    overall_start = time.time()
    
    # Run queries in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all queries
        futures = {
            "p1": executor.submit(get_p1_transaction_count, client, address, time_3yr_ago),
            "p2_p3": executor.submit(get_p2_p3_data, client, address, time_3yr_ago),
            "dex_nft": executor.submit(get_dex_and_nft_activity, client, address),
            "p4": executor.submit(get_p4_assets, client, address),
        }
        
        # Create reverse mapping from future to name
        future_to_name = {future: name for name, future in futures.items()}
        
        # Collect results as they complete
        results = {}
        for future in as_completed(futures.values()):
            name = future_to_name[future]
            try:
                result = future.result()
                results[name] = result
            except Exception as e:
                if verbose:
                    error_msg = str(e)
                    print(f"  ✗ Error in {name} query: {error_msg}")
                # Set default values based on query type
                if name == "p1":
                    results[name] = (0, 0.0)  # (tx_count, time)
                elif name == "p2_p3":
                    results[name] = (set(), set(), 0.0)  # (activity_types, protocols, time)
                elif name == "dex_nft":
                    results[name] = (0, 0, set(), 0.0)  # (dex_count, nft_count, protocols, time)
                elif name == "p4":
                    results[name] = (0, 0.0)  # (asset_count, time)
                else:
                    results[name] = None
    
    # Process P1 results
    if verbose:
        print("\n  → Processing results...")
    
    try:
        if results.get("p1") is not None:
            tx_count, p1_time = results["p1"]
        p1_score = calculate_p1_score(tx_count)
        if verbose:
                print(f"  ✓ P1 calculated: {tx_count} transactions → {p1_score:.2f} points (took {p1_time:.2f}s)")
        else:
            tx_count = 0
            p1_score = 0.0
            p1_time = 0.0
    except Exception as e:
        if verbose:
            print(f"  ✗ Error processing P1: {str(e)}")
        tx_count = 0
        p1_score = 0.0
        p1_time = 0.0
    
    # Process P2/P3 results
    dex_nft_time = 0.0
    p2_p3_time = 0.0
    
    try:
        if results.get("p2_p3") is not None:
            activity_types, interacted_protocols, p2_p3_time = results["p2_p3"]
        else:
            activity_types = set()
            interacted_protocols = set()
        
        # Add DEX/NFT results
        if results.get("dex_nft") is not None:
            try:
                dex_count_fungible, dex_count_nonfungible, dex_protocols, dex_nft_time = results["dex_nft"]
                
                # Add DEX protocols to interacted_protocols for P3
                if dex_protocols:
                    interacted_protocols.update(dex_protocols)
                    if verbose:
                        print(f"  [DEBUG] Added {len(dex_protocols)} DEX protocols to P3")
                
                # Add activity types based on counts
                if dex_count_fungible > 0:
                    activity_types.add("ERC-20 Trading")
                if dex_count_nonfungible > 0:
                    activity_types.add("NFT Trading")
        
            except (ValueError, TypeError) as e:
                if verbose:
                    print(f"  ⚠ Error unpacking DEX/NFT results: {str(e)}")
                dex_nft_time = 0.0
        
        unique_types = len(activity_types)
        unique_protocols = len(interacted_protocols)
        
        p2_score = calculate_p2_score(unique_types)
        p3_score = calculate_p3_score(unique_protocols)
        
        if verbose:
            print(f"  ✓ P2 calculated: {unique_types} types → {p2_score:.2f} points")
            print(f"    Activity types: {list(activity_types)}")
            print(f"  ✓ P3 calculated: {unique_protocols} protocols → {p3_score:.2f} points")
            print(f"  ✓ P2/P3 queries took: {p2_p3_time:.2f}s + DEX/NFT: {dex_nft_time:.2f}s")
    except Exception as e:
        if verbose:
            print(f"  ✗ Error processing P2/P3: {str(e)}")
            import traceback
            print(f"  Traceback: {traceback.format_exc()}")
        unique_types = 0
        unique_protocols = 0
        p2_score = 0.0
        p3_score = 0.0
    
    # Process P4 results
    try:
        if results.get("p4") is not None:
            unique_assets, p4_time = results["p4"]
        p4_score = calculate_p4_score(unique_assets)
        if verbose:
                print(f"  ✓ P4 calculated: {unique_assets} assets → {p4_score:.2f} points (took {p4_time:.2f}s)")
        else:
            unique_assets = 0
            p4_score = 0.0
            p4_time = 0.0
    except Exception as e:
        if verbose:
            print(f"  ✗ Error processing P4: {str(e)}")
        unique_assets = 0
        p4_score = 0.0
        p4_time = 0.0
    
    # Calculate final score
    avg_pillar_score = (p1_score + p2_score + p3_score + p4_score) / 4.0
    final_score = 25 + (avg_pillar_score * 0.75)
    final_score_rounded = round(final_score)
    
    total_time = time.time() - overall_start
    
    if verbose:
        print(f"\n  {'='*60}")
        print(f"  Query Timing Summary:")
        print(f"  {'='*60}")
        print(f"  P1 (Transaction Count):     {p1_time:.2f}s")
        print(f"  P2/P3 (Protocols):          {p2_p3_time:.2f}s")
        print(f"  DEX/NFT:                    {dex_nft_time:.2f}s")
        print(f"  P4 (Assets):                {p4_time:.2f}s")
        print(f"  {'='*60}")
        print(f"  Total Time:                  {total_time:.2f}s")
        print(f"  {'='*60}\n")
    
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

