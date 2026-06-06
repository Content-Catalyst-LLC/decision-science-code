! numerical_regret_model.f90
! Compile with: gfortran numerical_regret_model.f90 -o numerical_regret_model

program numerical_regret_model
  implicit none

  real :: values(6)
  real :: weights(6)
  real :: regrets(6)
  real :: expected_value
  real :: maximin_value
  real :: maximum_regret_value
  integer :: i

  values = (/0.73, 0.81, 0.79, 0.87, 0.76, 0.77/)
  weights = (/0.18, 0.16, 0.18, 0.17, 0.15, 0.16/)
  regrets = (/0.19, 0.00, 0.05, 0.01, 0.06, 0.06/)

  expected_value = 0.0
  maximin_value = values(1)
  maximum_regret_value = regrets(1)

  do i = 1, 6
    expected_value = expected_value + values(i) * weights(i)
    if (values(i) < maximin_value) then
      maximin_value = values(i)
    end if
    if (regrets(i) > maximum_regret_value) then
      maximum_regret_value = regrets(i)
    end if
  end do

  print *, "Expected value:", expected_value
  print *, "Maximin value:", maximin_value
  print *, "Maximum regret:", maximum_regret_value

end program numerical_regret_model
