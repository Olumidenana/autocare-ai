# AutoCare AI: WhatsApp Master Automotive Co-Pilot 🚗🇳🇬

A white-label, multilingual automotive diagnostic and customer retention platform designed for Nigerian car dealerships (such as **AutoContentment**) and vehicle owners.

Operates via WhatsApp with **zero hardware installation**. Speaks fluent **English, Nigerian Pidgin, Yoruba, and Igbo**.

---

## 🌟 Key Capabilities

1. **Multilingual Master Diagnostic Brain**:
   * Uses differential diagnostic decision trees (the "Dr. House of Cars" approach) to ask the single clarifying question that isolates faults.
   * Maps local vernacular (*brainbox, shocker, exhaust cat, gbagba-gbagba, gbọ̀n, mkpọtụ*) to formal engineering failure modes.
   * Armed with **Mechanic Scam Alerts** to protect owners from unnecessary part swaps.

2. **Proactive Acoustic Health Check (10-Second Engine Purr Test)**:
   * Analyzes audio recordings of idling and revving engines.
   * Detects valve lifter ticks, belt tensioner slippage, and bottom-end knock.
   * Emits an **Acoustic Health Index (0–100%)** as a proactive health certificate.

3. **Zero-Hardware Vehicle Tracking**:
   * **Dashboard Computer Vision**: Snaps dashboard odometer photos to verify mileage and flag instrument warning lights.
   * **Fuel & Oil Economy Tracker**: Calculates real-world km/L and flags sudden fuel consumption spikes (detecting dirty air filters or failing O2 sensors).
   * **Commute-Based Mileage Modeling**: Estimates daily driving based on local transit profiles (Lagos, Abuja, PH, Interstate).

4. **Hyper-Localized Nigerian Road Matrix**:
   * Incorporates real-world failure patterns for Lekki floods, Abuja high-speed thermal load, Benin-Ore craters, and northern Harmattan dust.

---

## 🚀 Quickstart & Testing

The project is built using Python 3.12 and managed with `uv`.

### 1. Run the Interactive Simulator (No API Keys Required)
Test all features in terminal immediately:
```powershell
cd C:\Users\giant\.gemini\antigravity\scratch\autocare-ai
uv run python simulator.py
```

### 2. Run the Verification Suite
```powershell
uv run python test_core.py
```

### 3. Start the Live FastAPI Webhook Server
```powershell
uv run uvicorn src.main:app --reload --port 8000
```
API Documentation will be available at: `http://localhost:8000/docs`

---

## 📱 Connecting to Your WhatsApp Business Account (Meta Cloud API)

When you are ready to link your actual WhatsApp Business number:

1. **Go to Meta for Developers**:
   * Visit [developers.facebook.com](https://developers.facebook.com/) and log in.
   * Click **Create App** $\rightarrow$ Select **Other** $\rightarrow$ Select **Business**.
   * Under Add Products, click **Set Up** on **WhatsApp**.

2. **Copy Credentials to `.env`**:
   * Copy `.env.example` to `.env`:
     ```powershell
     cp .env.example .env
     ```
   * Fill in `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, and `WHATSAPP_VERIFY_TOKEN`.

3. **Expose Local Server to the Web**:
   * In a new terminal, run `ngrok http 8000` or Cloudflare tunnel.
   * Copy the public forwarding HTTPS URL (e.g. `https://xyz.ngrok-free.app`).

4. **Configure Webhook on Meta**:
   * In Meta WhatsApp dashboard $\rightarrow$ **Configuration** $\rightarrow$ **Webhook**:
     * Callback URL: `https://xyz.ngrok-free.app/webhook`
     * Verify Token: `autocare_secret_token_123` (matching your `.env`)
   * Click **Verify and Save**.
   * Under Webhook fields, click **Manage** and subscribe to **messages**.

---

## 📂 Project Directory Structure

```
autocare-ai/
├── src/
│   ├── knowledge/
│   │   ├── nigerian_lexicon.py      # Pidgin, Yoruba, Igbo automotive terms & acoustics
│   │   ├── road_terrain_matrix.py   # City-specific road hazards (Lekki, Abuja, Ore, etc.)
│   │   └── known_failure_modes.py   # OEM Technical Service Bulletins (2GR, M274, K24)
│   ├── engine/
│   │   ├── diagnostic_brain.py      # Differential diagnosis state machine
│   │   ├── acoustic_analyzer.py     # 10-second engine sound & health evaluator
│   │   ├── vision_scanner.py        # Dashboard odometer OCR & warning scanner
│   │   └── proactive_tracker.py     # Fuel economy & consumption anomaly detector
│   ├── database/
│   │   ├── models.py                # Customer, Vehicle, FuelLog, ServiceLog schemas
│   │   └── db.py                    # Async SQLite database engine
│   ├── webhook/
│   │   ├── whatsapp_client.py       # Meta Graph API sender & media downloader
│   │   └── routes.py                # FastAPI webhook GET/POST routes
│   ├── config.py                    # Environment & configuration settings
│   └── main.py                      # FastAPI application entrypoint
├── simulator.py                     # Rich terminal interactive testing tool
├── test_core.py                     # Core module unit & smoke tests
├── pyproject.toml                   # uv project definition
└── README.md                        # Documentation
```
