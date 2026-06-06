! numerical_tradeoff_model.f90
! Compile with: gfortran numerical_tradeoff_model.f90 -o numerical_tradeoff_model

program numerical_tradeoff_model
  implicit none

  real :: scores(6)
  real :: weights(6)
  real :: total
  real :: regret_value
  integer :: i

  scores = (/0.90, 0.38, 0.42, 0.54, 0.48, 0.70/)
  weights = (/0.18, 0.18, 0.20, 0.18, 0.14, 0.12/)
  total = 0.0

  do i = 1, 6
    total = total + scores(i) * weights(i)
  end do

  regret_value = 0.91 - 0.72

  print *, "Weighted score:", total
  print *, "Regret:", regret_value

end program numerical_tradeoff_model
