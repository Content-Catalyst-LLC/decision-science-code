! numerical_behavioral_choice_model.f90
! Compile with: gfortran numerical_behavioral_choice_model.f90 -o numerical_behavioral_choice_model

program numerical_behavioral_choice_model
  implicit none

  real :: gain
  real :: loss
  real :: alpha
  real :: beta
  real :: lambda
  real :: gain_value
  real :: loss_value

  gain = 100.0
  loss = -100.0
  alpha = 0.88
  beta = 0.88
  lambda = 2.0

  gain_value = gain ** alpha
  loss_value = -lambda * ((-loss) ** beta)

  print *, "Gain value:", gain_value
  print *, "Loss value:", loss_value

end program numerical_behavioral_choice_model
