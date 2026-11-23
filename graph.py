import io, os, sys
import boto3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from botocore.exceptions import ClientError, BotoCoreError

BUCKET=os.getenv("AWS_LAB_BUCKET","lab2-nabok-2026")
REGION=os.getenv("AWS_REGION","eu-north-1")

def main():
    try:
        s3=boto3.client("s3",region_name=REGION)
        data=s3.get_object(Bucket=BUCKET,Key="rates_2022.csv")["Body"].read()
        df=pd.read_csv(io.BytesIO(data),parse_dates=["date"])
        for c in ["USD","EUR"]:
            values=df.loc[df.currency==c].sort_values("date")
            if values.empty: raise ValueError("Немає даних "+c)
            plt.plot(values.date,values.rate,label=c)
        plt.title("USD and EUR exchange rates in Ukraine (2022)")
        plt.xlabel("Date")
        plt.ylabel("UAH per unit")
        plt.grid(alpha=.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig("graph_2022.png",dpi=150)
        plt.close()
        s3.upload_file("graph_2022.png",BUCKET,"graph_2022.png")
        print(f"Графік завантажено: s3://{BUCKET}/graph_2022.png")
    except (ClientError,BotoCoreError,ValueError,OSError) as e:
        print("Помилка:",e,file=sys.stderr)
        sys.exit(1)

if __name__=="__main__": main()
