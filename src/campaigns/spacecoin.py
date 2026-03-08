import random

class SpacecoinCampaign:
    def __init__(self, wallet, config, chains):
        self.name = "spacecoin"
        self.wallet = wallet
        self.config = config
        self.chains = chains
        self.activity_chance = 0.6
        self.last_task = datetime.now()
        
        self.tasks = [
            {'name': 'Swap SOL/SPACE', 'type': 'swap', 'chain': 'solana', 'points': 70},
            {'name': 'Provide SPACE liquidity', 'type': 'liquidity', 'chain': 'solana', 'points': 130},
            {'name': 'Stake SPACE', 'type': 'stake', 'chain': 'solana', 'points': 90},
            {'name': 'Mint Space Explorer NFT', 'type': 'nft_mint', 'chain': 'solana', 'points': 110},
            {'name': 'Vote on SpaceDAO', 'type': 'vote', 'chain': 'solana', 'points': 30},
        ]
    
    def get_next_task(self):
        if random.random() < 0.7:
            return random.choice(self.tasks)
        return None
    
    def record_task(self, task, tx_hash):
        self.last_task = datetime.now()