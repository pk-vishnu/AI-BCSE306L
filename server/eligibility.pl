:- use_module(library(csv)).

% This file is to Test PROLOG LOGIC WITH SWIPL 
is_header(student('Student_ID', 'Attendance_percentage', 'CGPA')).

load_csv(File) :-
    csv_read_file(File, Rows, [functor(student), arity(3)]),
    exclude(is_header, Rows, DataRows),  % Skip the header row
    maplist(assert, DataRows).

eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance, CGPA),
    Attendance >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance, _),
    Attendance >= 75.
