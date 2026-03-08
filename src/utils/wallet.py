import base58
from web3 import Web3
from solders.keypair import Keypair

class WalletManager:
    def __init__(self, config):
        self.config = config
        self.address = None
        self.init_wallet()
        
    def init_wallet(self):
        """Initialize wallet from private key"""
        if 'private_key' in self.config and self.config['private_key']:
            # EVM wallet
            w3 = Web3()
            account = w3.eth.account.from_key(self.config['private_key'])
            self.address = account.address
            self.evm_account = account
            
        if 'solana_private_key' in self.config and self.config['solana_private_key']:
            # Solana wallet
            key_bytes = base58.b58decode(self.config['solana_private_key'])
            self.solana_keypair = Keypair.from_bytes(key_bytes)
            self.solana_address = str(self.solana_keypair.pubkey())
            
    def get_evm_account(self):
        return getattr(self, 'evm_account', None)
    
    def get_solana_keypair(self):
        return getattr(self, 'solana_keypair', None)
    
    def sign_message(self, message, chain='ethereum'):
        """Sign a message (demo only)"""
        if chain == 'ethereum' and hasattr(self, 'evm_account'):
            return self.evm_account.sign_message(message)
        return None