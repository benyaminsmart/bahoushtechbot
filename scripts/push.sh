#!/data/data/com.termux/files/usr/bin/bash
# Bahoush Tech Bot — Auto Commit & Push
# Usage: ./scripts/push.sh "commit message"

set -e
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

MSG="${1:-}"
if [ -z "$MSG" ]; then
  echo -e "${RED}❌ Error: commit message required${NC}"
  echo -e "${YELLOW}Usage: ./scripts/push.sh \"feat: your message\"${NC}"
  exit 1
fi

cd "$(dirname "$0")/.."
echo -e "${YELLOW}📦 Staging changes...${NC}"
git add -A

if git diff --cached --quiet; then
  echo -e "${YELLOW}ℹ️  No changes to commit.${NC}"
  exit 0
fi

echo -e "${YELLOW}📝 Committing: $MSG${NC}"
git commit -m "$MSG"

echo -e "${YELLOW}🚀 Pushing to origin/main...${NC}"
git push origin main

echo -e "${GREEN}✅ Done!${NC}"
git log --oneline -1
