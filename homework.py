from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector 
from mysql.connector import Error

app = Flask(__name__)
app.json.sort_keys = False 
ma = Marshmallow(app)

db_name = "fitness_tracker"
user = "root"
password = "Hammond45!"
host = "Localhost"

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database = db_name, 
            user = user,
            password = password,
            host = host
        )
        if conn.is_connected():
            return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None
    
class MemberSchema(ma.Schema):
    member_name = fields.String(required = True)
    member_email = fields.String(required = True)
    member_phone = fields.String(required = True)

    class Meta:
        fields = ("member_id", "member_name", "member_email", "member_phone")
    
member_schema = MemberSchema()        
members_schema = MemberSchema(many = True)

@app.route('/members', methods = ['GET'])
def get_members():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    query = "SELECT * FROM Members"
    cursor.execute(query)
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return members_schema.jsonify(members)

@app.route('/members', methods = ['POST'])
def add_member():
    member_info = member_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    member_name = member_info['member_name']
    member_email = member_info['member_email']
    member_phone = member_info['member_phone']
    new_member = (member_name, member_email, member_phone)
    query = "INSERT INTO Members(member_name, member_email, member_phone) VALUES (%s, %s, %s)"
    cursor.execute(query, new_member)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "New member was added successfully"}), 201 

@app.route("/members/<int:member_id>", methods = ["PUT"])
def update_member(member_id):
    member_info = member_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    member_name = member_info["member_name"]
    member_email = member_info["member_email"]
    member_phone = member_info["member_phone"]
    updated_member = (member_name, member_email, member_phone, member_id)
    query = "UPDATE Members SET member_name = %s, member_email = %s, member_phone = %s WHERE member_id = %s"
    cursor.execute(query, updated_member)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': "Member was updated successfully"}), 200

@app.route('/members/<int:member_id>', methods = ["DELETE"])
def delete_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Members WHERE member_id = %s"
    cursor.execute(query, (member_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Member successfully deleted!"}), 200

class WorkoutSessionSchema(ma.Schema):
    cardio_focus = fields.String(required = True)
    lift_focus = fields.String(required = True)
    date = fields.Date(required = True)
    member_id = fields.Int(required = True)

    class Meta:
        fields = ("workout_id", "cardio_focus", "lift_focus", "date", "member_id")
    
workout_session_schema = WorkoutSessionSchema()        
workout_sessions_schema = WorkoutSessionSchema(many = True)

@app.route('/workout_sessions', methods = ['GET'])
def get_workout_sessions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    query = "SELECT * FROM Workout_Sessions"
    cursor.execute(query)
    workout_sessions = cursor.fetchall()
    print(workout_sessions)
    cursor.close()
    conn.close()
    return workout_sessions_schema.jsonify(workout_sessions)

@app.route('/workout_sessions', methods = ['POST'])
def add_workout_session():
    workout_session_info = workout_session_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    cardio_focus = workout_session_info['cardio_focus']
    lift_focus = workout_session_info['lift_focus']
    date = workout_session_info['date']
    member_id = workout_session_info["member_id"]
    new_workout_session = (cardio_focus, lift_focus, date, member_id)
    query = "INSERT INTO Workout_Sessions(cardio_focus, lift_focus, date, member_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, new_workout_session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "New Workout Session was added successfully"}), 201 

@app.route("/workout_sessions/<int:workout_id>", methods = ["PUT"])
def update_workout_session(workout_id):
    workout_session_info = workout_session_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    cardio_focus = workout_session_info['cardio_focus']
    lift_focus = workout_session_info['lift_focus']
    date = workout_session_info['date']
    member_id = workout_session_info["member_id"]
    updated_workout_session = (cardio_focus, lift_focus, date, member_id, workout_id)
    query = "UPDATE Workout_Sessions SET cardio_focus = %s, lift_focus = %s, date = %s, member_id = %s WHERE workout_id = %s"
    cursor.execute(query, updated_workout_session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': "Workout Session was updated successfully"}), 200

@app.route('/workout_sessions/<int:workout_id>', methods = ["DELETE"])
def delete_workout_session(workout_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Workout_Sessions WHERE workout_id = %s"
    cursor.execute(query, (workout_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Workout Session successfully deleted!"}), 200

if __name__ == "__main__":
    app.run(debug=True, port = 5000) 