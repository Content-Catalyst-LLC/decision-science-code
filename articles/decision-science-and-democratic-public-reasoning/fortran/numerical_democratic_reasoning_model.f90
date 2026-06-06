! numerical_democratic_reasoning_model.f90
! Compile with: gfortran numerical_democratic_reasoning_model.f90 -o numerical_democratic_reasoning_model

program numerical_democratic_reasoning_model
  implicit none

  real :: legitimacy
  real :: trust

  legitimacy = 0.17 * 0.88 + 0.17 * 0.88 + 0.18 * 0.88 + 0.16 * 0.84 + 0.16 * 0.86 + 0.16 * 0.88
  trust = max(0.0, min(1.0, 0.62 + 0.08 * 0.70 + 0.06 * 0.78 + 0.08 * 0.74 + 0.08 * 0.72 - 0.06 * 0.36 - 0.10 * 0.30))

  print *, "Legitimacy score:", legitimacy
  print *, "Next trust:", trust

end program numerical_democratic_reasoning_model
