use futures::stream::StreamExt;
use spice_rs::*;

let mut spice_client = new_spice_client(api_key).await;

match spice_client.query(
    "SELECT number, \"timestamp\", base_fee_per_gas, base_fee_per_gas / 1e9 AS base_fee_per_gas_gwei FROM eth.recent_blocks limit 10".to_string()
    ).await {
        Ok(mut flight_data_stream) => {
              // Read back RecordBatches
            while let Some(batch) = flight_data_stream.next().await {
            match batch {
                Ok(batch) => {
                    println!("{:?}", batch);
                },
                Err(e) => {
                    assert!(false, "Error: {}", e)
                },
            };
            }
        }
        Err(e) => {
            assert!(false, "Error: {}", e);
        }
    };