! numerical_adaptive_pathway_model.f90
! Compile with: gfortran numerical_adaptive_pathway_model.f90 -o numerical_adaptive_pathway_model

program numerical_adaptive_pathway_model
  implicit none

  real :: pathway_score
  logical :: trigger_hit

  pathway_score = 0.20 * 0.76 + 0.18 * 0.88 + 0.16 * 0.82 + 0.16 * 0.80 - 0.12 * 0.38 + 0.18 * 0.84
  trigger_hit = (0.70 >= 0.68) .or. (0.55 <= 0.40)

  print *, "Pathway score:", pathway_score
  print *, "Trigger hit?", trigger_hit

end program numerical_adaptive_pathway_model
