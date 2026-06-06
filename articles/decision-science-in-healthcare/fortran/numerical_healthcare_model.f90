! numerical_healthcare_model.f90
! Compile with: gfortran numerical_healthcare_model.f90 -o numerical_healthcare_model

program numerical_healthcare_model
  implicit none

  real :: treatment_value_score
  real :: queue_next
  real :: queue_pressure

  treatment_value_score = 0.30 * 0.72 - 0.18 * 0.12 - 0.14 * 0.54 + 0.18 * 0.88 + 0.10 * 0.76 + 0.10 * 0.70
  queue_next = max(0.0, 18.0 + 24.0 - 22.0)
  queue_pressure = min(1.0, queue_next / 60.0)

  print *, "Treatment value score:", treatment_value_score
  print *, "Queue next:", queue_next
  print *, "Queue pressure:", queue_pressure

end program numerical_healthcare_model
