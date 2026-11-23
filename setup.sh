#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $# -ne 1 ]]; then
  echo "Використання: bash setup.sh https://github.com/USERNAME/aws-lab2-nabok.git"
  exit 2
fi
for cmd in git python3; do
  command -v "$cmd" >/dev/null || { echo "Немає $cmd"; exit 1; }
done
dir="aws-lab2-nabok-clone"
if [[ -e "$dir" ]]; then
  echo "Каталог $dir уже існує"; exit 1
fi
echo "[1/4] Клонуємо репозиторій"
git clone -- "$1" "$dir"
cd "$dir"
[[ -f requirements.txt ]] || { echo "Не знайдено requirements.txt"; exit 1; }
echo "[2/4] Створюємо venv"
python3 -m venv .venv
echo "[3/4] Встановлюємо залежності"
.venv/bin/python -m pip install -r requirements.txt
echo "[4/4] Перевіряємо бібліотеки"
.venv/bin/python -c 'import boto3, requests, pandas, matplotlib; print("Залежності встановлені успішно")'
echo "Готово: $(pwd)"
