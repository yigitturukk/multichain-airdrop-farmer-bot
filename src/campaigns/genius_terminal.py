import random

class GeniusTerminalCampaign:
    def __init__(self, wallet, config, chains):
        self.name = "genius_terminal"
        self.wallet = wallet
        self.config = config
        self.chains = chains
        self.activity_chance = 0.9  # Very high because campaign ends soon
        self.last_task = datetime.now()
        
        self.tasks = [
            {'name': 'Swap on GT Terminal', 'type': 'swap', 'chain': 'ethereum', 'points': 40},
            {'name': 'Trade with GT', 'type': 'swap', 'chain': 'arbitrum', 'points': 40},
            {'name': 'Hold GT tokens', 'type': 'hold', 'chain': 'ethereum', 'points': 20},
            {'name': 'Refer a friend', 'type': 'referral', 'chain': None, 'points': 100},
            {'name': 'Complete trades volume', 'type': 'volume', 'chain': 'ethereum', 'points': 200},
        ]
    
    def get_next_task(self):
        if random.random() < 0.95:  # 95% chance
            return random.choice(self.tasks)
        return None
    
    def record_task(self, task, tx_hash):
        self.last_task = datetime.now()