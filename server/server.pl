:- use_module(library(http/http_server)).
:- use_module(library(http/http_json)).
:- use_module(library(csv)).
:- use_module(library(lists)).

% This code is to create API server for the logic using HTTP Library
is_header(student('Student_ID', 'Attendance_percentage', 'CGPA')).

% Load CSV and assert facts
load_csv(File) :-
    csv_read_file(File, Rows, [functor(student), arity(3)]),
    exclude(is_header, Rows, DataRows),  % Skip the header row
    maplist(assert, DataRows).

% Add CORS headers to the response
add_cors_headers(Request) :-
    % Allow any origin to make a request (you can change '*' to a specific origin if needed)
    format('Access-Control-Allow-Origin: *~n'),
    format('Access-Control-Allow-Headers: Content-Type~n'),
    format('Access-Control-Allow-Methods: GET, POST, PUT, DELETE~n'),
    % If it's a pre-flight request (OPTIONS method), just send a successful response
    (   member(method(options), Request)
    ->  format('HTTP/1.1 200 OK~n')
    ;   true
    ).

% Define API handler for scholarship eligibility
student_scholarship_details(Request) :-
    add_cors_headers(Request), % Add CORS headers
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    (   student(Student_ID, Attendance, CGPA)
    ->  (   (   Attendance >= 75,
                CGPA >= 9.0
            ) ->  Eligible = true
                ;   Eligible = false
        ),
        Response = _{ 
            'eligible_for_scholarship' : Eligible,
            'student_details' : _{ 
                'Attendance' : Attendance,
                'CGPA' : CGPA
            },
            'student_id' : Student_ID
        },
        % Return JSON response
        reply_json(Response)
    ;   % If no student found
        http_reply_error(404, 'Student not found')
    ).

% Define API handler for exam eligibility
student_exam_permission(Request) :-
    add_cors_headers(Request), % Add CORS headers
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    (   student(Student_ID, Attendance, CGPA)
    ->  (   Attendance >= 75
        ->  Permitted = true
        ;   Permitted = false
        ),
        Response = _{
            'permitted_for_exam' : Permitted,
            'student_details' : _{
                'Attendance' : Attendance,
                'CGPA' : CGPA
            },
            'student_id' : Student_ID
        },
        % Return JSON response
        reply_json(Response)
    ;   % If no student found
        http_reply_error(404, 'Student not found')
    ).

% Server definition
:- http_handler('/scholarship', student_scholarship_details, []).
:- http_handler('/exam', student_exam_permission, []).

% Start the HTTP server
start_server :-
    load_csv('data.csv'), % Load CSV data
    http_server([port(5000)]).
