from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

# Demo Users
users = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "manager": {
        "password": "manager123",
        "role": "manager"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}


# ---------- Login ----------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    if username not in users:
        return jsonify({
            "message": "Invalid User"
        }), 401

    if users[username]["password"] != password:
        return jsonify({
            "message": "Invalid Password"
        }), 401

    token = create_access_token(
        identity={
            "username": username,
            "role": users[username]["role"]
        }
    )

    return jsonify({
        "access_token": token
    })


# ---------- Admin Only ----------
@app.route("/admin")
@jwt_required()
def admin():

    user = get_jwt_identity()

    if user["role"] != "admin":

        return jsonify({
            "message": "Access Denied"
        }), 403

    return jsonify({
        "message": "Welcome Admin"
    })


# ---------- Manager ----------
@app.route("/manager")
@jwt_required()
def manager():

    user = get_jwt_identity()

    if user["role"] not in [
        "admin",
        "manager"
    ]:

        return jsonify({
            "message": "Access Denied"
        }), 403

    return jsonify({
        "message": "Manager Dashboard"
    })


# ---------- User ----------
@app.route("/profile")
@jwt_required()
def profile():

    return jsonify(
        get_jwt_identity()
    )


@app.route("/")
def home():

    return jsonify({
        "message": "RBAC API"
    })


if __name__ == "__main__":

    app.run(debug=True)
