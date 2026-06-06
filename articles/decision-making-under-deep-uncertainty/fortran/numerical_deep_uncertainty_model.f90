! numerical_deep_uncertainty_model.f90
! Compile with: gfortran numerical_deep_uncertainty_model.f90 -o numerical_deep_uncertainty_model

program numerical_deep_uncertainty_model
  implicit none

  real :: values(6)
  real :: weights(6)
  real :: expected_value
  real :: worst_case
  integer :: i

  values = (/0.72, 0.80, 0.78, 0.87, 0.75, 0.77/)
  weights = (/0.1666667, 0.1666667, 0.1666667, 0.1666667, 0.1666667, 0.1666667/)
  expected_value = 0.0
  worst_case = values(1)

  do i = 1, 6
    expected_value = expected_value + values(i) * weights(i)
    if (values(i) < worst_case) then
      worst_case = values(i)
    end if
  end do

  print *, "Expected value:", expected_value
  print *, "Worst case:", worst_case

end program numerical_deep_uncertainty_model
