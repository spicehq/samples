from argparse import ArgumentParser

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
    schema: flight.SchemaResult = client.get_schema(flight.FlightDescriptor.for_command(
        'SELECT * FROM eth.blocks LIMIT 0;'), options)
    print(schema.schema)


if __name__ == '__main__':
    main()
