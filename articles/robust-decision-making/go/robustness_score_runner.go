package main
import "fmt"
func expectedValue(values []float64, weights []float64) float64 { total := 0.0; for i := range values { total += values[i] * weights[i] }; return total }
func worstCase(values []float64) float64 { worst := values[0]; for _, value := range values { if value < worst { worst = value } }; return worst }
func passRate(values []float64, threshold float64) float64 { passed := 0; for _, value := range values { if value >= threshold { passed++ } }; return float64(passed) / float64(len(values)) }
func main() { values := []float64{0.73, 0.77, 0.79, 0.81, 0.76, 0.86}; weights := []float64{0.18, 0.17, 0.18, 0.16, 0.15, 0.16}; fmt.Printf("Expected value: %.6f\n", expectedValue(values, weights)); fmt.Printf("Worst case: %.6f\n", worstCase(values)); fmt.Printf("Pass rate: %.6f\n", passRate(values, 0.70)) }
