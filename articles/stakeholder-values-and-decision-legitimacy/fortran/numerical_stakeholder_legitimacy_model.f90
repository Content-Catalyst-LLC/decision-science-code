! numerical_stakeholder_legitimacy_model.f90
! Compile with: gfortran numerical_stakeholder_legitimacy_model.f90 -o numerical_stakeholder_legitimacy_model

program numerical_stakeholder_legitimacy_model
  implicit none

  real :: values(6)
  real :: weights(6)
  real :: stakeholder_score
  real :: legitimacy_index
  integer :: i

  values = (/0.68, 0.80, 0.84, 0.82, 0.86, 0.90/)
  weights = (/0.12, 0.18, 0.28, 0.14, 0.16, 0.12/)

  stakeholder_score = 0.0
  do i = 1, 6
    stakeholder_score = stakeholder_score + values(i) * weights(i)
  end do

  legitimacy_index = 0.40 * 0.82 + 0.24 * 0.89 + 0.18 * 1.0 + 0.10 * 0.76 - 0.08 * 0.26

  print *, "Stakeholder score:", stakeholder_score
  print *, "Legitimacy index:", legitimacy_index

end program numerical_stakeholder_legitimacy_model
