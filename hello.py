from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:barbie@localhost/students_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    unit1 = db.Column(db.Integer, nullable=False)
    unit2 = db.Column(db.Integer, nullable=False)
    unit3 = db.Column(db.Integer, nullable=False)
    unit4 = db.Column(db.Integer, nullable=False)
    unit5 = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(2), nullable=False)

with app.app_context():
    db.create_all()
#route to home page
@app.route("/", methods=["GET"])
def home():
    return render_template("dashboard.html",students=Student.query.all())

# Route to Show Analysis of All Students
@app.route("/students_analysis", methods=["GET"])
def students_analysis():
    students = Student.query.all()

    if not students:
        return jsonify({"message": "No students found."}), 404

    study_materials = {
        "mechanics": "https://www.khanacademy.org/science/physics/mechanics",
        "thermodynamics": "https://www.khanacademy.org/science/physics/thermodynamics",
        "electromagnetism": "https://www.khanacademy.org/science/physics/electromagnetism",
        "optics": "https://www.khanacademy.org/science/physics/light-and-optics",
        "electricity": "https://www.khanacademy.org/science/physics/circuits",
    }

    student_data = []
    for student in students:
        scores = {
            "mechanics": student.unit1,
            "thermodynamics": student.unit2,
            "electromagnetism": student.unit3,
            "optics": student.unit4,
            "electricity": student.unit5,
        }

        weakest_unit = min(scores, key=scores.get)
        suggestion = study_materials.get(weakest_unit, "No study material available.")

        student_data.append({
            "Student ID": student.student_id,
            "Student Name": student.student_name,
            "Scores": scores,
            "Weakest Unit": weakest_unit.capitalize(),
            "Suggested Study Material": suggestion
        })

    return render_template("students_analysis.html", students=student_data)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
