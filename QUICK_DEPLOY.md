# 📁 Deploy Bestanden Overzicht

## 🚀 Quick Deploy (3 stappen)

### 1. Upload naar GitHub
```bash
cd ~/Documents/tankbeurt-app
./deploy.sh
```

### 2. Deploy op Render
1. Ga naar [render.com](https://render.com)
2. New Web Service → Connect GitHub
3. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn tankbeurt_app:app`
4. Deploy! 🚀

### 3. Klaar!
Je app is live met database!

---

## 📋 Alle Deploy Bestanden

| Bestand | Doel |
|---------|------|
| `DEPLOY.md` | Complete deploy handleiding |
| `deploy.sh` | Automatische Git upload script |
| `requirements.txt` | Python dependencies |
| `Procfile` | Render start command |
| `runtime.txt` | Python versie |
| `.gitignore` | Excludes database en cache |

---

## 🎯 Deploy Opties

| Platform | Kosten | Database |
|----------|--------|----------|
| **Render** | ✅ Gratis | ✅ Automatisch |
| **Railway** | ✅ Gratis trial | ✅ Automatisch |
| **Vercel** | ✅ Gratis | ✅ PostgreSQL |
| **GitHub Pages** | ✅ Gratis | ❌ Geen (localStorage) |

---

## 🚨 Belangrijk

- ❌ Upload **niet** `tankbeurten.db` naar git (zit in .gitignore)
- ✅ Render maakt automatisch database aan
- ✅ Gebruik `deploy.sh` voor makkelijke git push

---

**Start nu:** `cd ~/Documents/tankbeurt-app && ./deploy.sh`
