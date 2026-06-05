! numerical_bayesian_model.f90
! Compile with: gfortran numerical_bayesian_model.f90 -o numerical_bayesian_model

program numerical_bayesian_model
  implicit none

  real :: prior
  real :: sensitivity
  real :: false_positive_rate
  real :: posterior

  prior = 0.10
  sensitivity = 0.86
  false_positive_rate = 0.12

  posterior = (sensitivity * prior) / ((sensitivity * prior) + (false_positive_rate * (1.0 - prior)))

  print *, "Posterior:", posterior

end program numerical_bayesian_model
