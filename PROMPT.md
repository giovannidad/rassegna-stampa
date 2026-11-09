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
- Internazionali, attualità e politica: Reuters, Associated Press, BBC News, Politico Europe, The Guardian, Le Monde.
- Internazionali, tech, AI e cybersecurity: The Record (Recorded Future News), BleepingComputer, SecurityWeek, Krebs on Security, Dark Reading, Ars Technica, MIT Technology Review; istituzionali: CISA, ENISA, CERT-EU.
- Internazionali, PA digitale e privacy: EDPB, Commissione europea (Shaping Europe's Digital Future), Euractiv, noyb.
- Tennis e rugby: ATP Tour, WTA, World Rugby, Six Nations.
Usa solo fonti ad accesso libero: se un articolo è dietro paywall e ne vedi solo titolo o sommario, non usarlo e cerca la stessa notizia su una fonte aperta. Le notizie da fonti straniere vanno raccontate in italiano.
Fonti e pagine da evitare perché in passato hanno dato problemi (non raggiungibili, contenuto non datato o non verificabile):
- Pagine indice o tag di BleepingComputer (bleepingcomputer.com/tag/...): mostrano elenchi senza date né URL e a volte notizie vecchie. Usa solo articoli singoli, trovati con una ricerca, con data verificabile.
- Newsletter e aggregatori di notizie (this.weekinsecurity.com, learnrudi.com, fourweekmba.com, riepiloghi "AI Daily", substack e blog di riassunti): non caricano o riportano cifre non verificate. Servono al massimo come spunto: ogni notizia va confermata su una fonte primaria o su una testata della lista sopra.
- Federprivacy (federprivacy.org): le pagine dei singoli articoli spesso non si caricano. Per le notizie del Garante preferisci garanteprivacy.it o testate come Agenda Digitale e Cybersecurity360.
- redhotcyber.com: controlla sempre la data dell'articolo, a volte pubblica contenuti di anni fa che compaiono nelle ricerche sull'attualità.
- Home page di Agenda Digitale e pagine di elenco dell'EDPB: richiedono un'autorizzazione che nelle esecuzioni automatiche resta senza risposta. Cerca invece l'articolo specifico con WebSearch e aprilo da lì.
In generale: apri solo URL comparsi nei risultati di ricerca, controlla la data di ogni articolo, e se una pagina non si carica passa a un'altra fonte invece di insistere.

Verifica le notizie importanti su almeno due fonti. Non inventare nulla: se una sezione non ha notizie rilevanti, dillo in una frase e passa oltre.

## 3. Sezioni, in quest'ordine
1. **Attualità e politica** (Italia ed esteri): 5-6 notizie, almeno una internazionale o europea.
2. **Tech, AI e cybersecurity** (4-5 notizie): vulnerabilità critiche, attacchi rilevanti (soprattutto verso PA ed enti locali italiani), novità AI importanti.
3. **PA digitale e privacy** (3-4 notizie, almeno una di livello europeo): PNRR e scadenze, avvisi PA digitale, circolari AgID e ACN, provvedimenti e sanzioni del Garante, novità GDPR e AI Act che riguardano i Comuni.
4. **Sport**: SOLO tennis e rugby, e solo se c'è una notizia davvero rilevante (finali, risultati di italiani nei grandi tornei, Sei Nazioni, test match). Nessun altro sport: niente calcio, Formula 1, MotoGP, basket, ecc. Se non c'è nulla, ometti la sezione.

## 4. Stile del copione (sarà letto da una voce sintetica)
- Lunghezza: tra 1300 e 1450 parole (circa 10 minuti). Indicativamente: attualità 40%, tech e cybersecurity 30%, PA digitale e privacy 25%, sport il resto. Approfondisci con contesto e conseguenze invece di aggiungere notizie minori.
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
