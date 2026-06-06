! numerical_governance_model.f90
! Compile with: gfortran numerical_governance_model.f90 -o numerical_governance_model

program numerical_governance_model
  implicit none

  real :: accountability
  real :: gap

  accountability = 0.18 * 0.82 + 0.17 * 0.86 + 0.18 * 0.88 + 0.17 * 0.84 + 0.15 * 0.90 + 0.15 * 0.92
  gap = max(0.0, 0.62 - 0.34)

  print *, "Accountability score:", accountability
  print *, "Responsibility gap:", gap

end program numerical_governance_model
