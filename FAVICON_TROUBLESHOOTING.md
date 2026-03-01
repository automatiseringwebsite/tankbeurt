# Favicon Probleemoplossing

## Probleem
De favicon verschijnt mogelijk niet in je browser tabblad. Dit heeft verschillende oorzaken:

## Mogelijke Oorzaken

### 1. Browser Cache
Browsers cachen favicons zeer agressief. Mogelijke oplossingen:

**Force Refresh:**
- Windows: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

**Cache leegmaken:**
- Chrome: Instellingen → Privacy → Browseerdata wissen → Selecteer "Afbeeldingen en bestanden in cache"
- Firefox: Instellingen → Privacy → Browseerdata wissen
- Safari: Ontwikkel → Cache legen (Cmd + Option + E)

### 2. Deploy Status
De favicon is pas beschikbaar als Render de deploy heeft voltooid (2-5 min na push).

### 3. Browser Ondersteuning
Sommige browsers geven de voorkeur aan `.ico` boven `.png`. Onze favicon is `.png`.

## Testen

### Incognito/Privé Modus
Open de site in een incognito of privé venster:
- Chrome: `Ctrl + Shift + N`
- Firefox: `Ctrl + Shift + P`
- Safari: `Cmd + Shift + N`

Dit omzeilt de cache.

### Andere Browser
Test de site in een andere browser om te zien of het specifiek is voor jouw browser.

### Andere Device
Open de site op je mobiele telefoon of tablet. Soms werkt het wel op mobiel maar niet op desktop.

## Favicon Bestand

Het favicon bestand is `favicon.png` (16x16 pixels, PNG formaat).
- Gradient van `#667eea` naar `#764ba2`
- Gecreëerd met Python en base64

## Handmatig Toevoegen

Als je de favicon wilt forceren:

### Voor Gebruikers
1. Open https://tankbeurt-1.onrender.com
2. Klik met rechtermuisknop op de site
3. Selecteer "Maak bookmark" of "Voeg toe aan favorieten"
4. Het icoontje verschijnt dan in je bookmarks

### Voor Developers
Als je toegang hebt tot de server, upload `favicon.png` naar de root van de site.

## Huidige Status

- ✅ `favicon.png` in repository
- ✅ HTML linkt naar `/favicon.png?v=3`
- ⏳ Wachten op Render deploy

## Favicon Check

Je kunt direct het favicon bestand openen:
https://tankbeurt-1.onrender.com/favicon.png

Als dit een 404 error geeft, is de deploy nog niet afgerond.

## Extra Tips

- **Wacht even:** Soms duurt het 10-15 minuten voordat browsers favicons updaten
- **Schoon cache:** Probeer de browser cache volledig te legen
- **Andere browser:** Probeer een andere browser om te testen
- **Privé modus:** Gebruik incognito modus om cache te omzeilen

## Contact

Als het na een uur nog steeds niet werkt, kan er een ander probleem zijn. Controleer de GitHub repository en Render logs.
