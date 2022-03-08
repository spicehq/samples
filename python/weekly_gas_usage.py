from argparse import ArgumentParser

import matplotlib.pyplot as plt
import pandas as pd
from pyarrow import flight


def main():
    parser = ArgumentParser()
    parser.add_argument('api_key', help='API key to authenticate with')
    arguments = parser.parse_args()

    print('Connecting..')
    client = flight.connect('grpc+tls://flight.spiceai.io')
    token_pair = client.authenticate_basic_token('', arguments.api_key)
    options = flight.FlightCallOptions(headers=[token_pair])
    print('Querrying data...')
    flight_info = client.get_flight_info(
        flight.FlightDescriptor.for_command(
            'SELECT number, "timestamp", gas_used FROM eth.blocks ORDER BY "timestamp" DESC LIMIT 5000000;'),
        options)
    reader = client.do_get(flight_info.endpoints[0].ticket, options)
    data = reader.read_pandas()
    print('Data received')
    data = data.iloc[::-1]  # reverse order
    data = data.set_index(pd.DatetimeIndex(data['timestamp'].astype('datetime64[s]')))
    del data['timestamp']
    del data['number']
    aggregated_data = data.groupby([pd.Grouper(freq='1W')])['gas_used']
    aggregated_data = aggregated_data.mean().dropna()
    aggregated_data /= 1_000_000
    aggregated_data = aggregated_data.iloc[1:-1]

    _, axe = plt.subplots()
    axe.plot(aggregated_data, marker='o')
    axe.set_title('Weekly Average Gas Usage')
    axe.set_ylabel('Gas Used')
    plt.show()


if __name__ == '__main__':
    main()
