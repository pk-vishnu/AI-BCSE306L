import React, { useState } from "react";
import "./index.css";
const ScholarshipEligibility = () => {
  const [studentId, setStudentId] = useState("");
  const [result, setResult] = useState(null);

  const Scholarship = async () => {
    try {
      const response = await fetch(
        `http://localhost:5000/scholarship?student_id=${studentId}`
      );
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Failed to fetch data. Check backend or network." });
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h2 className="text-2xl mb-3 text-center">
        Scholarship Eligibility Checker
      </h2>

      <div className="mb-6">
        <input
          type="number"
          placeholder="Enter Student ID"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded shadow-sm mb-4"
        />
        <button
          onClick={Scholarship}
          className="w-full bg-gray-800 text-white p-3 rounded shadow hover:bg-white-800"
        >
          Check Scholarship
        </button>
      </div>

      {result && (
        <div className="p-4 border border-gray-300 rounded shadow-lg">
          {result.error ? (
            <p className="text-red-600 text-center">{result.error}</p>
          ) : (
            <div className="bg-gray-50 p-4 rounded">
              <p>
                <strong>Student ID:</strong> {result.student_id}
              </p>
              <p>
                <strong>Attendance:</strong> {result.student_details.Attendance}
                %
              </p>
              <p>
                <strong>CGPA:</strong> {result.student_details.CGPA}
              </p>
              <p>
                <strong>Eligible for Scholarship:</strong>{" "}
                {result.eligible_for_scholarship ? (
                  <p className="text-green-600 text-3xl">Eligible</p>
                ) : (
                  <p className="text-red-600 text-3xl">Not Eligible</p>
                )}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ScholarshipEligibility;
