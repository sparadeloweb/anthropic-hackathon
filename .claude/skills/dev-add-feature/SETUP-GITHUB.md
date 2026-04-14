# GitHub CLI Setup

## Install gh

**macOS:**
```bash
brew install gh
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install gh
```

**Windows:**
```bash
winget install GitHub.cli
```

## Authenticate

```bash
gh auth login
```

Follow the prompts to authenticate via browser.

## Verify

```bash
gh auth status
```

Should show: Logged in to github.com as YOUR_USERNAME.

## Set default repository

```bash
gh repo set-default OWNER/REPO
```
