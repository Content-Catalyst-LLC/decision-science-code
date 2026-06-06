// Run with: go run ethics_runner.go
package main
import "fmt"
func clamp(v, low, high float64) float64 { if v < low { return low }; if v > high { return high }; return v }
func ethicalRisk(h, o, e, i, a float64) float64 { return clamp(0.30*h+0.20*o+0.22*e+0.18*i-0.10*a, 0.0, 1.0) }
func legitimacy(t, p, c, a float64) float64 { return 0.26*t + 0.24*p + 0.25*c + 0.25*a }
func main() {
	fmt.Printf("Ethical risk: %.6f\n", ethicalRisk(0.64, 0.58, 0.68, 0.56, 0.46))
	fmt.Printf("Legitimacy: %.6f\n", legitimacy(0.82, 0.80, 0.86, 0.90))
}
