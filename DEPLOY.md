# 🚗 Tankbeurt App - Deploy Guide

Complete tankbeurt tracking applicatie met Flask backend.

## 📦 Bestanden

| Bestand | Beschrijving |
|---------|-------------|
| `index.html` | Statisch formulier (geen backend) |
| `tankbeurt_app.html` | Volledige app met localStorage |
| `tankbeurt_app.py` | Flask backend API |
| `tankbeurten.db` | SQLite database (niet in git!) |

## 🚀 Deploy op Render (Aanbevolen - Gratis)

### Stap 1: GitHub Repository

1. Maak een nieuwe repository op GitHub
2. Upload alle bestanden behalve `tankbeurten.db`

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/JOUW_GITHUB_USERNAME/tankbeurt-app.git
git push -u origin main
```

### Stap 2: Deploy op Render

1. Ga naar [render.com](https://render.com)
2. Klik op **"New +"** → **"Web Service"**
3. Connect je GitHub repository
4. Vul deze settings in:

| Setting | Waarde |
|---------|--------|
| **Name** | `tankbeurt-app` (of iets anders) |
| **Region** | Frankfurt (of nearest) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn tankbeurt_app:app` |

5. Klik op **"Create Web Service"**

6. ⚠️ **BELANGRIJK:** Na deploy moet je een database maken!

### Stap 3: Database initialiseren

Render maakt geen database automatisch. Voer dit uit in de Render Console:

1. Ga naar je dashboard op render.com
2. Klik op je service
3. Klik op **"Logs"** → **"Shell"** (console)
4. Run dit commando:

```bash
python tankbeurt_database.py
```

Dit maakt een nieuwe `tankbeurten.db` aan in de `/opt/render/project/src` map.

## 🌐 Alternatieve Platforms

### Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Railway
1. Ga naar [railway.app](https://railway.app)
2. Connect GitHub repository
3. Railway detecteert automatisch Python/Flask

### Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

## 📊 Statische Deploy (GitHub Pages)

Als je geen database nodig wilt:

1. Hernoem `tankbeurt_app.html` naar `index.html`
2. Upload naar GitHub
3. Enable GitHub Pages in repository settings
4. Klaar! ✅

**Nadeel:** Data wordt opgeslagen in browser (localStorage), niet gedeeld tussen apparaten.

## 🔧 Lokale Testen

### Met Flask (backend):
```bash
# 1. Installeer dependencies
pip install -r requirements.txt

# 2. Start server
python tankbeurt_app.py

# 3. Open browser op http://localhost:5000
```

### Zonder Flask (statisch):
```bash
# Open gewoon index.html in browser
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux
```

## 📝 Environment Variables (Optioneel)

Voor extra veiligheid kun je environment variables gebruiken:

```python
# In tankbeurt_app.py
import os
DB_PATH = os.getenv('DB_PATH', '/opt/render/project/src/tankbeurten.db')
```

In Render:
- Settings → Environment Variables
- Voeg `DB_PATH` = `/opt/render/project/src/tankbeurten.db` toe

## 🐛 Problemen?

**Deploy faalt?**
- Check de Logs tab in Render
- Zorg dat alle bestanden geüpload zijn
- Check dat `requirements.txt` bestaat

**Database niet gevonden?**
- Open Render Console
- Run `python tankbeurt_database.py`

**404 of 500 errors?**
- Check logs voor specifieke foutmelding
- Zorg dat `tankbeurt_app.py` correct is geconfigureerd

## 💡 Tips

- ✅ Gebruik `tankbeurt_app.html` voor snelle static deploy (GitHub Pages)
- ✅ Gebruik `tankbeurt_app.py` voor database en multi-device sync
- ✅ Exporteer regelmatig je data (CSV export functie in de app)
- ✅ Back-up je database bestand

## 📞 Support

GitHub Issues: [github.com/clawdbot/clawdbot](https://github.com/clawdbot/clawdbot)

---

**Gemaakt met ❤️ door Clawdbot**
