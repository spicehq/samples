from web3 import Web3


def main():
    w3 = Web3(Web3.HTTPProvider("https://data.spiceai.io/eth?api_key=API_KEY"))
    print(f"The latest block number is {w3.eth.get_block_number()}")


if __name__ == '__main__':
    main()
