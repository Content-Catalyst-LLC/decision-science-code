! numerical_feedback_delay_model.f90
! Compile with: gfortran numerical_feedback_delay_model.f90 -o numerical_feedback_delay_model

program numerical_feedback_delay_model
  implicit none

  real :: next_state
  real :: net_policy_effect
  real :: feedback_adjusted_score

  next_state = 50.0 + 4.0 - 1.12 + 0.4 - 0.3
  net_policy_effect = 0.8 * 10.0 - 0.4 * 6.0
  feedback_adjusted_score = 0.35 * 0.42 + 0.25 * 0.79 + 0.20 * 0.76 + 0.20 * 1.0

  print *, "Next state:", next_state
  print *, "Net policy effect:", net_policy_effect
  print *, "Feedback-adjusted score:", feedback_adjusted_score

end program numerical_feedback_delay_model
