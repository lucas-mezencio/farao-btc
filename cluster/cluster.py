TARGET_ADDRESS = "1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj"


def clusterize_addresses(transactions: list) -> list:
    clusters = []
    ignored_addressses = [
        "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s",
        "1HaTSjMb9Tg8yDNk5axvnWqyTUss26XUjV",
    ]
    known_addresses = set()

    for tx in transactions:
        tx_inputs = tx.get("inputs", [])
        tx_outputs = tx.get("outputs", [])
        tx_data = tx.get("transaction", {})

        if tx_data.get("is_coinbase", False):
            print(f"skipping coinbase transaction {tx_data.get('hash')}")
            continue

        # h1
        addresses = set()
        smaller_input_utxo = float("inf")
        for input in tx_inputs:
            address = input.get("recipient")
            value = input.get("value", 0)

            if (
                address
                and address.startswith(("1", "bc1"))
                and address not in ignored_addressses
            ):
                addresses.add(address)
                known_addresses.add(address)
                if value < smaller_input_utxo:
                    smaller_input_utxo = value
        if not addresses:
            continue

        # h2
        new_outputs = []
        for output in tx_outputs:
            address = output.get("recipient")
            value = output.get("value", 0)
            if (
                address
                and address.startswith(("1", "bc1"))
                and address not in ignored_addressses
            ):
                if address != TARGET_ADDRESS and address not in known_addresses:
                    new_outputs.append({"addr": address, "value": value})
        if len(new_outputs) == 1:
            change = new_outputs[0]
            if change["value"] < smaller_input_utxo:
                addresses.add(change["addr"])
                known_addresses.add(change["addr"])

        # merge culsters
        intersection_idxs = []
        for i, cluster in enumerate(clusters):
            if not addresses.isdisjoint(cluster):
                intersection_idxs.append(i)
        if not intersection_idxs:
            clusters.append(addresses)
        else:
            first_idx = intersection_idxs[0]
            clusters[first_idx].update(addresses)
            for i in reversed(intersection_idxs[1:]):
                clusters[first_idx].update(clusters.pop(i))

    return clusters


