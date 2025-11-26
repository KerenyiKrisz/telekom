# Streamlit Input Components Best Practices for Customer Churn Prediction

## Executive Summary
For a customer churn prediction dashboard, the optimal approach combines **semantic clarity** (using component types that match the data type), **cognitive load reduction** (grouping related inputs), and **business context** (making predictions feel immediate and reliable).

---

## 1. Input Widgets by Data Type

### A. Continuous Numeric Data (Tenure, Charges)

#### ✅ **RECOMMENDED: `st.slider()` for bounded ranges**
```python
tenure = st.slider(
    "Tenure (months)",
    min_value=0,
    max_value=72,
    value=24,
    step=1,
    help="Years with company (0-6 years)"
)
```

**Advantages for business dashboards:**
- **Visual feedback**: Users see the range context immediately
- **Prevents outliers**: Hard boundaries prevent invalid inputs
- **Exploration friendly**: Dragging encourages "what-if" scenarios
- **Mobile-friendly**: Touch-friendly on tablets used by support teams

**Trade-offs:**
- Poor for entering precise values (hard to hit exact number)
- Takes more screen space
- For tenure, 72-month maximum is realistic business constraint

#### 🟡 **ALTERNATIVE: `st.number_input()` when precision matters**
```python
monthly_charges = st.number_input(
    "Monthly Charges ($)",
    min_value=0.0,
    max_value=120.0,
    step=0.01,
    value=50.0,
    format="$%.2f"
)
```

**When to use:**
- Customer services with precise billing (e.g., $65.43)
- When users know exact value and entering is faster than sliding
- For data import workflows

**Disadvantages for churn prediction:**
- Less intuitive for exploratory "what-if" analysis
- Doesn't communicate range constraints visually
- Higher cognitive load to understand valid ranges

---

### B. Boolean/Service Status Data (Tech Support, Online Security, etc.)

#### ✅ **RECOMMENDED: `st.toggle()` for single binary service**
```python
tech_support = st.toggle(
    "Tech Support Active",
    value=False,
    help="Customer has tech support subscription"
)
```

**Advantages:**
- **Immediate visual state**: ON/OFF is crystal clear
- **Accessibility**: Larger touch target than checkbox
- **Modern UX**: Matches contemporary app patterns
- **Clean visual**: Minimal screen clutter

**When to use:**
- Individual service toggles
- Admin dashboards where on/off is primary concern
- Forms with one boolean per row

#### 🟡 **ACCEPTABLE: `st.checkbox()` for multiple services**
```python
tech_support = st.checkbox("Tech Support", value=False)
online_security = st.checkbox("Online Security", value=True)
phone_service = st.checkbox("Phone Service", value=False)
```

**Advantages:**
- Traditional, universally understood
- Good for multiple related booleans in close proximity
- Works well in compact layouts

**Disadvantages:**
- Smaller visual state indicator than toggle
- Feels dated in modern dashboards
- Checkboxes grouped vertically can feel cluttered

#### ✅ **RECOMMENDED for service categories: `st.select_slider()` or custom layout**
```python
# Better: Present as readable service group
with st.container(border=True):
    st.subheader("📱 Services")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tech_support = st.toggle("Tech Support")
    with col2:
        online_security = st.toggle("Online Security")
    with col3:
        phone_service = st.toggle("Phone Service")
```

**Why:**
- Visual grouping creates semantic meaning
- Border/container distinguishes service section
- Emoji + text provides business context
- Horizontal layout reduces vertical scrolling

---

### C. Categorical Data (Contract Type, Internet Service, etc.)

#### ✅ **RECOMMENDED: `st.selectbox()` for 3-6 options**
```python
contract_type = st.selectbox(
    "Contract Type",
    options=["Month-to-month", "One year", "Two year"],
    help="Current contract duration"
)
```

