import requests
import streamlit as st

DEV_API = "http://127.0.0.1:8000/predict"
PROD_API = "https://predictingforjay.azurewebsites.net/api/predict"


def fetch_prediction(payload: dict) -> dict:
    """Call the prediction API and return the JSON response"""
    response = requests.post(DEV_API, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


def fetch_prediction_from_production(params: dict) -> dict:
    """Call the production API and return the response.

    Our serverless function doesnt support JSON in or out
    Plus we need to increase the timeout for cold starts.
    """
    url = PROD_API + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()

# Page Configuration
st.set_page_config(page_title="Telco Churn Predictor", page_icon="📊", layout="wide")

# Custom styling: subtle page gradient and card-like main container
st.markdown(
        """
        <style>
            html, body, .stApp {
                background: linear-gradient(180deg, #f7fbff 0%, #eef3ff 100%) !important;
            }
            .stApp > div[data-testid="stAppViewContainer"] > div:first-child {
                background: rgba(255,255,255,0.9) !important;
                border-radius: 12px;
                padding: 1.0rem 1.25rem !important;
                box-shadow: 0 8px 30px rgba(12, 38, 63, 0.08) !important;
            }
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg,#f6f9ff, #ffffff) !important;
                border-radius: 8px;
            }
            .css-1offfwp { /* small fallback for some streamlit versions */
                background: transparent;
            }
            .stButton>button {
                background: linear-gradient(90deg,#4f46e5,#06b6d4) !important;
                color: white !important;
                border: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
)

st.title("📊 Telco Churn Prediction Dashboard")
st.write("Analyze customer churn risk and receive retention recommendations.")

st.divider()

# Input Section with Form
st.subheader("📋 Customer Profile")

with st.form("prediction_form", border=True):
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Subscription & Charges**")
        
        tenure = st.slider(
            "Customer Tenure",
            min_value=0,
            max_value=120,
            value=24,
            step=1,
            help="Months the customer has been with your company",
            label_visibility="visible"
        )
        
        monthly = st.slider(
            "Monthly Charges",
            min_value=0,
            max_value=1000,
            value=70,
            step=5,
            help="Monthly service charges in dollars",
            label_visibility="visible",
            format="$%d"
        )

    with col2:
        st.write("**Services & Support**")
        
        techsupport = st.toggle(
            "Tech Support",
            value=False,
            help="Customer has subscribed to technical support"
        )

    st.divider()
    
    # Display derived metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Annual Charges", f"${monthly * 12:.0f}")
    with col2:
        st.metric("Tenure Duration", f"{tenure} months")
    with col3:
        st.metric("Tech Support", "✅ Active" if techsupport else "❌ Inactive")
    
    # Submit button
    submitted = st.form_submit_button(
        "🔮 Predict Churn Risk",
        use_container_width=True,
        type="primary"
    )

st.divider()

payload = {
    "tenure": float(tenure),
    "monthly": float(monthly),
    "techsupport": float(techsupport),
}

# Make Prediction only on form submission
if submitted:
    try:
        with st.spinner("Analyzing customer profile..."):
            data = fetch_prediction(payload)
        
        prediction = data.get("prediction", 0)
        churn_percentage = prediction * 100

        # Result Section
        st.subheader("🎯 Prediction Results")
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            # Color code based on risk level
            if prediction < 0.3:
                color = "🟢"
                risk_level = "Low Risk"
                emoji = "✅"
            elif prediction < 0.6:
                color = "🟡"
                risk_level = "Medium Risk"
                emoji = "⚠️"
            else:
                color = "🔴"
                risk_level = "High Risk"
                emoji = "🚨"
            
            st.metric("Churn Probability", f"{churn_percentage:.1f}%", delta=f"{emoji} {risk_level}")
        
        with col2:
            st.metric("Risk Assessment", risk_level, delta=color)
    
        with col3:
            satisfaction_score = (1 - prediction) * 100
            st.metric("Satisfaction Score", f"{satisfaction_score:.0f}%")
    
        # Progress Bar
        st.progress(min(prediction, 1.0), text=f"Churn Risk: {churn_percentage:.1f}%")
    
        # Insights & Recommendations
        st.divider()
        st.subheader("💡 Insights & Recommendations")
    
        if prediction < 0.3:
            st.success(f"✅ **Low Risk** - This customer is satisfied with {tenure} months tenure.")
            st.write("""
            **Recommended Actions:**
            - Continue current service levels
            - Offer loyalty rewards program
            - Schedule periodic check-ins
            """)
        elif prediction < 0.6:
            st.warning(f"⚠️ **Medium Risk** - Moderate churn probability detected.")
            st.write("""
            **Recommended Actions:**
            - Review account for service complaints
            - Offer service bundle upgrades
            - Consider promotional discounts
            - Enhance tech support offerings
            """)
        else:
            st.error(f"🚨 **High Risk** - Immediate action recommended!")
            st.write("""
            **Recommended Actions:**
            - **Priority:** Schedule customer success call
            - Offer significant retention discount
            - Provide personalized service recommendations
            - Assign dedicated account manager
            - Consider service bundle customization
            """)
    
        # Advanced Details
        with st.expander("📊 Detailed Analysis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Input Parameters")
                st.write(f"**Tenure:** {tenure} months ({tenure/12:.1f} years)")
                st.write(f"**Monthly Charges:** ${monthly:.2f}")
                st.write(f"**Annual Charges:** ${monthly*12:.2f}")
                st.write(f"**Tech Support:** {'Yes' if techsupport else 'No'}")
            
            with col2:
                st.subheader("Model Prediction")
                st.json(data)
    
        # Comparison insights
        st.divider()
        st.subheader("📈 Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if tenure < 12:
                st.info("ℹ️ **New Customer** - High early churn risk. Focus on onboarding quality.")
            elif tenure > 48:
                st.info("ℹ️ **Loyal Customer** - Long-term relationship. Consider upsell opportunities.")
        
        with col2:
            if monthly > 200:
                st.info("ℹ️ **High-value Customer** - Premium services. Ensure high service quality.")
            elif monthly < 50:
                st.info("ℹ️ **Budget-conscious Customer** - Price-sensitive. Monitor for better offers.")

    except requests.RequestException as e:
        st.error(f"❌ Error calling API: {e}")
        st.info("Make sure the API server is running on http://127.0.0.1:8000")
else:
    st.info("👆 Adjust customer profile above and click **Predict Churn Risk** to analyze")
