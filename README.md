
# Bot Telegram Gopeed (déploiement Render / Replit)

Ce dépôt permet d'héberger une API qui transforme les liens Telegram en lien direct de téléchargement compatible avec Gopeed.

## Déploiement

### 🔹 Render
1. Crée un Web Service sur [https://render.com](https://render.com)
2. Ajoute une variable d'environnement `BOT_TOKEN` avec ton token Telegram
3. Port utilisé automatiquement (expose le port `PORT`)

### 🔸 Replit
1. Crée un Replit Python
2. Ajoute les fichiers `bot.py`, `requirements.txt`
3. Ajoute un `.env` avec :
   ```env
   BOT_TOKEN=ton_token_telegram
   ```

### 📤 Utilisation avec Gopeed
Dans ton extension `index.js`, appelle :

```js
const response = await fetch("https://TON_URL_RENDER/resolve-telegram", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ url: "https://t.me/.../..." })
});
```

Le script retourne un lien direct vers le fichier Telegram.
