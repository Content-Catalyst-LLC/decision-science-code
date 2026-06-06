! numerical_alignment_model.f90
! Compile with: gfortran numerical_alignment_model.f90 -o numerical_alignment_model

program numerical_alignment_model
  implicit none

  real :: scores(6)
  real :: weights(6)
  real :: total
  integer :: i

  scores = (/0.86, 0.88, 0.82, 0.86, 0.89, 0.77/)
  weights = (/0.16, 0.15, 0.17, 0.18, 0.18, 0.16/)
  total = 0.0

  do i = 1, 6
    total = total + scores(i) * weights(i)
  end do

  print *, "Decision quality score:", total

end program numerical_alignment_model
