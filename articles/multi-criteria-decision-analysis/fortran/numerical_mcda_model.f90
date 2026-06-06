! numerical_mcda_model.f90
! Compile with: gfortran numerical_mcda_model.f90 -o numerical_mcda_model

program numerical_mcda_model
  implicit none

  real :: scores(3)
  real :: weights(3)
  real :: total
  integer :: i

  scores = (/0.8, 0.6, 0.9/)
  weights = (/0.3, 0.3, 0.4/)
  total = 0.0

  do i = 1, 3
    total = total + scores(i) * weights(i)
  end do

  print *, "Weighted score:", total

end program numerical_mcda_model