**Advantages:**
- **Compact**: Only shows selected value until clicked
- **Mobile-friendly**: Dropdown is touch-friendly
- **Semantic**: Clear that this is a choice
- **Predictable**: Single column layout

**When to use:**
- 3-6 clearly different options
- Dropdown is hidden by default (saves space)
- Options have natural hierarchy or ordering

#### 🟡 **ALTERNATIVE: `st.radio()` for obvious choices**
```python
internet_service = st.radio(
    "Internet Service Type",
    options=["DSL", "Fiber Optic", "None"],
    horizontal=True
)
```

**Advantages:**
- All options visible without clicking
- Cannot miss an option
- Clear at-a-glance what's available

**Disadvantages:**
- Takes more space (not all options fit horizontally on mobile)
- Radio buttons feel dated in modern Streamlit
- Better reserved for important decisions

#### ❌ **AVOID for churn dashboards: `st.multiselect()` for single choice**
```python
# DON'T DO THIS
services = st.multiselect("Select services", options=[...])
```

**Why avoid:**
- Confuses users (they expect to select multiple)
- Adds complexity for single-choice scenarios
- Takes up space

---

## 2. Form Patterns: Individual vs. Grouped Inputs

### ✅ **RECOMMENDED: `st.form()` for customer data entry**

```python
with st.form("customer_input_form"):
    st.subheader("📋 Customer Information")
    
    col1, col2 = st.columns(2)
    with col1:
        tenure = st.slider("Tenure (months)", 0, 72, 24)
        monthly = st.number_input("Monthly Charges ($)", 0.0, 120.0, 50.0)
    
    with col2:
        contract = st.selectbox("Contract Type", 
            ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", 
            ["DSL", "Fiber Optic", "No"])
    
    services_header = st.subheader("📱 Services")
    col1, col2, col3 = st.columns(3)
    with col1:
        tech_support = st.toggle("Tech Support", value=False)
    with col2:
        online_security = st.toggle("Online Security", value=False)
    with col3:
        backup_service = st.toggle("Backup Service", value=False)
    
    submitted = st.form_submit_button("🔮 Predict Churn Risk")

if submitted:
    # Make single API call with all data
    prediction = fetch_prediction({
        "tenure": tenure,
        "monthly": monthly,
        "contract": contract,
        "internet": internet,
        "tech_support": tech_support,
        "online_security": online_security,
        "backup_service": backup_service
    })
```

**Advantages:**
- **Single API call**: Reduces latency and server load
- **Atomic transactions**: All-or-nothing data consistency
- **User expectation**: "Submit" button signals form-like behavior
- **Performance**: Streamlit re-runs only on submit, not per input change

**Business dashboard benefits:**
- Support teams feel confident they've entered complete data
- No premature predictions while they're still filling form
- Protects API from excessive calls
- Better for batch processing customer lists

---

### 🟡 **ALTERNATIVE: Reactive inputs (no form)**

```python
# Individual inputs without form (auto-predict on each change)
tenure = st.slider("Tenure (months)", 0, 72, 24)
monthly = st.number_input("Monthly Charges ($)", 0.0, 120.0, 50.0)
tech_support = st.toggle("Tech Support", value=False)

# Prediction happens immediately on any change
prediction = fetch_prediction({...})
```

**When to use:**
- Exploratory dashboards where "what-if" is the goal
- Lightweight predictions with fast API response
- Single customer analysis (not batch processing)

**Disadvantages for business use:**
- Multiple API calls per user interaction
- Can feel "laggy" with slow API
- Higher server load
- Users feel pressured by real-time feedback

---

## 3. Recommended Component Mapping for Telco Churn Data

### Customer Demographics
| Data | Type | Widget | Reasoning |
|------|------|--------|-----------|
| Tenure | Continuous (0-72 mo) | `st.slider()` | Bounded range, natural max is 72mo |
| Monthly Charges | Continuous ($) | `st.slider()` | Range-based; most churn patterns fit $18-120 |
| Total Charges | Continuous ($) | Calculated (tenure × monthly) | Derived, show only |
| Age | Continuous (18-80) | `st.slider()` | If available; clear age range context |

