import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


def load_schemes_dataframe(db_conn=None, csv_path="schemes_data.csv"):
    """
    Loads schemes into a Pandas DataFrame from MySQL if connected,
    otherwise falls back seamlessly to the local CSV dataset.
    """
    if db_conn is not None:
        try:
            query = "SELECT * FROM schemes"
            df = pd.read_sql(query, db_conn)
            if not df.empty:
                return df
        except Exception as e:
            print(f"[INFO] Falling back to CSV dataset due to DB read notice: {e}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_csv_path = os.path.join(base_dir, csv_path)
    return pd.read_csv(full_csv_path)


def check_rule_eligibility(row, user_profile):
    """
    Rule-Based Eligibility Engine:
    Evaluates strict criteria (Age, Annual Income, Occupation, Location, Social Category).
    Returns (is_eligible: bool, matched_reasons: list[str]).
    """
    reasons = []

    # 1. Age Rule
    if not (row["min_age"] <= user_profile["age"] <= row["max_age"]):
        return False, []
    reasons.append(f"Age {user_profile['age']} fits ({row['min_age']}-{row['max_age']} yrs)")

    # 2. Income Rule
    if user_profile["income"] > float(row["max_income"]):
        return False, []
    reasons.append(f"Income Rs.{int(user_profile['income']):,} <= limit Rs.{int(row['max_income']):,}")

    # 3. Occupation Rule
    allowed_occ = [x.strip().lower() for x in str(row["allowed_occupations"]).split(",")]
    user_occ = user_profile["occupation"].strip().lower()
    if "all" not in allowed_occ and user_occ not in allowed_occ:
        return False, []
    if "all" not in allowed_occ:
        reasons.append(f"Targeted for {user_profile['occupation']}")

    # 4. Location Rule
    allowed_loc = [x.strip().lower() for x in str(row["allowed_locations"]).split(",")]
    user_loc = user_profile["location"].strip().lower()
    if "all" not in allowed_loc and user_loc not in allowed_loc:
        return False, []
    if "all" not in allowed_loc:
        reasons.append(f"Available in {user_profile['location']} areas")

    # 5. Social Category Rule
    allowed_cat = [x.strip().lower() for x in str(row["allowed_social_categories"]).split(",")]
    user_cat = user_profile["category"].strip().lower()
    if "all" not in allowed_cat and user_cat not in allowed_cat:
        return False, []
    if "all" not in allowed_cat:
        reasons.append(f"Special provision for {user_profile['category']} category")

    return True, reasons


def get_eligible_and_recommended_schemes(user_profile, db_conn=None):
    """
    Hybrid Pipeline:
    Step 1: Pandas data loading & cleaning.
    Step 2: Rule-Based filtering for hard eligibility constraints.
    Step 3: Scikit-learn TF-IDF + Cosine Similarity & Numeric Feature Scoring to rank
            best-fit schemes for the user's profile and needs.
    """
    df = load_schemes_dataframe(db_conn=db_conn)
    df = df.fillna("All")

    # Build user text query for Scikit-learn TF-IDF semantic similarity
    user_text = (
        f"{user_profile['occupation']} {user_profile['location']} "
        f"{user_profile['category']} {user_profile.get('interest', '')} "
        f"welfare financial assistance support"
    )

    # Combine scheme textual attributes
    scheme_corpus = (
        df["scheme_name"].astype(str) + " " +
        df["category_tag"].astype(str) + " " +
        df["allowed_occupations"].astype(str) + " " +
        df["allowed_social_categories"].astype(str) + " " +
        df["description"].astype(str) + " " +
        df["benefits"].astype(str)
    ).tolist()

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(scheme_corpus + [user_text])
    cosine_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # Numeric proximity score using MinMaxScaler (how closely user income/age aligns)
    scaler = MinMaxScaler()
    income_ratio = np.clip(1.0 - (user_profile["income"] / (df["max_income"].astype(float) + 1.0)), 0, 1)
    norm_income_score = scaler.fit_transform(income_ratio.values.reshape(-1, 1)).flatten()

    df["ml_similarity"] = cosine_scores
    df["income_fit"] = norm_income_score

    eligible_results = []
    other_recommendations = []

    for idx, row in df.iterrows():
        is_eligible, reasons = check_rule_eligibility(row, user_profile)

        # Hybrid relevance score (0 to 100%)
        hybrid_score = round(float((0.65 * row["ml_similarity"] + 0.35 * row["income_fit"]) * 100), 1)
        # Boost display confidence for exact rule matches
        display_score = min(99.0, round(55.0 + hybrid_score * 0.45, 1)) if is_eligible else round(hybrid_score, 1)

        scheme_item = {
            "scheme_id": int(row["scheme_id"]),
            "scheme_name": row["scheme_name"],
            "category_tag": row["category_tag"],
            "benefits": row["benefits"],
            "description": row["description"],
            "official_link": row["official_link"],
            "max_income": int(row["max_income"]),
            "age_range": f"{int(row['min_age'])} - {int(row['max_age'])} yrs",
            "match_score": display_score,
            "reasons": reasons,
        }

        if is_eligible:
            eligible_results.append(scheme_item)
        elif hybrid_score >= 15.0:
            other_recommendations.append(scheme_item)

    # Sort by ML hybrid match score descending
    eligible_results.sort(key=lambda x: x["match_score"], reverse=True)
    other_recommendations.sort(key=lambda x: x["match_score"], reverse=True)

    return eligible_results, other_recommendations[:3]
