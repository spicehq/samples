using Spice;

var client = new SpiceClientBuilder()
        .WithApiKey(ApiKey)
        .WithSpiceCloud()
        .Build();

var reader = await client.Query("SELECT number, \"timestamp\", base_fee_per_gas, base_fee_per_gas / 1e9 AS base_fee_per_gas_gwei FROM eth.recent_blocks limit 10");

var enumerator = reader.GetAsyncEnumerator();

while (await enumerator.MoveNextAsync())
{
    var batch = enumerator.Current;
    Console.WriteLine(batch);
}
