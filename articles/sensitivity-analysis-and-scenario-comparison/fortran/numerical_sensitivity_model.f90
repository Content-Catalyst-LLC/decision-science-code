! numerical_sensitivity_model.f90
! Compile with: gfortran numerical_sensitivity_model.f90 -o numerical_sensitivity_model

program numerical_sensitivity_model
  implicit none

  real :: base, demand_sensitivity, cost_sensitivity
  real :: disruption_sensitivity, resilience_buffer, adaptation_capacity
  real :: demand, cost, disruption, score

  base = 75.0
  demand_sensitivity = 8.0
  cost_sensitivity = 10.0
  disruption_sensitivity = 11.0
  resilience_buffer = 9.0
  adaptation_capacity = 7.0
  demand = 0.5
  cost = 0.3
  disruption = 0.2

  score = base + demand_sensitivity * demand - cost_sensitivity * cost - &
          disruption_sensitivity * disruption + resilience_buffer * max(0.0, disruption) + &
          adaptation_capacity * abs(demand)

  print *, "Balanced strategy score:", score

end program numerical_sensitivity_model
