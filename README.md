
---

# 🛡️ Sir eDom of Crash-a-Lot

**An Honorable (but slightly clunky) Scout for the eDominations Universe.**

Sir eDom is a specialized Discord bot designed to traverse the eDominations API. He identifies strategic openings for Resistance Wars (RW) and sniffs out the country stats across the globe to keep you informed.

---

## 📜 The Knight’s Abilities
Sir eDom listens for calls starting with !. Depending on how you summon him, he will respond differently:


* **`!command`**: Sir eDom announces the findings publicly in the **current channel**.

### ⚔️ Available Commands
* **`rws`** – Scans and identifies Resistance Wars that can be "Free" to open countries, lists "Ongoing" wars, and calculates precise countdown timers for those RWs that are on 48h cooldown.
* **`country <ID>`** – Performs a deep-scan of a specific nation to report on its military and economic standing.

  * Activity: Identifies non-banned citizens active within the last 48 hours.

  * Power: Calculates Total and Average Strength across the population.

  * Impact: Aggregates Total Weekly Damage and average damage per citizen.

  * Example: Use !country 64 for a report on Slovenia.


---

## 🛠️ Summoning the Knight (Setup)

### 1. The Secret Scroll (`.env`)
Create a file named `.env` in the root directory. Sir eDom requires your Discord Token to wake up:
```plaintext
DISCORD_TOKEN=your_private_token_here
```

### 2. Prepare the Forge (Requirements)
Ensure your environment is equipped with the necessary Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Entering the Fray (Execution)
To run the bot normally:
```bash
python main.py
```

---


## ⚠️ Disclaimer
Sir eDom of Crash-A-Lot is currently in his **Early Squire** phase. He might be slow to clank his way to the API, and he might trip over his cape (crash). Use at your own risk.

---
