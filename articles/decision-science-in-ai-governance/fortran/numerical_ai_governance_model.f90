! numerical_ai_governance_model.f90
! Compile with: gfortran numerical_ai_governance_model.f90 -o numerical_ai_governance_model

program numerical_ai_governance_model
  implicit none

  real :: composite_risk
  real :: drift

  composite_risk = 0.20 * 0.52 + 0.18 * 0.48 + 0.16 * 0.50 + 0.16 * 0.42 + 0.14 * 0.55 + 0.16 * 0.46
  drift = abs(0.77 - 0.86)

  print *, "Composite AI risk:", composite_risk
  print *, "Drift indicator:", drift

end program numerical_ai_governance_model
