! numerical_public_policy_model.f90
! Compile with: gfortran numerical_public_policy_model.f90 -o numerical_public_policy_model

program numerical_public_policy_model
  implicit none

  real :: policy_value_score
  real :: drift_next
  logical :: requires_review

  policy_value_score = 0.18 * 0.72 + 0.22 * 0.84 + 0.18 * 0.70 + 0.14 * 0.76 + 0.14 * 0.80 + 0.14 * 0.86
  drift_next = max(0.0, 6.0 + 0.40 - 0.030 * 12.0 - 0.020 * 22.0)
  requires_review = (0.46 < 0.55) .or. (0.54 < 0.55) .or. (0.68 < 0.55)

  print *, "Policy value score:", policy_value_score
  print *, "Implementation drift next:", drift_next
  print *, "Requires review?", requires_review

end program numerical_public_policy_model
