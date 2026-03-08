#!/usr/bin/env python3
"""
Multi-Chain Airdrop Farmer Bot
Automates airdrop farming across multiple chains and campaigns
"""

import os
import sys
import time
import yaml
import random
import threading
import logging
from datetime import datetime, timedelta
from colorama import init, Fore, Style
import requests
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

# Import chain modules
from chains.ethereum import EthereumChain
from chains.solana import SolanaChain
from chains.arbitrum import ArbitrumChain

# Import campaign modules
from campaigns.openledger import OpenLedgerCampaign
from campaigns.lombard import LombardCampaign
from campaigns.spacecoin import SpacecoinCampaign
from campaigns.genius_terminal import GeniusTerminalCampaign

# Import utils
from utils.wallet import WalletManager
from utils.logger import setup_logger

init(autoreset=True)
logger = setup_logger()

class AirdropFarmer:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.wallet = WalletManager(self.config['wallet'])
        self.chains = {}
        self.campaigns = []
        self.stats = {
            'total_transactions': 0,
            'total_gas_spent': 0,
            'campaigns_progress': {},
            'start_time': datetime.now()
        }
        self.running = True
        
        self.init_chains()
        self.init_campaigns()
        
        # Start background threads
        self.threads = []
        self.start_workers()
        
    def init_chains(self):
        """Initialize blockchain connections"""
        if self.config['chains']['ethereum']['enabled']:
            self.chains['ethereum'] = EthereumChain(self.config['chains']['ethereum'])
            logger.info(f"{Fore.GREEN}✓ Ethereum chain initialized")
        
        if self.config['chains']['solana']['enabled']:
            self.chains['solana'] = SolanaChain(self.config['chains']['solana'])
            logger.info(f"{Fore.GREEN}✓ Solana chain initialized")
        
        if self.config['chains']['arbitrum']['enabled']:
            self.chains['arbitrum'] = ArbitrumChain(self.config['chains']['arbitrum'])
            logger.info(f"{Fore.GREEN}✓ Arbitrum chain initialized")
    
    def init_campaigns(self):
        """Initialize airdrop campaigns"""
        campaign_map = {
            'openledger': OpenLedgerCampaign,
            'lombard': LombardCampaign,
            'spacecoin': SpacecoinCampaign,
            'genius_terminal': GeniusTerminalCampaign
        }
        
        for name, config in self.config['campaigns'].items():
            if config.get('enabled') and name in campaign_map:
                campaign = campaign_map[name](self.wallet, config, self.chains)
                self.campaigns.append(campaign)
                self.stats['campaigns_progress'][name] = {
                    'points': 0,
                    'tasks_completed': 0,
                    'last_update': datetime.now()
                }
                logger.info(f"{Fore.GREEN}✓ Campaign '{name}' initialized")
    
    def start_workers(self):
        """Start background workers for each campaign"""
        for campaign in self.campaigns:
            thread = threading.Thread(target=self.campaign_worker, args=(campaign,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            logger.info(f"{Fore.CYAN}Started worker for {campaign.name}")
    
    def campaign_worker(self, campaign):
        """Worker thread for a specific campaign"""
        while self.running:
            try:
                # Check if we should work on this campaign
                if random.random() < campaign.activity_chance:
                    task = campaign.get_next_task()
                    if task:
                        logger.info(f"{Fore.YELLOW}[{campaign.name}] Executing task: {task['name']}")
                        
                        # Execute the task on appropriate chain
                        chain = self.chains.get(task['chain'])
                        if chain:
                            success, tx_hash, gas = chain.execute_task(task, self.wallet)
                            if success:
                                campaign.record_task(task, tx_hash)
                                self.stats['total_transactions'] += 1
                                self.stats['total_gas_spent'] += gas
                                self.stats['campaigns_progress'][campaign.name]['tasks_completed'] += 1
                                
                                # Simulate earning points
                                points_earned = random.randint(10, 100)
                                self.stats['campaigns_progress'][campaign.name]['points'] += points_earned
                                
                                logger.info(f"{Fore.GREEN}  ✓ Task completed! TX: {tx_hash[:10]}... | +{points_earned} points")
                            else:
                                logger.warning(f"{Fore.RED}  ✗ Task failed")
                
                # Random delay between tasks
                delay = random.randint(
                    self.config['settings']['tx_delay_min'],
                    self.config['settings']['tx_delay_max']
                )
                time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Worker error: {e}")
                time.sleep(60)
    
    def generate_html_dashboard(self):
        """Generate HTML dashboard"""
        uptime = datetime.now() - self.stats['start_time']
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Airdrop Farmer Dashboard</title>
            <meta http-equiv="refresh" content="5">
            <style>
                body {{ font-family: Arial; margin: 20px; background: #1a1a1a; color: #fff; }}
                .stats {{ background: #2d2d2d; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .campaign {{ background: #333; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
                .progress {{ background: #444; height: 20px; border-radius: 10px; }}
                .progress-bar {{ background: #4CAF50; height: 20px; border-radius: 10px; width: 0%; }}
                h1 {{ color: #4CAF50; }}
                h2 {{ color: #888; }}
            </style>
        </head>
        <body>
            <h1>🚀 Multi-Chain Airdrop Farmer</h1>
            <div class="stats">
                <h2>System Stats</h2>
                <p><strong>Uptime:</strong> {str(uptime).split('.')[0]}</p>
                <p><strong>Total Transactions:</strong> {self.stats['total_transactions']}</p>
                <p><strong>Total Gas Spent:</strong> ${self.stats['total_gas_spent']:.4f}</p>
                <p><strong>Active Chains:</strong> {', '.join(self.chains.keys())}</p>
            </div>
            
            <h2>Campaign Progress</h2>
        """
        
        for name, progress in self.stats['campaigns_progress'].items():
            html += f"""
            <div class="campaign">
                <h3>{name.upper()}</h3>
                <p><strong>Points:</strong> {progress['points']}</p>
                <p><strong>Tasks Completed:</strong> {progress['tasks_completed']}</p>
                <div class="progress">
                    <div class="progress-bar" style="width: {min(progress['points']/1000*100, 100)}%"></div>
                </div>
            </div>
            """
        
        html += """
            <p><small>Auto-refreshes every 5 seconds • Generated by Airdrop Farmer Bot</small></p>
        </body>
        </html>
        """
        return html
    
    def run_dashboard(self):
        """Run Flask web dashboard"""
        app = Flask(__name__)
        socketio = SocketIO(app)
        
        @app.route('/')
        def dashboard():
            return self.generate_html_dashboard()
        
        @socketio.on('connect')
        def handle_connect():
            emit('connected', {'data': 'Connected to dashboard'})
        
        port = self.config['settings'].get('dashboard_port', 8080)
        socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
    
    def run(self):
        """Main entry point"""
        logger.info(f"{Fore.CYAN}Starting Airdrop Farmer Bot...")
        logger.info(f"{Fore.CYAN}Wallet address: {self.wallet.address}")
        logger.info(f"{Fore.CYAN}Active campaigns: {len(self.campaigns)}")
        logger.info(f"{Fore.CYAN}Dashboard: http://localhost:{self.config['settings']['dashboard_port']}")
        
        # Start dashboard in a separate thread
        dashboard_thread = threading.Thread(target=self.run_dashboard)
        dashboard_thread.daemon = True
        dashboard_thread.start()
        
        try:
            while self.running:
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info(f"{Fore.YELLOW}Shutting down...")
            self.running = False
            sys.exit(0)

if __name__ == "__main__":
    farmer = AirdropFarmer()
    farmer.run()