package main

import (
	"context"
	"fmt"

	"github.com/spiceai/gospice"
)

func main() {
	spice := gospice.NewSpiceClient()

	spice.Init("API_KEY")

	reader, err := spice.Query(context.Background(), "SELECT * FROM eth.recent_blocks ORDER BY number LIMIT 10")
	if err != nil {
		panic(fmt.Errorf("error querying: %w", err))
	}

	for reader.Next() {
		record := reader.Record()
		defer record.Release()

		fmt.Printf("%v\n", record)
	}

	reader.Release()
	spice.Close()
}
