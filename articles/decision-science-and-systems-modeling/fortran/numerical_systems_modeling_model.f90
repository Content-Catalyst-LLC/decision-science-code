! numerical_systems_modeling_model.f90
! Compile with: gfortran numerical_systems_modeling_model.f90 -o numerical_systems_modeling_model

program numerical_systems_modeling_model
  implicit none

  real :: stock
  real :: next_stock
  real :: next_state
  real :: systems_score

  stock = 100.0
  next_stock = stock + 12.0 - 8.5
  next_state = 55.0 + 3.85 - 2.10 - 0.4
  systems_score = 0.35 * 0.78 + 0.25 * 0.82 + 0.20 * 0.79 + 0.20 * 1.0

  print *, "Next stock:", next_stock
  print *, "Next state:", next_state
  print *, "Systems decision score:", systems_score

end program numerical_systems_modeling_model