"""
{
    "transaction": {
        "block_id": 672885,
        "id": 621202225,
        "hash": "0056281655e3942cd69e3ec252e2dbe7605ff264d03bdf626e83eccb51462b0b",
        "date": "2021-03-02",
        "time": "2021-03-02 20:37:32",
        "size": 250,
        "weight": 670,
        "version": 1,
        "lock_time": 0,
        "is_coinbase": false,
        "has_witness": true,
        "input_count": 1,
        "output_count": 2,
        "input_total": 26402027,
        "input_total_usd": 13212.895,
        "output_total": 26382203,
        "output_total_usd": 13202.974,
        "fee": 19824,
        "fee_usd": 9.92092,
        "fee_per_kb": 79296,
        "fee_per_kb_usd": 39.68368,
        "fee_per_kwu": 29588.06,
        "fee_per_kwu_usd": 14.807344,
        "cdd_total": 0,
        "is_rbf": true
    },
    "inputs": [
        {
            "block_id": 672877,
            "transaction_id": 621185422,
            "index": 1,
            "transaction_hash": "37a6c828569fdca402f036e2c945483ae8c4511a876c5debadd16705d1883e8f",
            "date": "2021-03-02",
            "time": "2021-03-02 19:49:35",
            "value": 26402027,
            "value_usd": 13212.895,
            "recipient": "3E4BS7ZXHCEP5wWz9XhA1xYiMaDNXoE5wk",
            "type": "scripthash",
            "script_hex": "a91487a22ed9ba7f9b43e01e7274fb7af6d717f73fe887",
            "is_from_coinbase": false,
            "is_spendable": null,
            "is_spent": true,
            "spending_block_id": 672885,
            "spending_transaction_id": 621202225,
            "spending_index": 0,
            "spending_transaction_hash": "0056281655e3942cd69e3ec252e2dbe7605ff264d03bdf626e83eccb51462b0b",
            "spending_date": "2021-03-02",
            "spending_time": "2021-03-02 20:37:32",
            "spending_value_usd": 13212.895,
            "spending_sequence": 0,
            "spending_signature_hex": "16001435e680d22b562155e375d29255e242db465d9461",
            "spending_witness": "3045022100b6c64f80c7193185a627a851d2cdd30d44a8513ecc94a1e9c8ccc02b78e0ecd9022007fc5d84482168edfc7a35aae586f207e68f4557a36d47f01ae17dd71b9a9d2901,02bcbf3250ea8ae47c710274a06e344a42d959a1f40e256431de0af66622c5eaa1",
            "lifespan": 2877,
            "cdd": 0
        }
    ],
    "outputs": [
        {
            "block_id": 672885,
            "transaction_id": 621202225,
            "index": 0,
            "transaction_hash": "0056281655e3942cd69e3ec252e2dbe7605ff264d03bdf626e83eccb51462b0b",
            "date": "2021-03-02",
            "time": "2021-03-02 20:37:32",
            "value": 7012364,
            "value_usd": 3509.3376,
            "recipient": "1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj",
            "type": "pubkeyhash",
            "script_hex": "76a914bd8e2964ae5fb38e225e2f189da6e0604667cab088ac",
            "is_from_coinbase": false,
            "is_spendable": null,
            "is_spent": true,
            "spending_block_id": 673153,
            "spending_transaction_id": 621793564,
            "spending_index": 2,
            "spending_transaction_hash": "f7661801f63b229e3102f3c8d72974636b684da3f476cfb589d5b09a9b1d9769",
            "spending_date": "2021-03-04",
            "spending_time": "2021-03-04 18:47:19",
            "spending_value_usd": 3520.347,
            "spending_sequence": 4294967295,
            "spending_signature_hex": "4830450221009e811f296a37dd53965f72adb4c838c52d4a8822915e5c24eb6d1dbffc061dac02201ae557f49ab0953c050f2e75dfd88a348ac08ca34a55e95cfeac8cbb41a1d924012103d11a188557b1c99f083c00221f378952ed812c02f060139851c42b88ada8fc8a",
            "spending_witness": "",
            "lifespan": 166187,
            "cdd": 0
        },
        {
            "block_id": 672885,
            "transaction_id": 621202225,
            "index": 1,
            "transaction_hash": "0056281655e3942cd69e3ec252e2dbe7605ff264d03bdf626e83eccb51462b0b",
            "date": "2021-03-02",
            "time": "2021-03-02 20:37:32",
            "value": 19369839,
            "value_usd": 9693.636,
            "recipient": "3GibDvwUZJpqR48u1kFoNFtKnguSTVoJwj",
            "type": "scripthash",
            "script_hex": "a914a4d61997c720fd94c658bd05f46d05cf76cdf01487",
            "is_from_coinbase": false,
            "is_spendable": null,
            "is_spent": true,
            "spending_block_id": 673038,
            "spending_transaction_id": 621538686,
            "spending_index": 0,
            "spending_transaction_hash": "c6031e6737c709979776aabcabd4f9736f07a0798147115136fe2bd2fe4e42c7",
            "spending_date": "2021-03-03",
            "spending_time": "2021-03-03 20:52:49",
            "spending_value_usd": 9400.57,
            "spending_sequence": 0,
            "spending_signature_hex": "160014fe794caf1e4d91c710ef709b201b974ef7090aa4",
            "spending_witness": "3045022100f36bb428ba7f5c8474415381dca1c5bc706d6a0d331d0b904b273aca2264fdcd02207fc524f04bd07ee08754f3e715e1f5d58cbc922cf208a8d7956037bd18d51edd01,03d712523c7f4b605fb6fb7ede74c989cb3638d317ddb35c4534cc684447921a90",
            "lifespan": 87317,
            "cdd": 0
        }
    ]
}
"""
