package main

import "fmt"

func crisisRisk(likelihood float64, severity float64, exposure float64, vulnerability float64, criticality float64) float64 {
	return likelihood * severity * exposure * vulnerability * criticality
}

func main() {
	fmt.Printf("Crisis risk: %.6f\n", crisisRisk(0.72, 0.86, 0.68, 0.62, 0.90))
}
