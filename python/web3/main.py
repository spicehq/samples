from web3 import Web3


def main():
    url = "https://data.spiceai.io/eth"
    w3 = Web3(Web3.HTTPProvider(url))
    if not w3.isConnected():
        print(f"Cannot connect to {url}")
    print(w3.eth.get_block("latest"))


if __name__ == '__main__':
    main()
