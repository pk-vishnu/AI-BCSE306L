from flask import Flask, jsonify, request
from flask_cors import CORS


from pyswip import Prolog
#Flask server implementation for API (Not used for DA implementation)
app = Flask(__name__)
CORS(app)
prolog = Prolog()
prolog.consult("eligibility.pl")  
list(prolog.query("load_csv('data.csv')."))

@app.route("/students", methods=["GET"])
def get_students():
    students = list(prolog.query("student(ID, Attendance, CGPA)."))
    return jsonify(students)

@app.route("/scholarship/<int:student_id>", methods=["GET"])
def check_scholarship(student_id):
    try:
        student_details = list(prolog.query(f"student({student_id}, Attendance, CGPA)."))
        if not student_details:
            return jsonify({"error": "Student not found"}), 404
        eligible_result = list(prolog.query(f"eligible_for_scholarship({student_id})."))
        eligible = bool(eligible_result)
        student = student_details[0]
        return jsonify({
            "student_id": student_id,
            "student_details": {
                "Attendance": student["Attendance"],
                "CGPA": student["CGPA"]
            },
            "eligible_for_scholarship": eligible
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/exam/<int:student_id>", methods=["GET"])
def check_exam_permission(student_id):
    try:
        student_details = list(prolog.query(f"student({student_id}, Attendance, CGPA)."))
        if not student_details:
            return jsonify({"error": "Student not found"}), 404
    
        permitted_result = list(prolog.query(f"permitted_for_exam({student_id})."))
        permitted = bool(permitted_result)
        
        student = student_details[0]
        return jsonify({
            "student_id": student_id,
            "student_details": {
                "Attendance": student["Attendance"],
                "CGPA": student["CGPA"]
            },
            "permitted_for_exam": permitted
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
