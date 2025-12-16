The DeFi Score is designed to measure a wallet's strategic engagement and sophistication within the DeFi ecosystem, independent of the total capital deployed. The score ranges from 25 to 100\.

The final score is calculated using the following formula:

**DeFi Strategy Score \= 25 (Base Score) \+ (Average Pillar Score × 0.75)**

Here’s how each component is derived:

#### **1\. Base Score**

Every wallet automatically starts with a Base Score of 25\. This ensures that even new users have a starting point on the scorecard.

#### **2\. The Four Pillars**

The core of the score comes from four distinct "Pillars," each designed to measure a different aspect of a user's on-chain activity over the last 1 years. Each pillar is scored on a scale of 0 to 100 points.

* P1: Transaction Count: Measures the wallet's overall activity level.  
  * Scoring: Points are awarded based on the total number of transactions.  
    * 0-10 TXs \= 0 points  
    * 100+ TXs \= 100 points (The scoring is linear between these two thresholds).  
* P2: Transaction Types: Measures the diversity of a wallet's interactions with DeFi.  
  * Activity Types (8 total): DEX Swaps, Lending/Borrowing, Staking, Liquidity Provision, NFT Trading, Governance, Bridging, Yield Farming.  
  * Scoring: Points are awarded based on the number of unique activity types performed.  
    * 1 unique type \= 0 points  
    * 5+ unique types \= 100 points (The scoring is linear between these two thresholds).  
* P3: Protocols Used: Measures how widely a user has interacted with the DeFi ecosystem.  
  * Detection: This is based on interactions with a curated whitelist of smart contracts from major protocols (e.g., Uniswap, Aave, Lido, Compound).  
  * Scoring: Points are awarded based on the number of unique protocols used.  
    * 1 unique protocol \= 0 points  
    * 8+ unique protocols \= 100 points (The scoring is linear between these two thresholds).  
* P4: Assets Held: Measures the diversity of a wallet's portfolio.  
  * Criteria: An asset is counted if it's an ERC-20 token with a current balance exceeding $10 USD. Holding any NFT adds 1 to the asset count.  
  * Scoring: Points are awarded based on the number of unique assets held.  
    * 1 unique asset \= 0 points  
    * 15+ unique assets \= 100 points (The scoring is linear between these two thresholds).

#### **3\. Final Score Calculation**

1. Calculate Individual Pillar Scores: Determine the 0-100 point score for each of the four pillars (P1, P2, P3, P4).  
2. Calculate the Average Pillar Score: Sum the scores of the four pillars and divide by 4\.  
   1. Average Pillar Score \= (P1 \+ P2 \+ P3 \+ P4) / 4  
3. Apply the Weighting Factor: Multiply the Average Pillar Score by a 75% weighting factor (0.75). This scales the contribution from the pillars to a maximum of 75 points.  
4. Add the Base Score: Add the weighted pillar average to the base score of 25 to get the final DeFi Strategy Score.

Example:

Using the wallet 0xABC... from our previous discussion:

* Pillar Scores: P1=80, P2=75, P3=70, P4=70  
* Average Pillar Score: (80 \+ 75 \+ 70 \+ 70\) / 4 \= 73.75  
* Final Score: 25 \+ (73.75 \* 0.75) \= 25 \+ 55.3125 \= 80.3125  
* The final score is rounded to the nearest whole number, resulting in 80\.

