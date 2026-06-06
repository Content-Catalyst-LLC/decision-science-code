! numerical_scenario_choice_model.f90
! Compile with: gfortran numerical_scenario_choice_model.f90 -o numerical_scenario_choice_model

program numerical_scenario_choice_model
  implicit none

  real, dimension(5) :: values
  real, dimension(5) :: probabilities
  real :: expected_value
  real :: worst_case
  real :: threshold_pass_rate
  integer :: i
  integer :: pass_count

  values = (/0.78, 0.76, 0.82, 0.80, 0.81/)
  probabilities = (/0.22, 0.24, 0.20, 0.18, 0.16/)

  expected_value = 0.0
  pass_count = 0

  do i = 1, 5
    expected_value = expected_value + values(i) * probabilities(i)
    if (values(i) >= 0.70) then
      pass_count = pass_count + 1
    end if
  end do

  worst_case = minval(values)
  threshold_pass_rate = real(pass_count) / 5.0

  print *, "Expected value:", expected_value
  print *, "Worst case:", worst_case
  print *, "Threshold pass rate:", threshold_pass_rate

end program numerical_scenario_choice_model
