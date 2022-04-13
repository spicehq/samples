from argparse import ArgumentParser

import matplotlib.pyplot as plt
from pyarrow import flight

from grpc_cert import get_grpc_cert


def main():
    parser = ArgumentParser()
    parser.add_argument('api_key', help='API key to authenticate with')
    arguments = parser.parse_args()

    get_grpc_cert()

    print('Connecting..')
    client = flight.connect('grpc+tls://flight.spiceai.io')
    token_pair = client.authenticate_basic_token('', arguments.api_key)
    options = flight.FlightCallOptions(headers=[token_pair])
    print('Querrying data...')
    flight_info = client.get_flight_info(flight.FlightDescriptor.for_command(
        'SELECT number, "timestamp" FROM eth.recent_blocks ORDER BY number DESC;'), options)
    reader = client.do_get(flight_info.endpoints[0].ticket, options)
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
