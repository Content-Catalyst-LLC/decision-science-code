! numerical_ai_support_model.f90
! Compile with: gfortran numerical_ai_support_model.f90 -o numerical_ai_support_model

program numerical_ai_support_model
  implicit none

  real :: justified_reliance
  real :: automation_bias

  justified_reliance = max(0.0, min(1.0, 0.35 * 0.82 + 0.35 * 0.78 - 0.16 * 0.54 - 0.14 * 0.36))
  automation_bias = 0.78 - justified_reliance

  print *, "Justified model reliance:", justified_reliance
  print *, "Automation bias:", automation_bias

end program numerical_ai_support_model
