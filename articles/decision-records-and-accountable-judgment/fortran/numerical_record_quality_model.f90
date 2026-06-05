! numerical_record_quality_model.f90
! Compile with: gfortran numerical_record_quality_model.f90 -o numerical_record_quality_model

program numerical_record_quality_model
  implicit none

  real :: weights(11)
  real :: record(11)
  real :: quality
  real :: accountable

  weights = (/0.10,0.09,0.11,0.11,0.12,0.10,0.09,0.10,0.09,0.09,0.10/)
  record = (/0.91,0.88,0.80,0.89,0.92,0.86,0.84,0.88,0.90,0.92,0.90/)

  quality = sum(weights * record)
  accountable = 0.70 * quality + 0.30 * minval(record)

  print *, "Accountable judgment score:", accountable

end program numerical_record_quality_model
