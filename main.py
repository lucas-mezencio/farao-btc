import os
import requests
import json
from dotenv import load_dotenv

TARGET_ADDRESS = "1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj"
PAYMENTS_DIR = "./cache/payments"
TRANSACTIONS_DIR = "./cache/transactions"


def load_payments_data() -> list:
    payments_data = []
    try:
        payments = os.listdir(PAYMENTS_DIR)
        for payment_file in payments:
            with open(
                os.path.join(PAYMENTS_DIR, payment_file), "r", encoding="utf-8"
            ) as f:
                data = json.load(f)
                payments_data.extend(data.get("data", []))

        return payments_data

    except Exception as e:
        print(f"Error loading payments data: {e}")
        return []


def download_transactions(key, txs: set) -> None:
    for tx_hash in txs:
        download_transaction_data(key, tx_hash)


def download_transaction_data(key, hash: str) -> None:
    url = f"https://api.blockchair.com/bitcoin/dashboards/transaction/{hash}"
    resp = requests.get(url, params={"key": key})
    print(f"transaction {hash} - status {resp.status_code}")
    data = resp.json()
    try:
        with open(
            os.path.join(TRANSACTIONS_DIR, f"tx-{hash}.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing transaction data for {hash}: {e}")
        exit(1)


def download_payments_data(key: str, target: str) -> None:
    url = "https://api.blockchair.com/bitcoin/outputs"
    for offset in range(0, 400, 100):
        params = {
            "key": key,
            "s": "time(desc)",
            "q": f"recipient({target})",
            "limit": 100,
            "offset": offset,
        }
        resp = requests.get(url, params=params)
        print(f"page {int(offset / 100)} - status: {resp.status_code}")
        data = resp.json()
        try:
            with open(
                os.path.join(PAYMENTS_DIR, f"payments-pg{int(offset / 100)}.json"),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error writing payments data: {e}")
            exit(1)


def should_download_data(path: str) -> bool:
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            exit(1)
    content = os.listdir(path)
    if len(content) == 0:
        return True
    return False


def main():
    if not load_dotenv():
        print(".env file not found")
        return

    api_key = os.getenv("BLOCKCHAIR_APIKEY")
    if api_key is None:
        print("BLOCKCHAIR_APIKEY not found in .env file")
        return
    if should_download_data(PAYMENTS_DIR):
        print("donwloading payments data...", api_key)
        download_payments_data(api_key, TARGET_ADDRESS)

    payments_to_target = load_payments_data()
    transaction_hashes = set(
        [payment["transaction_hash"] for payment in payments_to_target]
    )
    print(f"Payments to {TARGET_ADDRESS}:{len(transaction_hashes)}")

    if should_download_data(TRANSACTIONS_DIR):
        print("donwloading transactions data...")
        download_transactions(api_key, transaction_hashes)


if __name__ == "__main__":
    main()
