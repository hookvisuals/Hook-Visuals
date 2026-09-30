#!/bin/bash
# Startet einen lokalen Server für den Akquise-Briefgenerator und öffnet ihn im Browser.
# Nötig, damit Google-Login (OAuth) funktioniert — das geht nicht per Doppelklick (file://).

cd "$(dirname "$0")" || exit 1

PORT=8000

# WICHTIG: einen evtl. noch laufenden alten Server auf diesem Port beenden.
# Sonst würde der neue (cache-freie) Server den Port nicht bekommen und der
# Browser landet weiter auf der ALTEN, gecachten Version.
lsof -ti "tcp:${PORT}" 2>/dev/null | xargs kill -9 2>/dev/null
sleep 1

# Eindeutige Adresse mit Zeitstempel → der Browser MUSS die frische Datei laden
# (eine neue URL kann er nicht aus dem Cache nehmen).
URL="http://localhost:${PORT}/akquise-generator.html?v=$(date +%s)"

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

# Server OHNE Caching starten (sonst zeigt der Browser beim Reload alte Versionen).
python3 briefgenerator_serve.py "$PORT"
