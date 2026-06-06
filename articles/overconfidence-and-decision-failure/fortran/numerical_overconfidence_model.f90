! numerical_overconfidence_model.f90
! Compile with: gfortran numerical_overconfidence_model.f90 -o numerical_overconfidence_model

program numerical_overconfidence_model
  implicit none

  real :: probability
  real :: outcome
  real :: brier
  real :: confidence
  real :: accuracy_proxy
  real :: confidence_gap
  real :: actual
  real :: estimate
  real :: planning_gap

  probability = 0.69
  outcome = 0.0
  confidence = 0.88
  accuracy_proxy = 0.52
  actual = 520.0
  estimate = 365.0

  brier = (probability - outcome) ** 2
  confidence_gap = confidence - accuracy_proxy
  planning_gap = (actual - estimate) / estimate

  print *, "Brier score:", brier
  print *, "Confidence error:", confidence_gap
  print *, "Planning error:", planning_gap

end program numerical_overconfidence_model
