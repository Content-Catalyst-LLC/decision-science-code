! numerical_value_of_information_model.f90
! Compile with: gfortran numerical_value_of_information_model.f90 -o numerical_value_of_information_model

program numerical_value_of_information_model
  implicit none

  real :: values(4)
  real :: probabilities(4)
  real :: expected_value
  real :: evpi
  real :: net_value_waiting
  integer :: i

  values = (/82.0, 28.0, 40.0, 76.0/)
  probabilities = (/0.35, 0.25, 0.20, 0.20/)

  expected_value = 0.0
  do i = 1, 4
    expected_value = expected_value + values(i) * probabilities(i)
  end do

  evpi = 76.4 - 68.1
  net_value_waiting = 4.4 - 2.0 - 1.3

  print *, "Expected value:", expected_value
  print *, "EVPI:", evpi
  print *, "Net value waiting:", net_value_waiting

end program numerical_value_of_information_model
