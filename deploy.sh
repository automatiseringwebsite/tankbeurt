#!/bin/bash

# Deploy Script voor Tankbeurt App naar GitHub en Render

echo "🚗 Tankbeurt App Deploy Script"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Git initialiseren..."
    git init
    git branch -M main
else
    echo "✅ Git already initialized"
fi

# Add files
echo "📝 Bestanden toevoegen..."
git add .
git commit -m "Deploy tankbeurt app"

# Check if remote is set
if ! git remote get-url origin &>/dev/null; then
    echo "❌ Geen GitHub remote gevonden!"
    echo ""
    echo "Maak eerst een GitHub repository aan:"
    echo "1. Ga naar https://github.com/new"
    echo "2. Maak een nieuwe repository"
    echo "3. Kopieer de repository URL"
    echo ""
    read -p "Voer je GitHub repository URL in: " repo_url

    git remote add origin "$repo_url"
fi

# Push to GitHub
echo "📤 Pushen naar GitHub..."
git push -u origin main

echo ""
echo "✅ Deploy klaar!"
echo ""
echo "📋 Volgende stappen:"
echo "1. Ga naar https://render.com"
echo "2. Nieuwe Web Service aanmaken"
echo "3. Connect je GitHub repository"
echo "4. Settings:"
echo "   - Build: pip install -r requirements.txt"
echo "   - Start: gunicorn tankbeurt_app:app"
echo "5. Deploy en wachten op build..."
echo "6. Klaar! 🎉"
