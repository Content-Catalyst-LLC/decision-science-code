program numerical_robustness_model
  implicit none
  real :: values(6), weights(6), expected_value, worst_case
  integer :: i
  values = (/0.73, 0.77, 0.79, 0.81, 0.76, 0.86/)
  weights = (/0.18, 0.17, 0.18, 0.16, 0.15, 0.16/)
  expected_value = 0.0
  worst_case = values(1)
  do i = 1, 6
    expected_value = expected_value + values(i) * weights(i)
    if (values(i) < worst_case) worst_case = values(i)
  end do
  print *, "Expected value:", expected_value
  print *, "Worst case:", worst_case
end program numerical_robustness_model
