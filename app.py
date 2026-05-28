import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Health AI",
    page_icon="❤️",
    layout="wide"
)

from db_connection import init_database
from auth import login_user, register_user
from fitbit_loader import FitbitLoader
from preprocess import DataPreprocessor
from features import FeatureEngine
from xgb_model import XGBoostModel
from IsolationForest import IsolationForestModel
from HybridRisk import HybridRiskCalculator
from userpatterns import BaselineEngine

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    font-size: 16px;
    font-weight: 600;
    background: linear-gradient(90deg,#ff416c,#ff4b2b);
    color: white;
    border: none;
}

.insight-box {
    padding: 18px;
    border-radius: 14px;
    background: #161b22;
    border-left: 5px solid #00b894;
    margin-bottom: 12px;
}

.warning-box {
    padding: 18px;
    border-radius: 14px;
    background: #161b22;
    border-left: 5px solid #ff4757;
    margin-bottom: 12px;
}

.recommend-box {
    padding: 18px;
    border-radius: 14px;
    background: #161b22;
    border-left: 5px solid #1e90ff;
    margin-bottom: 12px;
}

.glow-card {
    background: linear-gradient(145deg,#161b22,#1f2937);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 0 18px rgba(255,75,75,0.15);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================

init_database()

# =========================================================
# SESSION STATE
# =========================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'username' not in st.session_state:
    st.session_state.username = None

if 'baseline_engine' not in st.session_state:
    st.session_state.baseline_engine = BaselineEngine()

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_resource
def load_pipeline():

    loader = FitbitLoader("./data/")
    if not loader.load_all():
        return None, None, None

    preprocessor = DataPreprocessor(
        loader.get_daily(),
        loader.get_sleep(),
        loader.get_heart_rate()
    )

    raw_data = preprocessor.preprocess()

    fe = FeatureEngine(raw_data)

    feature_df = fe.create_features()

    feature_cols = fe.get_feature_columns()

    X = feature_df[feature_cols].fillna(0)

    if 'risk_label' in feature_df.columns:
        y = feature_df['risk_label']
    else:
        y = pd.Series([0] * len(feature_df))

    xgb = XGBoostModel()
    xgb.train(X, y)

    isolation = IsolationForestModel()
    isolation.train(X)

    hybrid = HybridRiskCalculator(
        xgb,
        isolation
    )

    return raw_data, hybrid, feature_cols

raw_data, hybrid_model, feature_cols = load_pipeline()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("❤️ Health AI")

    if not st.session_state.logged_in:

        mode = st.radio(
            "Choose",
            ["Login", "Create Account"]
        )

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if mode == "Login":

            if st.button("Login"):

                if username.strip() == "":
                    st.error("Enter username")

                elif password.strip() == "":
                    st.error("Enter password")

                else:

                    user_id = login_user(
                        username,
                        password
                    )

                    if user_id:

                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username

                        st.success(
                            "Login Successful"
                        )

                        st.rerun()

                    else:
                        st.error(
                            "Invalid username or password"
                        )

        else:

            st.caption(
                "Password must contain at least 6 characters"
            )

            if st.button("Create Account"):

                if username.strip() == "":
                    st.error("Username cannot be empty")

                elif password.strip() == "":
                    st.error("Password cannot be empty")

                elif len(password) < 6:
                    st.error(
                        "Password must contain at least 6 characters"
                    )

                else:

                    created = register_user(
                        username,
                        password
                    )

                    if created:

                        st.success(
                            "Account created successfully"
                        )

                        st.info(
                            "Now login using your credentials"
                        )

                    else:

                        st.error(
                            "Username already exists"
                        )

    else:

        st.success(
            f"Welcome, {st.session_state.username}"
        )

        st.caption(
            f"Logged in • {datetime.now().strftime('%d %B %Y')}"
        )

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None

            st.rerun()

# =========================================================
# MAIN APP
# =========================================================

if st.session_state.logged_in:

    st.title("❤️ AI-Powered Health Risk Prediction")

    st.caption(
        "Your Personalized AI Health Companion"
    )

    if raw_data is None:

        st.error(
            "CSV files missing inside data folder"
        )

    else:

        users = raw_data['user_id'].unique()

        patient_names = [
            f"Patient {i+1}"
            for i in range(len(users))
        ]

        selected_patient = st.selectbox(
            "Select Patient Profile",
            patient_names
        )

        selected_index = patient_names.index(
            selected_patient
        )

        selected_user = users[selected_index]

        user_data = raw_data[
            raw_data['user_id'] == selected_user
        ].sort_values('date')

        # =================================================
        # METRICS
        # =================================================

        st.subheader("📊 Health Overview")

        col1, col2, col3, col4 = st.columns(4)

        avg_hr = user_data['heart_rate'].mean()
        avg_sleep = user_data['sleep_hours'].mean()
        avg_steps = user_data['steps'].mean()
        avg_calories = user_data['calories'].mean()

        col1.metric(
            "❤️ Heart Rate",
            f"{avg_hr:.0f} bpm"
        )

        col2.metric(
            "😴 Sleep",
            f"{avg_sleep:.1f} hrs"
        )

        col3.metric(
            "👣 Daily Steps",
            f"{avg_steps:.0f}"
        )

        col4.metric(
            "🔥 Calories",
            f"{avg_calories:.0f}"
        )

        # =================================================
        # BASELINE
        # =================================================

        baseline = st.session_state.baseline_engine.compute_baseline(
            user_data.head(5),
            selected_user
        )

        st.subheader("📌 Personalized Baseline")

        base1, base2, base3 = st.columns(3)

        base1.info(
            f"❤️ Normal HR\n\n{baseline['heart_rate']:.0f} bpm"
        )

        base2.info(
            f"😴 Normal Sleep\n\n{baseline['sleep']:.1f} hrs"
        )

        base3.info(
            f"👣 Normal Activity\n\n{baseline['activity']:.0f} steps"
        )

        # =================================================
        # USER INPUT
        # =================================================

        st.subheader(
            "🩺 Enter Today's Health Data"
        )

        input1, input2, input3 = st.columns(3)

        with input1:

            manual_hr = st.number_input(
                "Heart Rate (BPM)",
                min_value=30,
                max_value=220,
                value=75
            )

        with input2:

            manual_sleep = st.slider(
                "Sleep Hours",
                0.0,
                12.0,
                7.0
            )

        with input3:

            manual_steps = st.number_input(
                "Daily Steps",
                min_value=0,
                max_value=50000,
                value=7000
            )

        # =================================================
        # ANALYSIS BUTTON
        # =================================================

        if st.button("🚀 Analyze Health Condition"):

            latest_row = user_data.iloc[-1].copy()

            latest_row['heart_rate'] = manual_hr
            latest_row['sleep_hours'] = manual_sleep
            latest_row['steps'] = manual_steps

            temp_df = pd.DataFrame([latest_row])

            fe_user = FeatureEngine(temp_df)

            user_features = fe_user.create_features()

            X_pred = user_features[
                feature_cols
            ].fillna(0)

            result = hybrid_model.calculate(X_pred)

            current_risk = 0.0

            if result is not None:

                hybrid_scores, _, _ = result

                if hybrid_scores is not None:
                    current_risk = float(
                        hybrid_scores[-1]
                    )

            # =================================================
            # RULE ENGINE
            # =================================================

            if manual_hr >= 160:
                current_risk += 0.40

            elif manual_hr >= 140:
                current_risk += 0.30

            elif manual_hr >= 120:
                current_risk += 0.20

            if manual_sleep <= 4:
                current_risk += 0.25

            elif manual_sleep <= 5:
                current_risk += 0.15

            if manual_steps <= 3000:
                current_risk += 0.15

            current_risk = max(
                0.0,
                min(current_risk, 1.0)
            )

            # =================================================
            # STATUS
            # =================================================

            if current_risk >= 0.80:

                alert_level = "🔴 CRITICAL"

            elif current_risk >= 0.60:

                alert_level = "🟠 HIGH"

            elif current_risk >= 0.35:

                alert_level = "🟡 MODERATE"

            else:

                alert_level = "🟢 LOW"

            # =================================================
            # AI SCORES
            # =================================================

            stress_score = 0

            if manual_hr > 120:
                stress_score += 35

            if manual_sleep < 5:
                stress_score += 35

            if manual_steps < 3000:
                stress_score += 20

            stress_score = min(stress_score, 100)

            recovery_score = 100 - stress_score

            wellness_score = max(
                0,
                100 - int(current_risk * 100)
            )

            # =================================================
            # MAIN OUTPUT
            # =================================================

            left, right = st.columns([1,1])

            with left:

                gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=current_risk * 100,
                    title={
                        'text': "Health Risk Score"
                    },
                    gauge={
                        'axis': {
                            'range': [0,100]
                        },
                        'bar': {
                            'color': "#ff4757"
                        },
                        'steps': [
                            {
                                'range':[0,35],
                                'color':"#2ed573"
                            },
                            {
                                'range':[35,65],
                                'color':"#ffa502"
                            },
                            {
                                'range':[65,100],
                                'color':"#ff4757"
                            }
                        ]
                    }
                ))

                gauge.update_layout(
                    template="plotly_dark",
                    height=350
                )

                st.plotly_chart(
                    gauge,
                    use_container_width=True
                )

            with right:

                st.subheader(
                    "🤖 AI Doctor Analysis"
                )

                st.markdown(
                    f"## {alert_level}"
                )

                st.metric(
                    "🧠 Stress Level",
                    f"{stress_score}%"
                )

                st.metric(
                    "⚡ Recovery Readiness",
                    f"{recovery_score}%"
                )

                st.metric(
                    "🌿 Wellness Score",
                    f"{wellness_score}%"
                )

            # =================================================
            # AI SUMMARY
            # =================================================

            st.subheader("🧠 AI Health Summary")

            if current_risk >= 0.80:

                st.markdown("""
<div class="warning-box">
Your current biometrics indicate that your body may be under severe physiological stress.
Immediate recovery and medical monitoring are recommended.
</div>
""", unsafe_allow_html=True)

            elif current_risk >= 0.50:

                st.markdown("""
<div class="recommend-box">
Moderate irregularities were detected in your current health metrics.
Better recovery and sleep consistency may improve your condition.
</div>
""", unsafe_allow_html=True)

            else:

                st.markdown("""
<div class="insight-box">
Your current health metrics appear balanced and stable.
Your recovery indicators currently look healthy.
</div>
""", unsafe_allow_html=True)

            # =================================================
            # EXTRA INSIGHTS
            # =================================================

            st.subheader("🧠 Smart Health Insights")

            if manual_hr > baseline['heart_rate'] + 25:

                st.markdown(f"""
<div class="warning-box">
❤️ Your heart rate is approximately {manual_hr - baseline['heart_rate']:.0f} BPM above your usual baseline.
This may indicate stress, fatigue, dehydration or overexertion.
</div>
""", unsafe_allow_html=True)

            else:

                st.markdown("""
<div class="insight-box">
❤️ Your cardiovascular activity currently appears relatively stable.
</div>
""", unsafe_allow_html=True)

            if manual_sleep < baseline['sleep'] - 1.5:

                st.markdown("""
<div class="warning-box">
😴 Your sleep duration appears significantly lower than your normal recovery pattern.
Reduced sleep may affect concentration, mood and body recovery.
</div>
""", unsafe_allow_html=True)

            else:

                st.markdown("""
<div class="insight-box">
😴 Your sleep duration currently supports healthy body recovery.
</div>
""", unsafe_allow_html=True)

            if manual_steps < 3000:

                st.markdown("""
<div class="warning-box">
👣 Reduced physical activity was detected today.
Long periods of inactivity may increase fatigue and sluggishness.
</div>
""", unsafe_allow_html=True)

            elif manual_steps > 25000:

                st.markdown("""
<div class="recommend-box">
🔥 Very high physical activity was detected today.
Hydration and muscle recovery are important after intense movement.
</div>
""", unsafe_allow_html=True)

            else:

                st.markdown("""
<div class="insight-box">
👣 Your movement level currently supports healthy circulation and energy balance.
</div>
""", unsafe_allow_html=True)

            # =================================================
            # BODY STATE ANALYSIS
            # =================================================

            st.subheader("🩺 Body State Analysis")

            body_col1, body_col2, body_col3 = st.columns(3)

            with body_col1:

                if stress_score >= 70:
                    st.error("⚠️ High Body Stress")

                elif stress_score >= 40:
                    st.warning("⚠️ Moderate Body Stress")

                else:
                    st.success("✅ Balanced Stress Level")

            with body_col2:

                if recovery_score >= 70:
                    st.success("⚡ Strong Recovery")

                elif recovery_score >= 40:
                    st.warning("⚡ Average Recovery")

                else:
                    st.error("⚡ Poor Recovery")

            with body_col3:

                if wellness_score >= 70:
                    st.success("🌿 Good Wellness")

                elif wellness_score >= 40:
                    st.warning("🌿 Average Wellness")

                else:
                    st.error("🌿 Low Wellness")

            # =================================================
            # RECOMMENDATIONS
            # =================================================

            st.subheader("💡 Personalized Recommendations")

            recommendations = []

            if manual_sleep < 6:
                recommendations.append(
                    "Improve sleep consistency and aim for 7-8 hours of recovery sleep."
                )

            if manual_hr > 120:
                recommendations.append(
                    "Reduce stress and avoid excessive physical strain temporarily."
                )

            if manual_steps < 4000:
                recommendations.append(
                    "Increase light walking and physical movement gradually."
                )

            if manual_steps > 25000:
                recommendations.append(
                    "Hydrate properly and allow muscle recovery after intense activity."
                )

            if len(recommendations) == 0:
                recommendations.append(
                    "Continue maintaining your healthy routine and balanced lifestyle."
                )

            for item in recommendations:

                st.markdown(f"""
<div class="recommend-box">
✅ {item}
</div>
""", unsafe_allow_html=True)

            # =================================================
            # VISUAL ANALYTICS
            # =================================================

            st.subheader("📊 Health Analytics")

            chart1, chart2 = st.columns(2)

            with chart1:

                pie_chart = go.Figure(
                    data=[
                        go.Pie(
                            labels=[
                                "Risk",
                                "Healthy"
                            ],
                            values=[
                                int(current_risk * 100),
                                100 - int(current_risk * 100)
                            ],
                            hole=0.5
                        )
                    ]
                )

                pie_chart.update_layout(
                    template="plotly_dark",
                    height=350
                )

                st.plotly_chart(
                    pie_chart,
                    use_container_width=True
                )

            with chart2:

                radar_chart = go.Figure()

                radar_chart.add_trace(
                    go.Scatterpolar(
                        r=[
                            max(0, 100 - abs(manual_hr - 75)),
                            manual_sleep * 10,
                            min(manual_steps / 100, 100),
                            recovery_score
                        ],
                        theta=[
                            'Heart',
                            'Sleep',
                            'Activity',
                            'Recovery'
                        ],
                        fill='toself'
                    )
                )

                radar_chart.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0,100]
                        )
                    ),
                    template="plotly_dark",
                    height=350
                )

                st.plotly_chart(
                    radar_chart,
                    use_container_width=True
                )

            # =================================================
            # TRENDS
            # =================================================

            st.subheader("📈 Recent Health Trends")

            trend_df = user_data.tail(10)

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=trend_df['date'],
                    y=trend_df['heart_rate'],
                    mode='lines+markers',
                    name='Heart Rate'
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=trend_df['date'],
                    y=trend_df['sleep_hours'],
                    mode='lines+markers',
                    name='Sleep Hours'
                )
            )

            fig.update_layout(
                template="plotly_dark",
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

else:

    st.title(
        "❤️ AI-Powered Health Monitoring System"
    )

    st.markdown("""
### Smart Features

- Hybrid Machine Learning Prediction
- AI Doctor-like Insights
- Personalized Recommendations
- Stress & Recovery Analysis
- Wellness Scoring
- Health Analytics Dashboard
- Interactive Monitoring
- Modern Beautiful UI

Login or create an account from the sidebar to continue.
""")