### Service Status (Booleans)
| Data | Widget | Alternative |
|------|--------|-------------|
| Tech Support | `st.toggle()` | `st.checkbox()` |
| Online Security | `st.toggle()` | `st.checkbox()` |
| Phone Service | `st.toggle()` | `st.radio(horizontal=True)` |
| Internet Service | `st.selectbox()` | `st.radio()` |
| Backup Service | `st.toggle()` | Grouped checkbox |

### Contract & Billing
| Data | Type | Widget |
|------|------|--------|
| Contract Type | Categorical | `st.selectbox()` |
| Internet Service | Categorical | `st.selectbox()` |
| Payment Method | Categorical | `st.selectbox()` |
| Paperless Billing | Boolean | `st.toggle()` |

---

## 4. Layout Patterns for Business Dashboards

### ✅ **RECOMMENDED: Sectioned layout with clear visual hierarchy**

```python
st.title("📊 Telco Churn Prediction")

# Section 1: Core Demographics
with st.container(border=True):
    st.subheader("👤 Customer Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        tenure = st.slider("Tenure", 0, 72, 24)
    with col2:
        monthly = st.slider("Monthly Charges ($)", 18, 120, 50)
    with col3:
        total_charges = tenure * monthly
        st.metric("Total Charges", f"${total_charges:.2f}")

# Section 2: Services
with st.container(border=True):
    st.subheader("📱 Subscribed Services")
    col1, col2, col3 = st.columns(3)
    with col1:
        tech_support = st.toggle("Tech Support")
    with col2:
        online_security = st.toggle("Online Security")
    with col3:
        phone = st.toggle("Phone Service")

# Section 3: Contract Details
with st.container(border=True):
    st.subheader("📋 Account Details")
    col1, col2 = st.columns(2)
    with col1:
        contract = st.selectbox("Contract Type", 
            ["Month-to-month", "One year", "Two year"])
    with col2:
        internet = st.selectbox("Internet Service", 
            ["DSL", "Fiber Optic", "No"])

# Prediction Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔮 Predict Churn Risk", use_container_width=True):
        prediction = fetch_prediction({...})
        # Display results
```

**Why this works:**
- Visual hierarchy reduces cognitive load
- Containers group related inputs
- Emoji + text provides semantic meaning
- Call-to-action button is prominent and centered

---

## 5. Input Validation & Error Handling

### ✅ **RECOMMENDED: Validate in form before prediction**

```python
with st.form("prediction_form"):
    tenure = st.slider("Tenure (months)", 0, 72)
    monthly = st.number_input("Monthly ($)", 0.0, 150.0)
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    
    submitted = st.form_submit_button("Predict")

if submitted:
    # Client-side validation
    if tenure < 0 or monthly < 0:
        st.error("❌ Invalid input values")
    elif tenure == 0 and monthly == 0:
        st.warning("⚠️ New customer with no charges - unusual but valid")
    else:
        try:
            prediction = fetch_prediction({
                "tenure": tenure,
                "monthly": monthly,
                "contract": contract
            })
            st.success(f"✅ Churn probability: {prediction:.1%}")
        except requests.RequestException as e:
            st.error(f"API Error: {str(e)}")
```

**Best practices:**
- Sliders/selectboxes eliminate most invalid input automatically
- Form submission validates before API call
- Clear error messages guide users
- Unexpected inputs (like new customers with $0) get warnings, not errors

---

## 6. Mobile & Accessibility Considerations

### ✅ **Optimize for support team tablets**

```python
# Use responsive columns
col1, col2 = st.columns([1, 1])  # Equal width

# Avoid horizontal radio with >3 options
internet = st.selectbox("Internet", ["DSL", "Fiber", "No", "Satellite"])

# Use large touch targets
tech_support = st.toggle("Tech Support")  # Larger than checkbox

# Add help text for all inputs
tenure = st.slider("Tenure (months)", help="How long customer has been with us")

# Use horizontal=True for max 3-4 options
gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

# Test on mobile before deployment
st.write("👉 *Designed for tablet & desktop*")
```

