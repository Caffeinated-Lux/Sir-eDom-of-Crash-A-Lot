import time
from datetime import datetime, timedelta, timezone
from curl_cffi import requests

def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == "help":
        msg = (
            "**🛡️ Sir eDom of Crash-a-Lot — Command Menu**\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 **Country Intelligence**\n"
            "• `!country <ID>` — *Generates a deep-scan report.* \n"
            "  > Includes: Active citizens, Total/Avg Strength, and Total Weekly Damage (Last 7 Days).\n"
            "  > *Example: `!country 64` for Slovenia.*\n\n"
            "⚔️ **RW Strategic Radar**\n"
            "• `!rws` — *Scans the globe for occupied nations.*\n"
            "  > 🟢 **Free**: Resistance War can be opened now.\n"
            "  > ⏳ **Timer**: Shows exactly when the 48h cooldown ends.\n"
            "  > ⚔️ **Ongoing**: A war is currently active in that nation.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "*“I may crash-a-lot, but I scan-a-lot more!”*"
        )
        return msg

    # --- COUNTRY COMMAND (Auto-Day Detection) ---
    if p_message.startswith("country"):

        parts = p_message.split()
        cid = parts[1] if len(parts) > 1 and parts[1].isdigit() else "17"

        def get_game_day():
            # Game Day 1: April 26, 2017
            start_date = datetime(2017, 4, 26)
            # We use UTC to match server time resets
            now = datetime.utcnow()
            delta = now - start_date
            # Adding 1 because Day 0 is technically Day 1 in eDom logic
            return delta.days + 1

        country_names = {
            "1": "Afghanistan", "2": "Albania", "3": "Algeria", "4": "Argentina", "5": "Armenia",
            "6": "Australia", "7": "Austria", "8": "Azerbaijan", "9": "Belarus", "10": "Belgium",
            "11": "Bolivia", "12": "Bosnia and Herzegovina", "13": "Brazil", "14": "Bulgaria", "15": "Canada",
            "16": "Chile", "17": "China", "18": "Colombia", "19": "Croatia", "20": "Cuba",
            "21": "Cyprus", "22": "Czech Republic", "23": "Denmark", "24": "Ecuador", "25": "Egypt",
            "26": "Estonia", "27": "Finland", "28": "France", "29": "Georgia", "30": "Germany",
            "31": "Greece", "32": "Hungary", "33": "India", "34": "Indonesia", "35": "Iran",
            "36": "Ireland", "37": "Israel", "38": "Italy", "39": "Japan", "40": "Latvia",
            "41": "Lithuania", "42": "Luxembourg", "43": "Malaysia", "44": "Mexico", "45": "Montenegro",
            "46": "Netherlands", "47": "New Zealand", "48": "North Korea", "49": "Norway", "50": "Pakistan",
            "51": "Paraguay", "52": "Peru", "53": "Poland", "54": "Portugal", "55": "Republic of China (Taiwan)",
            "56": "North Macedonia", "57": "Republic of Moldova", "58": "Romania", "59": "Russia", "60": "Saudi Arabia",
            "61": "Serbia", "62": "Singapore", "63": "Slovakia", "64": "Slovenia", "65": "South Africa",
            "66": "South Korea", "67": "Spain", "68": "Sweden", "69": "Switzerland", "70": "Thailand",
            "71": "Tunisia", "72": "Turkey", "73": "Ukraine", "74": "United Arab Emirates", "75": "United Kingdom",
            "76": "United States of America", "77": "Uruguay", "78": "Venezuela", "79": "Greenland", "80": "Palestine",
            "81": "Jordan", "82": "Lebanon", "83": "Syria", "84": "Iraq"
        }

        def analyze_country_full(country_id):
            session = requests.Session()

            # Determine Current Game Day
            current_day = get_game_day()
            # We check players active today or yesterday
            active_days = [current_day, current_day - 1]

            url_citizens = f"https://www.edominations.com/en/api/citizenship/{country_id}"
            try:
                resp = session.get(url_citizens, impersonate="chrome120", timeout=20)
                if resp.status_code != 200: return None
                data = resp.json()

                # Filtering using the dynamic days
                active_players = [
                    p for p in data.values()
                    if isinstance(p, dict) and p.get('LastSeen') in active_days and p.get('Banned') == "No"
                ]

                count = len(active_players)
                if count == 0: return 0, 0, 0, 0, current_day

                total_str = sum(float(p.get('Strength', 0)) for p in active_players)
                avg_str = total_str / count

                total_weekly_dmg = 0
                for p in active_players:
                    p_id = p.get('ID')
                    if not p_id: continue
                    try:
                        p_resp = session.get(f"https://edominations.com/en/api/citizen/{p_id}", impersonate="chrome120",
                                             timeout=5)
                        if p_resp.status_code == 200:
                            p_data = p_resp.json()[0]
                            total_weekly_dmg += float(p_data.get('Last7DaysDamage', 0))
                        time.sleep(0.02)
                    except:
                        continue

                return count, total_str, avg_str, total_weekly_dmg, current_day
            except Exception as e:
                print(f"Error: {e}")
                return None

        # Execute
        data_pack = analyze_country_full(cid)

        if data_pack:
            count, total_str, avg_str, weekly_dmg, game_day = data_pack
            c_name = country_names.get(cid, f"Unknown ID {cid}")

            msg = (f"**📊 Intelligence Report: {c_name}**\n"
                   f"📅 **In-Game Day:** `{game_day}`\n"
                   f"━━━━━━━━━━━━━━━━━━\n"
                   f"👤 **Active Citizens:** `{count}`\n"
                   f"⚔️ **Total Strength:** `{total_str:,.2f}`\n"
                   f"📈 **Average Strength:** `{avg_str:,.2f}`\n"
                   f"━━━━━━━━━━━━━━━━━━\n"
                   f"💥 **Total Weekly Damage:**\n`{weekly_dmg:,.0f}`\n"
                   f"━━━━━━━━━━━━━━━━━━\n"
                   f"⚖️ **Avg DMG per Citizen:** `{(weekly_dmg / count) if count > 0 else 0:,.0f}`\n"
                   f"━━━━━━━━━━━━━━━━━━\n"
                   f"*Scan based on Days {game_day} & {game_day - 1}*")
        else:
            msg = f"❌ Error retrieving data for ID: `{cid}`."

        return msg

    if p_message == "rws":

        # --- SETUP (Game Chronological Order) ---
        drzave = ["Afghanistan", "Albania", "Algeria", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
                  "Belarus", "Belgium", "Bolivia", "Bosnia and Herzegovina", "Brazil", "Bulgaria", "Canada", "Chile",
                  "China", "Colombia", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Ecuador", "Egypt",
                  "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "India", "Indonesia",
                  "Iran", "Ireland", "Israel", "Italy", "Japan", "Latvia", "Lithuania", "Luxembourg", "Malaysia",
                  "Mexico", "Montenegro", "Netherlands", "New Zealand", "North Korea", "Norway", "Pakistan", "Paraguay",
                  "Peru", "Poland", "Portugal", "Republic of China (Taiwan)", "North Macedonia", "Republic of Moldova",
                  "Romania", "Russia", "Saudi Arabia", "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa",
                  "South Korea", "Spain", "Sweden", "Switzerland", "Thailand", "Tunisia", "Turkey", "Ukraine",
                  "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Venezuela",
                  "Greenland", "Palestine", "Jordan", "Lebanon", "Syria", "Iraq"]

        session = requests.Session()
        now_la = datetime.now(timezone(timedelta(hours=-7)))

        try:
            # 1. FETCH DATA
            map_resp = session.get("https://edominations.com/en/api/map", impersonate="chrome120").json()
            live_battles = session.get("https://edominations.com/en/api/battles/1", impersonate="chrome120").json()
            history = session.get("https://edominations.com/en/api/battle-history", impersonate="chrome120").json()

            # 2. MAP TRACKING (Original Owner vs Current Owner)
            real_cores, held_cores = {i: 0 for i in range(1, 85)}, {i: 0 for i in range(1, 85)}
            for rid, d in map_resp.items():
                if rid == "0": continue
                o_id, c_id = int(d.get("owner_original_id", 0)), int(d.get("owner_current_id", 0))
                if o_id in real_cores:
                    real_cores[o_id] += 1
                    if o_id == c_id: held_cores[o_id] += 1

            # 3. INITIALIZE STATUS
            country_status = {i: "✅ **Free**" for i in range(1, 85)}
            norm_map = {name.lower().strip(): i + 1 for i, name in enumerate(drzave)}

            # 4. LIVE BATTLE SCAN (Ongoing)
            # Any battle in the live list is Ongoing.
            for b_id, b in live_battles.items():
                if "Resistance" in str(b.get("Type", "")):
                    att_name = str(b.get("Attacker", "")).lower().strip()
                    if att_name in norm_map:
                        country_status[norm_map[att_name]] = "⚔️ **Ongoing**"

            # 5. HISTORY SCAN (Cooldowns)
            latest_history = {}
            for h in reversed(history):
                if h.get("type") == 1:
                    aid = h.get("attacker")
                    if aid and aid not in latest_history: latest_history[aid] = h

            for cid in range(1, 85):
                if country_status[cid] == "⚔️ **Ongoing**": continue

                event = latest_history.get(cid)
                if event:
                    # IMPORTANT: If the Resistance won the last battle, no cooldown applies!
                    # In battle-history, 'win' is usually 1 (Attacker won) or 2 (Defender won)
                    # If they won (1), we keep it as "✅ Free"
                    if str(event.get("win")) == "1":
                        continue

                    # If they lost (2), check 48h cooldown from the end date
                    date_str = event.get("date")
                    if date_str and date_str != "0000-00-00 00:00:00":
                        b_end = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(
                            tzinfo=timezone(timedelta(hours=-7)))
                        expiry = b_end + timedelta(hours=48)

                        if expiry > now_la:
                            diff = expiry - now_la
                            h, m = divmod(int(diff.total_seconds()) // 60, 60)
                            country_status[cid] = f"⏳ `{h}h {m}m`"

            # 6. OUTPUT (Chronological order, occupied only)
            final_list = []
            for i, name in enumerate(drzave):
                cid = i + 1
                if held_cores[cid] < real_cores[cid]:
                    final_list.append(f"• {name}: {country_status[cid]}")

            return "**🌍 RW Strategy Intelligence**\n" + "\n".join(final_list)

        except Exception as e:
            return f"❌ System Error: {str(e)}"