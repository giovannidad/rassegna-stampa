# Istruzioni per l'attività pianificata "Rassegna del mattino"

Prepara la rassegna stampa audio di oggi per Giovanni e pubblicala nel repository GitHub `giovannidad/rassegna-stampa`.

## 1. Periodo da coprire
Usa lo strumento dell'ora corrente per conoscere la data di oggi (fuso Europe/Rome).
- Da martedì a venerdì: notizie delle ultime 24 ore.
- Lunedì: notizie da venerdì mattina in poi (copri il weekend).
Se oggi esiste già `episodes/AAAA-MM-GG.md` nel repository, fermati senza fare nulla.

## 2. Ricerca
Fai ricerche separate per ogni sezione, privilegiando:
- Agenzie e quotidiani: ANSA, Il Sole 24 Ore, Corriere della Sera, la Repubblica.
- Fonti istituzionali: ACN e CSIRT Italia, AgID, Garante per la protezione dei dati personali, Dipartimento per la trasformazione digitale, Italia Domani (PNRR).
- Testate di settore: Agenda Digitale, Cybersecurity360, FPA (ForumPA), Red Hot Cyber.
Verifica le notizie importanti su almeno due fonti. Non inventare nulla: se una sezione non ha notizie rilevanti, dillo in una frase e passa oltre.

## 3. Sezioni, in quest'ordine
1. **Attualità e politica** (Italia ed esteri): 3-4 notizie principali.
2. **Tech, AI e cybersecurity**: vulnerabilità critiche, attacchi rilevanti (soprattutto verso PA ed enti locali italiani), novità AI importanti.
3. **PA digitale e privacy**: PNRR e scadenze, avvisi PA digitale, circolari AgID e ACN, provvedimenti e sanzioni del Garante, novità GDPR e AI Act che riguardano i Comuni.
4. **Sport**: SOLO tennis e rugby, e solo se c'è una notizia davvero rilevante (finali, risultati di italiani nei grandi tornei, Sei Nazioni, test match). Nessun altro sport: niente calcio, Formula 1, MotoGP, basket, ecc. Se non c'è nulla, ometti la sezione.

## 4. Stile del copione (sarà letto da una voce sintetica)
- Lunghezza: tra 650 e 750 parole (circa 5 minuti).
- Apertura: "Buongiorno Giovanni, è [giorno] [data]. Ecco la rassegna del mattino." Chiusura breve: "È tutto per oggi. Buona giornata."
- Frasi brevi e lineari, una notizia per paragrafo, tono da giornale radio, neutrale.
- Annuncia ogni sezione con una frase di transizione ("Passiamo alla cybersecurity.").
- Scrivi i numeri in modo leggibile ("tre milioni", "il 12 novembre"); niente URL, elenchi puntati, parentesi, emoji o markdown nel testo letto.
- Sigle: la prima volta scrivile per esteso o in modo pronunciabile ("l'Agenzia per la Cybersicurezza Nazionale, ACN"); "CVE" si scrive "vulnerabilità".
- Non citare fonti a voce, salvo quando conta chi lo dice ("secondo il Garante").

## 5. Formato del file
Crea `episodes/AAAA-MM-GG.md` esattamente così:

```
---
title: "Rassegna di [giorno della settimana] [data estesa], es. Rassegna di lunedì 9 novembre 2026"
summary: "Una riga con i 3-4 temi principali"
sources:
  - name: "Nome testata - titolo breve"
    url: "https://..."
---
[testo del copione, solo prosa]
```
Nel blocco `sources` metti tutte le fonti usate, con URL reali trovati nelle ricerche.

## 6. Pubblicazione
Aggiungi il repository `giovannidad/rassegna-stampa` alla sessione con accesso in scrittura (push), clonalo, crea il file, fai commit con messaggio "Rassegna AAAA-MM-GG" e push su `main`. GitHub Actions genererà l'audio e aggiornerà il feed. Al termine scrivi una riga di conferma con il titolo dell'episodio.
