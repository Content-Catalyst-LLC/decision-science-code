! Compile with: gfortran numerical_ethics_model.f90 -o numerical_ethics_model
program numerical_ethics_model
  implicit none
  real :: ethical_risk
  real :: legitimacy
  ethical_risk = max(0.0, min(1.0, 0.30 * 0.64 + 0.20 * 0.58 + 0.22 * 0.68 + 0.18 * 0.56 - 0.10 * 0.46))
  legitimacy = 0.26 * 0.82 + 0.24 * 0.80 + 0.25 * 0.86 + 0.25 * 0.90
  print *, "Ethical risk:", ethical_risk
  print *, "Legitimacy:", legitimacy
end program numerical_ethics_model
