import requests
import pandas as pd
from config import API_KEY, TOKEN

# Dirección del contrato de LINK en Ethereum (mainnet)
LINK_CONTRACT = "0x514910771af9ca656af840dff83e8264ecf986ca"

def get_transactions(start_block=0, end_block=99999999, max_txs=2000):
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": LINK_CONTRACT,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "desc",
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "1":
        df = pd.DataFrame(data["result"])
        df["timeStamp"] = pd.to_datetime(df["timeStamp"], unit='s')
        df["value"] = df["value"].astype(float) / 10**18  # convertir de wei
        return df.head(max_txs)
    else:
        return pd.DataFrame()

def calculate_whale_risk(df):
    # Whale = cualquier tx > 100.000 LINK
    whale_txs = df[df["value"] > 100_000]
    if len(whale_txs) > 0:
        return "CRÍTICO", len(whale_txs)
    elif df["value"].max() > 50_000:
        return "INCIERTO", 1
    else:
        return "VITAL", 0

def group_volume_by_day(df):
    return df.groupby(df["timeStamp"].dt.date)["value"].sum()
