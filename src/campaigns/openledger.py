import random
from datetime import datetime, timedelta

class OpenLedgerCampaign:
    def __init__(self, wallet, config, chains):
        self.name = "openledger"
        self.wallet = wallet
        self.config = config
        self.chains = chains
        self.activity_chance = 0.7
        self.last_task = datetime.now()
        
        # Tasks specific to OpenLedger campaign
        self.tasks = [
            {'name': 'Swap ETH/USDC on Uniswap', 'type': 'swap', 'chain': 'ethereum', 'points': 50},
            {'name': 'Add liquidity to ETH/OPEN pool', 'type': 'liquidity', 'chain': 'ethereum', 'points': 100},
            {'name': 'Stake OPEN tokens', 'type': 'stake', 'chain': 'ethereum', 'points': 75},
            {'name': 'Bridge to Arbitrum', 'type': 'bridge', 'chain': 'arbitrum', 'points': 60},
            {'name': 'Swap on Arbitrum', 'type': 'swap', 'chain': 'arbitrum', 'points': 40},
            {'name': 'Mint OpenLedger Genesis NFT', 'type': 'nft_mint', 'chain': 'solana', 'points': 150},
        ]
    
    def get_next_task(self):
        """Return next task to execute"""
        if random.random() < 0.8:  # 80% chance to have a task
            return random.choice(self.tasks)
        return None
    
    def record_task(self, task, tx_hash):
        """Record completed task"""
        self.last_task = datetime.now()
        # In real implementation, would update points via API