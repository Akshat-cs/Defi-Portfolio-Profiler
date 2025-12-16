**DeFi Strategy Score \= 25 (Base Score) \+ (Average Pillar Score × 0.75)**

**Where** Average Pillar Score \= (P1 \+ P2 \+ P3 \+ P4) / 4, P1: Transaction Count, P2: Transaction Types, P3: Protocols Used, P4: Assets Held

Defi score calculation for this address \- **0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862**

**P1 Query** \- [https://ide.bitquery.io/transaction-count-for-an-address-in-last-1-years](https://ide.bitquery.io/transaction-count-for-an-address-in-last-1-years)   
query MyQuery($address: String) {  
  EVM(network: eth, dataset: combined) {  
    Transactions(  
      where: {Transaction: {From: {is: $address}}, Block: {Time: {since\_relative: {years\_ago: 1}}}, TransactionStatus: {Success: true}}  
    ){  
      count  
    }  
  }  
}

{  
  "address": "0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862"  
}

Tx Count \- 86  
P1 Score \- 84.44 points

**P2 & P3 Query** \- [https://ide.bitquery.io/Calls-to-Different-types-of-protocols\_2](https://ide.bitquery.io/Calls-to-Different-types-of-protocols_2)   
query MyQuery($protocols: \[String\!\], $address: String) {  
  EVM(network: eth, dataset: combined) {  
    Calls(  
      where: {Block:{Time:{since\_relative:{years\_ago:1}}} Call: {To: {in: $protocols }}, TransactionStatus: {Success: true}, Transaction: {From: {is:$address}}}  
    ) {  
      Call {  
        To  
      }  
      count(distinct:Transaction\_Hash)  
    }  
  }  
}

{  
  "address": "0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862",  
  "protocols": \[  
"0xd01607c3C5eCABa394D8be377a08590149325722",  
"0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",

"0xa0d9C1E9E48Ca30c8d8C3B5D69FF5dc1f6DFfC24",  
"0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",

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

"0xc3d688B66703497DAA19211EEdff47f25384cdc3",  
"0xA17581A9E3356d9A858b789D68B4d866e593aE94",  
"0x3Afdc9BCA9213A35503b077a6072F3D0d5AB0840",  
"0x3D0bb1ccaB520A66e607822fC55BC921738fAFE3",  
"0x5D409e56D886231aDAf00c8775665AD0f9897b56",

"0xC13e21B648A5Ee794902342038FF3aDAB66BE987",

"0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb",

"0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",  
"0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",

"0xDD3f50F8A6CafbE9b31a427582963f465E745AF8",

"0xC36442b4a4522E871399CD717aBDD847Ab11FE88",

"0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5",

"0x8731d54E9D02c286767d56ac03e8037C07e01e98",  
"0x150f94B44927F078737562f0fcF3C95c01Cc2376",

"0xdA816459F1AB5631232FE5e97a05BBBb94970c95",  
"0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9",  
"0x7Da96a3891Add058AdA2E826306D812C638D87A7",  
"0xa258C4606Ca8206D8aA700cE2143D7db854D168c",

"0xF403C135812408BFbE8713b5A23a04b3D48AAE31"  
\]

}

1 type \- Lending✅; and interacted with 1 protocols  
P2 score \- 0 points  
P3 score \- 0 points

1. **DEXSwaps, NFT Trading** \- separate query \- [https://ide.bitquery.io/dexswaps-and-nft-trading-activity\_1](https://ide.bitquery.io/dexswaps-and-nft-trading-activity_1)   
   query MyQuery($address: String) {  
     EVM(network: eth, dataset: combined) {  
       DEXTrades(  
         where: {Block: {Time: {since\_relative: {years\_ago: 1}}}, Transaction: {From: {is: $address}}, TransactionStatus: {Success: true}}  
       ) {  
         dex\_count\_fungible:count(distinct:Trade\_Dex\_ProtocolName if:{Trade:{Buy:{Currency:{Fungible:true}}}})  
         dex\_count\_nonfungible:count(distinct:Trade\_Dex\_ProtocolName if:{Trade:{Buy:{Currency:{Fungible:false}}}})  
       }  
     }  
   }  
     
   {  
     "address": "0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862"  
   }  
     
     
2. **Lending/ Borrowing** 

**Aave v3 Addresses**\- "0xd01607c3C5eCABa394D8be377a08590149325722","0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"  
**Aave v2 addresses** \- "0xa0d9C1E9E48Ca30c8d8C3B5D69FF5dc1f6DFfC24","0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"  
**Compound \- v2** \- "0xe65cdB6479BaC1e22340E4E755fAE7E509EcD06c",  
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
"0x6d903f6003cca6255D85CcA4D3B5E5146dC33925"

**Compound v3** \- “0xc3d688B66703497DAA19211EEdff47f25384cdc3”,”0xA17581A9E3356d9A858b789D68B4d866e593aE94”,”0x3Afdc9BCA9213A35503b077a6072F3D0d5AB0840”,”0x3D0bb1ccaB520A66e607822fC55BC921738fAFE3”,”0x5D409e56D886231aDAf00c8775665AD0f9897b56”

**Sparklend** \- “0xC13e21B648A5Ee794902342038FF3aDAB66BE987”  
**Morpho** \- “0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb”

3. **Staking**   
   **Ethereum 2.0** \- “0x00000000219ab540356cBB839Cbe05303d7705Fa”  
   **Lido** \- “0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84”, “0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0”  
   **RocketPool** \- “0xDD3f50F8A6CafbE9b31a427582963f465E745AF8”  
   **Swell** \- “0xFAe103DC9cf190eD75350761e95403b7b8aFa6c0”  
   **Coinbase cbETH** \- “0xBe9895146f7AF43049ca1c1AE358B0541Ea49704”  
   **Frax Ether** \- “0xac3E018457B222d93114458476f3E3416Abbe38F”

   

4. **Liquidity Provision**   
   **Uniswap v3** \- “0xC36442b4a4522E871399CD717aBDD847Ab11FE88”  
     
5. **Governance**  \- separate query \- [https://ide.bitquery.io/governance-check-for-an-address\_1](https://ide.bitquery.io/governance-check-for-an-address_1)   
   query MyQuery($address: String) {  
     EVM(network: eth, dataset: combined) {  
       Calls(  
         where: {Block: {Time: {since\_relative: {years\_ago: 1}}}, Call: {Signature: {Name: {includesCaseInsensitive: "vote"}}}, Transaction:{From:{is:$address}} ,TransactionStatus: {Success: true}}  
       ) {  
         count  
       }  
     }  
   }  
     
   {  
     "address": "0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862"  
   }  
     
     
6. **Bridging**  
   **Across** \- “0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5”  
   **Stargate** \- “0x8731d54E9D02c286767d56ac03e8037C07e01e98”, “0x150f94B44927F078737562f0fcF3C95c01Cc2376”  
     
7. **Yield Farming**   
   **Yearn Finance** \- “0xdA816459F1AB5631232FE5e97a05BBBb94970c95”, “0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9”, “0x7Da96a3891Add058AdA2E826306D812C638D87A7”, “0xa258C4606Ca8206D8aA700cE2143D7db854D168c”  
   **Convex Finance** \- 0xF403C135812408BFbE8713b5A23a04b3D48AAE31  
     
     
   

**P4 Query** \- NFT Balances \- [https://ide.bitquery.io/NFT-balances-of-an-address\_1](https://ide.bitquery.io/NFT-balances-of-an-address_1)   
query MyQuery {  
  EVM(dataset: combined, network: eth) {  
    BalanceUpdates(  
      where: {BalanceUpdate: {Address: {is: "0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862"}}, Currency: {Fungible: false}}  
      orderBy: {descendingByField: "balance"}  
    ) {  
      Currency {  
        Name  
        Symbol  
        SmartContract  
      }  
      balance: sum(of: BalanceUpdate\_Amount)  
    }  
  }  
}

Token ERC-20 Token Balances \- [https://ide.bitquery.io/Token-balances-of-an-address-above-10\_1](https://ide.bitquery.io/Token-balances-of-an-address-above-10_1)   
{  
  EVM(network: eth, dataset: combined) {  
    BalanceUpdates(  
      orderBy: {descendingByField: "Balance\_usd"}  
      where: {BalanceUpdate: {Address: {is: "0x6979B914f3A1d8C0fec2C1FD602f0e674cdf9862"}}, Currency: {Fungible: true}}  
    ) {  
      BalanceUpdate {  
        Address  
      }  
      Currency{  
        Name  
        Symbol  
        SmartContract  
      }  
      Balance:sum(of:BalanceUpdate\_Amount selectWhere:{gt:"0"})  
      Balance\_usd:sum(of:BalanceUpdate\_AmountInUSD selectWhere:{ge:"10"})  
    }  
  }  
}

7 Tokens gt $10 balance  
29 NFTs  
P4 score \- 100

Defi Strategy score \- 25 \+ avg pillar score \* 0.75  
Avg pillar score \= (84.44 \+ 0 \+ 0 \+ 100\) / 4 \= 46.11

Final Defi Score \= 25 \+ 46.11 \* 0.75 \= **59.5825**