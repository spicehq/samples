from argparse import ArgumentParser

import matplotlib.pyplot as plt
from spicepy import Client


def main():
    parser = ArgumentParser()
    parser.add_argument('api_key', help='API key to authenticate with')
    arguments = parser.parse_args()

    print('Connecting..')
    client = Client(arguments.api_key)
    print('Querrying data...')
    reader = client.query(
        'SELECT number, "timestamp" FROM eth.recent_blocks ORDER BY number DESC;')
    data = reader.read_pandas()
    print('Data received')

    data = data.iloc[::-1]  # reverse order
    data['time'] = data['timestamp'].astype('datetime64[s]')
    data['dayofweek'] = data['time'].dt.dayofweek
    data['mining_time'] = data['timestamp'].diff()
    data = data.dropna()  # Dropping firt row as diff will output NaN
    aggregated_data = data.groupby(['dayofweek']).mean()

    _, axe = plt.subplots()
    axe.plot(aggregated_data.index, aggregated_data['mining_time'])
    axe.set_title(f'Mining time from {data["time"].iloc[0]} to {data["time"].iloc[-1]}')
    axe.set_ylabel('Average mining time')
    axe.set_xlabel('Day of Week')
    plt.show()


if __name__ == '__main__':
    main()
