# Rassegna Stampa

Rassegna stampa audio di 10 minuti, dal lunedì al venerdì, pubblicata come podcast privato.

## Come funziona
1. Alle 6:30 un'attività pianificata Claude scrive il copione in `episodes/AAAA-MM-GG.md` (istruzioni in `PROMPT.md`).
2. GitHub Actions genera l'MP3 (Edge TTS, con Piper di riserva), aggiorna `docs/feed.xml` e pubblica su GitHub Pages.
3. L'app podcast scarica il nuovo episodio dal feed.

## Configurazione iniziale
1. Carica tutti questi file nel repository (ramo `main`).
2. **Settings → Pages → Source: GitHub Actions**.
3. **Settings → Actions → General → Workflow permissions: Read and write**.
4. Avvia una prima volta il workflow da **Actions → Pubblica episodio → Run workflow**.
5. Nell'app podcast aggiungi il feed tramite URL: `https://giovannidad.github.io/rassegna-stampa/feed.xml`
   (Apple Podcasts: Libreria → menu ⋯ → Segui uno show tramite URL).

## Personalizzare
- Voce, velocità e numero di episodi conservati: `config.yml`.
- Fonti, sezioni e stile: `PROMPT.md` (poi va aggiornata anche l'attività pianificata).
