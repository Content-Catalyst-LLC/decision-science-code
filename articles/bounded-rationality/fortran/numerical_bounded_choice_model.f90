! numerical_bounded_choice_model.f90
! Compile with: gfortran numerical_bounded_choice_model.f90 -o numerical_bounded_choice_model

program numerical_bounded_choice_model
  implicit none

  real, dimension(5) :: values
  real :: aspiration
  integer :: i
  logical :: found

  values = (/0.58, 0.71, 0.82, 0.77, 0.91/)
  aspiration = 0.75
  found = .false.

  do i = 1, 5
    if (values(i) >= aspiration .and. .not. found) then
      print *, "Satisficing option:", i
      print *, "Value:", values(i)
      found = .true.
    end if
  end do

  if (.not. found) then
    print *, "No option satisfies aspiration."
  end if

end program numerical_bounded_choice_model
