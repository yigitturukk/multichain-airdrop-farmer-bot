import random
from datetime import datetime

class LombardCampaign:
    def __init__(self, wallet, config, chains):
        self.name = "lombard"
        self.wallet = wallet
        self.config = config
        self.chains = chains
        self.activity_chance = 0.8  # Higher because season ends soon
        self.last_task = datetime.now()
        
        self.tasks = [
            {'name': 'Swap ETH/LOMB on Curve', 'type': 'swap', 'chain': 'ethereum', 'points': 60},
            {'name': 'Provide LOMB liquidity', 'type': 'liquidity', 'chain': 'ethereum', 'points': 120},
            {'name': 'Stake LOMB', 'type': 'stake', 'chain': 'ethereum', 'points': 80},
            {'name': 'Bridge LOMB to Arbitrum', 'type': 'bridge', 'chain': 'arbitrum', 'points': 50},
            {'name': 'Vote on Lombard governance', 'type': 'vote', 'chain': 'ethereum', 'points': 40},
        ]
    
    def get_next_task(self):
        if random.random() < 0.9:  # 90% chance
            return random.choice(self.tasks)
        return None
    
    def record_task(self, task, tx_hash):
        self.last_task = datetime.now()