# GitHub Publishing

This repo can be published once a GitHub remote exists.

## Option A: Existing GitHub Repo

Create an empty repository on GitHub, then run:

```bash
git remote add origin git@github.com:<your-user-or-org>/one-pass-med-review.git
git push -u origin main
```

If you prefer HTTPS:

```bash
git remote add origin https://github.com/<your-user-or-org>/one-pass-med-review.git
git push -u origin main
```

## Option B: GitHub CLI

If `gh` is installed and authenticated:

```bash
gh repo create one-pass-med-review --public --source=. --remote=origin --push
```

## Real-Time Push Workflow

For normal development, use small commits and push after each coherent change:

```bash
git add .
git commit -m "Describe the change"
git push
```

Automated push on every file save is not recommended because it can publish broken or sensitive intermediate files. A safer "near real-time" policy is to push after each passing test checkpoint.
