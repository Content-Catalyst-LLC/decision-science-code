// rollback_score_runner.go
// Run with: go run rollback_score_runner.go

package main

import "fmt"

func expectedValue(successPayoff float64, failurePayoff float64, successProbability float64, cost float64, credit float64) float64 {
	return successPayoff*successProbability + failurePayoff*(1.0-successProbability) - cost + credit
}

func main() {
	immediate := expectedValue(125.0, -35.0, 0.58, 0.0, 0.0)
	staged := expectedValue(145.0, -20.0, 0.54, 12.0, 18.0)

	fmt.Printf("Immediate EV: %.4f\n", immediate)
	fmt.Printf("Staged EV: %.4f\n", staged)
	fmt.Printf("Net value of staging: %.4f\n", staged-immediate)
}