---

## 7. Performance Optimization

### ✅ **Use `@st.cache_data` for static options**

```python
@st.cache_data
def get_contract_options():
    return ["Month-to-month", "One year", "Two year"]

contract = st.selectbox("Contract Type", get_contract_options())
```

### ✅ **Debounce number inputs with forms**

```python
with st.form("input_form"):
    monthly = st.number_input("Monthly Charges", step=0.01)
    if st.form_submit_button("Calculate"):
        # Single API call, not per keystroke
        result = predict(monthly)
```

---

## 8. Recommended Implementation for Your Dashboard

### Current Issues:
1. ❌ Tenure as `selectbox` is poor UX (requires scrolling to find value)
2. ✅ Monthly charges as `number_input` is appropriate
3. ✅ Tech support as `checkbox` works but toggle would be better
4. ❌ Missing form - API is called during re-render

### Improved Implementation:

```python
import streamlit as st
import requests

st.set_page_config(page_title="Telco Churn Predictor", page_icon="📊", layout="wide")

st.title("📊 Telco Churn Prediction Dashboard")
st.write("Predict customer churn risk based on their profile and services.")

st.divider()

# Form groups inputs and prevents excessive API calls
with st.form("churn_prediction_form"):
    st.subheader("📋 Customer Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tenure = st.slider(
            "Tenure (months)",
            min_value=0,
            max_value=72,
            value=24,
            step=1,
            help="How long the customer has been with company (0-72 months)"
        )
    
    with col2:
        monthly = st.slider(
            "Monthly Charges ($)",
            min_value=18.0,
            max_value=120.0,
            value=50.0,
            step=1.0,
            help="Monthly service charges ($18-$120 typical range)"
        )
    
    with col3:
        # Calculate and display total charges
        total_charges = tenure * monthly
        st.metric("Total Charges", f"${total_charges:,.0f}")
    
    # Services section
    st.subheader("📱 Subscribed Services")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        tech_support = st.toggle(
            "Tech Support",
            value=False,
            help="Customer has tech support subscription"
        )
    
    with col2:
        online_security = st.toggle(
            "Online Security",
            value=False,
            help="Customer has online security subscription"
        )
    
    with col3:
        phone_service = st.toggle(
            "Phone Service",
            value=False,
            help="Customer has phone service"
        )
    
    with col4:
        backup_service = st.toggle(
            "Backup Service",
            value=False,
            help="Customer has backup service"
        )
    
    # Contract section
    st.subheader("📋 Account Details")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contract = st.selectbox(
            "Contract Type",
            ["Month-to-month", "One year", "Two year"],
            help="Duration of customer contract"
        )
    
    with col2:
        internet = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber Optic", "No"],
            help="Type of internet service"
        )
    
    with col3:
        payment_method = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
            help="How customer pays their bill"
        )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button(
            "🔮 Predict Churn Risk",
            use_container_width=True,
            type="primary"
        )

# Only process prediction after form submission
if submitted:
    payload = {
        "tenure": float(tenure),
        "monthly": float(monthly),
        "techsupport": float(tech_support),
        "onlinesecurity": float(online_security),
        "phoneservice": float(phone_service),
        "backupservice": float(backup_service),
        "contract": contract,
        "internet": internet,
        "payment_method": payment_method,
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        prediction = data.get("prediction", 0)
        churn_percentage = prediction * 100
        
        st.divider()
        st.subheader("🎯 Prediction Results")
        
        # Risk level determination
        if prediction < 0.3:
            color = "green"
            risk_level = "Low Risk"
        elif prediction < 0.6:
            color = "orange"
            risk_level = "Medium Risk"
        else:
            color = "red"
            risk_level = "High Risk"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Churn Probability", f"{churn_percentage:.1f}%")
        
        with col2:
            st.metric("Risk Level", risk_level)
        
        with col3:
            st.metric("Tenure (months)", int(tenure))
        
        # Progress bar
        st.progress(
            min(prediction, 1.0),
            text=f"Churn Risk: {churn_percentage:.1f}%"
        )
        
        # Insights
        st.divider()
        st.subheader("💡 Insights & Recommendations")
        
        if prediction < 0.3:
            st.success(
                f"✅ **Low Churn Risk** ({churn_percentage:.1f}%)\n\n"
                f"This customer appears satisfied. Consider offering loyalty programs "
                f"to maintain retention and potentially upsell premium services."
            )
        elif prediction < 0.6:
            st.warning(
                f"⚠️ **Medium Churn Risk** ({churn_percentage:.1f}%)\n\n"
                f"Review their account and consider offering service upgrades, discounts, "
                f"or improved support to reduce churn likelihood."
            )
        else:
            st.error(
                f"🚨 **High Churn Risk** ({churn_percentage:.1f}%)\n\n"
                f"Immediate intervention recommended! Contact customer to understand concerns "
                f"and offer retention incentives."
            )
        
        # Detailed information
        with st.expander("📊 Detailed Information"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Input Parameters:**")
                st.write(f"- Tenure: {tenure} months")
                st.write(f"- Monthly Charges: ${monthly:.2f}")
                st.write(f"- Total Charges: ${total_charges:,.2f}")
                st.write(f"- Tech Support: {'✅ Yes' if tech_support else '❌ No'}")
                st.write(f"- Online Security: {'✅ Yes' if online_security else '❌ No'}")
                st.write(f"- Phone Service: {'✅ Yes' if phone_service else '❌ No'}")
                st.write(f"- Backup Service: {'✅ Yes' if backup_service else '❌ No'}")
                st.write(f"- Contract Type: {contract}")
                st.write(f"- Internet Service: {internet}")
                st.write(f"- Payment Method: {payment_method}")
            
            with col2:
                st.write("**Model Output:**")
                st.json(data)
    
    except requests.RequestException as e:
        st.error(f"❌ Error calling API: {e}")
        st.info("Make sure the API server is running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
```

