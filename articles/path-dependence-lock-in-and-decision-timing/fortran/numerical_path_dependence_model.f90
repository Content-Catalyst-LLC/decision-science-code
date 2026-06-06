! numerical_path_dependence_model.f90
! Compile with: gfortran numerical_path_dependence_model.f90 -o numerical_path_dependence_model

program numerical_path_dependence_model
  implicit none

  real :: switching_cost
  real :: lock_in_risk
  logical :: review

  switching_cost = 0.36 * 0.55 + 0.34 * 0.62 + 0.30 * 0.58
  lock_in_risk = 0.42 * switching_cost + 0.28 * 0.62 + 0.20 * 0.55 - 0.10 * 0.40
  review = (lock_in_risk >= 0.72) .or. (0.40 <= 0.35)

  print *, "Switching cost:", switching_cost
  print *, "Lock-in risk:", lock_in_risk
  print *, "Review?", review

end program numerical_path_dependence_model
