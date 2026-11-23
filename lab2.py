import csv, os, sys
from datetime import datetime
from pathlib import Path
import boto3, requests
from botocore.exceptions import ClientError, BotoCoreError

BUCKET = os.getenv("AWS_LAB_BUCKET", "lab2-nabok-2026")
REGION = os.getenv("AWS_REGION", "eu-north-1")
URL = "https://bank.gov.ua/NBU_Exchange/exchange_site"

def get_rates(currency):
    r = requests.get(URL, params={"start":"20220101","end":"20221231","valcode":currency,"sort":"exchangedate","order":"asc","json":""}, timeout=60)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data,list) or not data:
        raise ValueError("Немає даних для " + currency)
    return [{"date":datetime.strptime(x["exchangedate"],"%d.%m.%Y").strftime("%Y-%m-%d"),
             "currency":currency,"rate":float(x.get("rate_per_unit",x["rate"]))} for x in data]

def main():
    try:
        rows = sorted(get_rates("USD")+get_rates("EUR"),key=lambda r:(r["date"],r["currency"]))
        path=Path("rates_2022.csv")
        with path.open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=["date","currency","rate"])
            writer.writeheader()
            writer.writerows(rows)
        print("Створено CSV. Записів:", len(rows))
        if len(rows)!=730: print("Увага: очікувалось 730 записів")
        boto3.client("s3",region_name=REGION).upload_file(str(path),BUCKET,path.name)
        print(f"Завантажено s3://{BUCKET}/{path.name}")
    except (requests.RequestException,ValueError,KeyError,ClientError,BotoCoreError) as e:
        print("Помилка:",e,file=sys.stderr)
        sys.exit(1)

if __name__=="__main__": main()
