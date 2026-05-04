package main

import "fmt"

type Outcome struct {
	Probability float64
	Value       float64
}

func expectedValue(outcomes []Outcome) float64 {
	total := 0.0

	for _, outcome := range outcomes {
		total += outcome.Probability * outcome.Value
	}

	return total
}

func main() {
	outcomes := []Outcome{
		{Probability: 0.65, Value: 72.0},
		{Probability: 0.35, Value: 38.0},
	}

	fmt.Println("Expected value:")
	fmt.Printf("%.3f\n", expectedValue(outcomes))
}
