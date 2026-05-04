program expected_value_model
  implicit none

  real, dimension(2) :: probabilities
  real, dimension(2) :: values
  real :: ev

  probabilities = (/0.65, 0.35/)
  values = (/72.0, 38.0/)

  ev = sum(probabilities * values)

  print *, "Expected value:", ev

end program expected_value_model
