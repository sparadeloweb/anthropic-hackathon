# Google Places API Setup

## 1. Create a Google Cloud project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing (required for Places API)

## 2. Enable the Places API (New)

1. Go to **APIs & Services > Library**
2. Search for **Places API (New)**
3. Click **Enable**

## 3. Create an API key

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > API Key**
3. Restrict the key to **Places API (New)** only (recommended)

## 4. Set the environment variable

```bash
export GOOGLE_PLACES_API_KEY="your-api-key-here"
```

To persist across sessions, add it to your shell profile (`~/.bashrc`, `~/.zshrc`) or use Claude Code's environment settings.

## Billing notes

The script uses **Text Search (New)** at the **Enterprise + Atmosphere** SKU to fetch all available fields (photos, reviews, hours, etc.):

| SKU | What it adds | Cost per request |
|---|---|---|
| Text Search Pro | displayName, address, websiteUri, photos, types | $0.032 |
| Text Search Enterprise | + phone, rating, hours, businessStatus | $0.040 |
| Text Search Enterprise + Atmosphere | + reviews, editorialSummary, parking, payment, etc. | $0.064 |

The script uses the Enterprise + Atmosphere tier ($0.064/request).

Estimated costs:
- 3x3 grid (~15 requests with pagination): ~$0.96
- 5x5 grid (~50 requests with pagination): ~$3.20
- 7x7 grid (~100 requests with pagination): ~$6.40
