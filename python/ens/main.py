from audioop import add
from web3 import Web3
import spicepy
from pyarrow import csv
import pandas as pd
import os
import requests
from functools import reduce
from multiprocessing import Pool, freeze_support

# Params

csv_file_name = "twitter1.csv"
eth_column_name = "eth_name"
api_key = ''

##

host = "https://data.spiceai.io"
client = spicepy.Client(api_key)


def getBalance(address):
    checksum_address = Web3.toChecksumAddress(address)
    balance = client.w3.eth.get_balance(checksum_address) / 1e18  # wei -> eth
    return balance


if __name__ == '__main__':
    if not os.path.exists(csv_file_name):
        print("ERROR: CSV file " + csv_file_name + "  not found")
        exit(1)

    if not api_key or len(api_key) == 0:
        print("ERROR: API key not set")
        exit(1)

    pool = Pool(processes=3)

    print("Processing " + csv_file_name + " ...")
    csv_data = csv.read_csv(csv_file_name)

    column = csv_data.column(eth_column_name)
    if not column:
        print("ERROR: Column " + eth_column_name + " not found")
        exit(1)

    eth_names = column.combine_chunks().to_pylist()
    unique_eth_names = []

    body = ""

    for eth_name in eth_names:
        parts = os.path.splitext(eth_name.lower())
        if len(parts) < 2 or (not parts[1].__contains__(".eth") and not parts[1].__contains__(".𝚎𝚝𝚑")):
            if eth_name != "NA" and eth_name != "":
                print("Skipping invalid name: " + eth_name)
        else:
            cleaned_name = f"{parts[0]}.eth"

        if cleaned_name and cleaned_name not in unique_eth_names:
            body += cleaned_name + "\n"
            unique_eth_names.append(cleaned_name)

    print("Processing complete. Found " +
          str(len(unique_eth_names)) + " unique names.")

    print("Checking health of " + host + " ...")
    resp = requests.get(host + '/health')
    print("Health: " + resp.text)
    resp.close

    print("Sending request to " + host + " ...")
    resp = requests.post(
        host + '/ens/v0.1/address', body.strip("\n").encode('utf-8'), headers={
            'Content-Type': 'text/plain',
            'X-API-Key': api_key
        })

    result = resp.text.splitlines()
    resp.close()

    if len(unique_eth_names) != len(result):
        print("ERROR: number of names does not match number of results")
        print("names: " + str(len(unique_eth_names)))
        print("results: " + str(len(result)))
        exit()

    addresses = []
    valid_names = []

    for i, name in enumerate(unique_eth_names):
        line = result[i]
        if line.startswith("200:"):
            valid_names.append(name)
            address = line[4:].lower()
            addresses.append(address)

    quoted_addresses = [f"'{address.lower()}'" for address in addresses]

    print("Querying Spice.ai for contracts ...")
    sql = 'SELECT address, erc20_confidence, erc721_confidence, erc1155_confidence FROM eth.contracts WHERE address in (' + ",".join(
        quoted_addresses) + ')'
    contracts = client.query(sql).read_pandas()

    print("Fetching wallet balances ...")
    balances = pool.map(getBalance, addresses)

    domains = pd.DataFrame(list(zip(valid_names, addresses, balances)),
                           columns=['name', 'address', 'balance'])

    merged_df = reduce(lambda left, right: pd.merge(left, right, on=['address'],
                                                    how='outer'), [domains, contracts]).fillna('none')

    final_df = merged_df.assign(
        is_contract=merged_df['erc20_confidence'] != 'none')

    print(final_df.sort_values(by=['balance'], ascending=False))
