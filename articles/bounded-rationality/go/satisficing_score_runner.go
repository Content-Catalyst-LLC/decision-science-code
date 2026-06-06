// satisficing_score_runner.go
// Run with: go run satisficing_score_runner.go

package main

import "fmt"

func firstSatisficing(values []float64, aspiration float64) (int, float64, bool) {
	for i, value := range values {
		if value >= aspiration {
			return i + 1, value, true
		}
	}
	return -1, 0.0, false
}

func main() {
	values := []float64{0.58, 0.71, 0.82, 0.77, 0.91}
	index, value, ok := firstSatisficing(values, 0.75)
	fmt.Printf("Found: %v option: %d value: %.6f\n", ok, index, value)
}
