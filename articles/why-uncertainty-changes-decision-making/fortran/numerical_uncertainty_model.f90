! numerical_uncertainty_model.f90
! Compile with: gfortran numerical_uncertainty_model.f90 -o numerical_uncertainty_model

program numerical_uncertainty_model
  implicit none

  real :: p(5)
  real :: expand(5), hedge(5), preserve(5), adaptive(5)

  p = (/0.40, 0.24, 0.16, 0.10, 0.10/)
  expand = (/120.0, 45.0, -95.0, -130.0, 20.0/)
  hedge = (/92.0, 68.0, 18.0, -20.0, 55.0/)
  preserve = (/72.0, 62.0, 42.0, 18.0, 70.0/)
  adaptive = (/95.0, 72.0, 34.0, 10.0, 78.0/)

  print *, "Expand EV:", sum(p * expand)
  print *, "Hedge EV:", sum(p * hedge)
  print *, "Preserve Option EV:", sum(p * preserve)
  print *, "Adaptive Pathway EV:", sum(p * adaptive)

end program numerical_uncertainty_model
