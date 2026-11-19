import os
from flask import Flask, render_template, request
import mysql.connector
from dotenv import load_dotenv
from recommender import get_eligible_and_recommended_schemes, load_schemes_dataframe

load_dotenv()

# IMPORTANT: All files live in the same single root folder (no nested templates/ or static/ folders)
app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "yojana_sarthi_dev_key")


def get_mysql_connection():
    """Creates a MySQL connection using environment variables. Returns None if DB is offline."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "yojana_sarthi_db"),
            connection_timeout=3,
        )
        return conn
    except Exception:
        return None


def log_user_query_to_mysql(conn, profile, matched_count):
    """Saves citizen eligibility check analytics into MySQL user_queries table."""
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO user_queries (full_name, age, income, occupation, location, social_category, matched_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            profile.get("full_name", "Citizen"),
            profile["age"],
            profile["income"],
            profile["occupation"],
            profile["location"],
            profile["category"],
            matched_count,
        ))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"[INFO] Could not log query to MySQL: {e}")


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_mysql_connection()
    db_status = "Connected to MySQL" if conn is not None else "CSV Fallback Mode (MySQL Offline)"

    eligible_schemes = None
    related_schemes = None
    user_profile = None
    error_msg = None

    if request.method == "POST":
        try:
            full_name = request.form.get("full_name", "").strip() or "Citizen"
            age = int(request.form.get("age", 0))
            income = float(request.form.get("income", 0))
            occupation = request.form.get("occupation", "All").strip()
            location = request.form.get("location", "All").strip()
            category = request.form.get("category", "General").strip()
            interest = request.form.get("interest", "").strip()

            if age < 0 or age > 120 or income < 0:
                error_msg = "Please enter a valid age (0-120) and non-negative annual income."
            else:
                user_profile = {
                    "full_name": full_name,
                    "age": age,
                    "income": income,
                    "occupation": occupation,
                    "location": location,
                    "category": category,
                    "interest": interest,
                }
                eligible_schemes, related_schemes = get_eligible_and_recommended_schemes(
                    user_profile, db_conn=conn
                )
                log_user_query_to_mysql(conn, user_profile, len(eligible_schemes))
        except ValueError:
            error_msg = "Invalid numeric input. Please check Age and Income fields."

    # Load all schemes for the Browse All tab
    all_schemes_df = load_schemes_dataframe(db_conn=conn)
    all_schemes = all_schemes_df.to_dict(orient="records")

    if conn is not None:
        conn.close()

    return render_template(
        "index.html",
        db_status=db_status,
        eligible_schemes=eligible_schemes,
        related_schemes=related_schemes,
        all_schemes=all_schemes,
        user_profile=user_profile,
        error_msg=error_msg,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
