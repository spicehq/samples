from argparse import ArgumentParser

from spicepy import Client


def main():
    parser = ArgumentParser()
    parser.add_argument('api_key', help='Spice.xyz API key')
    arguments = parser.parse_args()

    print('Connecting..')
    client = Client(arguments.api_key)
    print('Querying data...')
    reader = client.query('SELECT number, "hash" FROM eth.recent_blocks ORDER BY number DESC LIMIT 10;')
    data = reader.read_pandas()
    print(data)


if __name__ == '__main__':
    main()
