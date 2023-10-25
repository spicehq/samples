use spice_rs::Client;
use futures::stream::StreamExt;

let mut spice_client = Client::new("api_key").await;

match spice_client.query(
    "SELECT number, \"timestamp\", base_fee_per_gas, base_fee_per_gas / 1e9 AS base_fee_per_gas_gwei FROM eth.recent_blocks limit 10"
    ).await {
        Ok(mut flight_data_stream) => {
            // Read back RecordBatches
            while let Some(batch) = flight_data_stream.next().await {
            match batch {
                Ok(batch) => {                   
                    /* process batch */
                    println!("{:?}", batch)
                },
                Err(e) => { /* handle error */ },
            };
            }
        }
        Err(e) => { /* handle error */ }
    };