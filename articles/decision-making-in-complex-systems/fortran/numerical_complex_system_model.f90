! numerical_complex_system_model.f90
! Compile with: gfortran numerical_complex_system_model.f90 -o numerical_complex_system_model

program numerical_complex_system_model
  implicit none

  real :: adaptability
  real :: robustness
  real :: feedback_awareness
  real :: interdependence
  real :: coordination_burden
  real :: legitimacy
  real :: threshold_resilience
  real :: complex_score
  real :: next_state

  adaptability = 0.81
  robustness = 0.86
  feedback_awareness = 0.82
  interdependence = 0.83
  coordination_burden = 0.44
  legitimacy = 0.78
  threshold_resilience = 0.86

  complex_score = 0.18 * adaptability + 0.18 * robustness + 0.16 * feedback_awareness + &
                  0.16 * interdependence - 0.10 * coordination_burden + 0.12 * legitimacy + &
                  0.20 * threshold_resilience

  next_state = 52.0 + 3.0 - 1.4 - 0.2

  print *, "Complex-system score:", complex_score
  print *, "Next state:", next_state

end program numerical_complex_system_model