---

## 9. Summary Table: Component Recommendations

| Scenario | Widget | Reasoning |
|----------|--------|-----------|
| **Continuous, bounded (tenure, age)** | `st.slider()` | Visual range context, prevents outliers |
| **Precise decimal (billing)** | `st.slider()` with step | Slider better than number_input for business |
| **Boolean, single** | `st.toggle()` | Modern, clear ON/OFF state |
| **Boolean, multiple related** | `st.toggle()` × N | Group in columns with container border |
| **Categorical, 3-6 options** | `st.selectbox()` | Compact, mobile-friendly, clear choices |
| **Categorical, obvious choice** | `st.radio()` with horizontal=True | Only if ≤3 options and always visible matters |
| **Data entry workflow** | `st.form()` | Single submit, fewer API calls, better UX |
| **Exploratory analysis** | Individual inputs | Real-time feedback for what-if scenarios |

---

## 10. Key Takeaways for Your Dashboard

✅ **DO:**
- Use `st.slider()` for tenure (bounded, intuitive)
- Use `st.toggle()` for service booleans (modern, clear)
- Use `st.form()` to batch inputs (one API call, atomic)
- Add help text to all inputs (context for support teams)
- Use `st.container(border=True)` to group related inputs
- Test on tablet (your users' primary device)

❌ **DON'T:**
- Use `st.selectbox()` for tenure (users have to scroll)
- Mix `st.checkbox()` and `st.toggle()` (inconsistent)
- Process inputs outside forms (causes excessive API calls)
- Use numbers without units ($ for money, months for time)
- Forget accessibility (tooltips, clear labels, large touch targets)

