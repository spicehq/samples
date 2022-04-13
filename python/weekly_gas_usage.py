from argparse import ArgumentParser

import matplotlib.pyplot as plt
import pandas as pd
from spicepy import Client


def main():
    parser = ArgumentParser()
    parser.add_argument('api_key', help='API key to authenticate with')
    arguments = parser.parse_args()

    print('Connecting..')
    client = Client(arguments.api_key)
    print('Querrying data...')
    reader = client.query(
        'SELECT "timestamp", gas_used FROM eth.recent_blocks ORDER BY "timestamp" DESC;')
    data = reader.read_pandas()
    print('Data received')
    data = data.iloc[::-1]  # reverse order
    data = data.set_index(pd.DatetimeIndex(data['timestamp'].astype('datetime64[s]')))
    del data['timestamp']
    aggregated_data = data.groupby([pd.Grouper(freq='1W')])['gas_used']
    aggregated_data = aggregated_data.mean().dropna()
    aggregated_data /= 1_000_000
    aggregated_data = aggregated_data.iloc[1:-1]

    _, axe = plt.subplots()
    axe.plot(aggregated_data, marker='o')
    axe.set_title('Weekly Average Gas Usage')
    axe.set_ylabel('Gas Used (in millions)')
    plt.show()


if __name__ == '__main__':
    main()
