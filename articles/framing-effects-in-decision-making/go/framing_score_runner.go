// framing_score_runner.go
// Run with: go run framing_score_runner.go

package main

import (
	"fmt"
	"math"
)

func prospectValue(x float64, alpha float64, beta float64, lossAversion float64) float64 {
	if x >= 0 {
		return math.Pow(x, alpha)
	}
	return -lossAversion * math.Pow(-x, beta)
}

func main() {
	fmt.Printf("Gain value: %.6f\n", prospectValue(100.0, 0.88, 0.88, 2.0))
	fmt.Printf("Loss value: %.6f\n", prospectValue(-100.0, 0.88, 0.88, 2.0))
}
