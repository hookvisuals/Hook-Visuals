#!/bin/bash
# Startet einen lokalen Server für den Akquise-Briefgenerator und öffnet ihn im Browser.
# Nötig, damit Google-Login (OAuth) funktioniert — das geht nicht per Doppelklick (file://).

cd "$(dirname "$0")" || exit 1

PORT=8000
URL="http://localhost:${PORT}/akquise-generator.html"

# Browser kurz nach dem Start öffnen
( sleep 1; open "$URL" ) &

echo "───────────────────────────────────────────────"
echo "  Hook Visuals · Akquise-Briefgenerator"
echo "───────────────────────────────────────────────"
echo "  Läuft unter:  $URL"
echo ""
echo "  Dieses Fenster offen lassen, solange du arbeitest."
echo "  Zum Beenden: dieses Fenster schließen oder Strg+C."
echo "───────────────────────────────────────────────"

# Falls Port belegt ist, den nächsten freien probieren
python3 -m http.server "$PORT" 2>/dev/null || python3 -m http.server 8001
