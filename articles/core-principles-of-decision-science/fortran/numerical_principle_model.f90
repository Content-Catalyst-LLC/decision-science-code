! numerical_principle_model.f90
! Compile with: gfortran numerical_principle_model.f90 -o numerical_principle_model

program numerical_principle_model
  implicit none

  real :: weights(9)
  real :: adaptive(9)

  weights = (/0.12, 0.14, 0.12, 0.10, 0.11, 0.14, 0.12, 0.08, 0.07/)
  adaptive = (/0.88, 0.87, 0.85, 0.84, 0.86, 0.86, 0.93, 0.84, 0.88/)

  print *, "Adaptive Learning Strategy score:", sum(weights * adaptive)

end program numerical_principle_model
