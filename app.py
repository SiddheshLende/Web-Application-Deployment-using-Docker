import streamlit as st

# Page setup
st.set_page_config(
    page_title="Portfolio | Cloud & Python Engineer....",
    page_icon="⚡",
    layout="wide",
)

# --- HEADER SECTION ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Software & Cloud Engineer")
    st.caption("Specializing in Python Web Applications, Docker, & Cloud Infrastructure")
    
    st.write(
        """
        Passionate about designing scalable 3-tier architectures, automating CI/CD deployments, 
        and containerizing Python applications for cloud environments.
        """
    )
    
    st.markdown("📬 **Contact:** `your.email@example.com` | [GitHub](https://github.com) | [LinkedIn](https://linkedin.com)")

with col2:
    st.metric(label="Primary Stack", value="Python & AWS")
    st.metric(label="Architecture", value="3-Tier Systems")

st.divider()

# --- TECH STACK SECTION ---
st.subheader("🛠️ Technical Skills")

sk1, sk2, sk3 = st.columns(3)

with sk1:
    st.markdown("### Backend & Web")
    st.markdown("""
    - Python (Flask, FastAPI, Streamlit)
    - Nginx & Gunicorn
    - REST APIs
    """)

with sk2:
    st.markdown("### Cloud & DevOps")
    st.markdown("""
    - AWS (EC2, S3, IAM)
    - GitHub Actions (CI/CD)
    - Docker & Containerization
    """)

with sk3:
    st.markdown("### Infrastructure & Architecture")
    st.markdown("""
    - 3-Tier Web Application Architecture
    - Linux Server Administration
    - Automated Deployment Pipelines
    """)

st.divider()

# --- PROJECTS SECTION ---
st.subheader("🚀 Featured Projects")

tab1, tab2 = st.tabs(["3-Tier Web Application", "Automated CI/CD Pipeline"])

with tab1:
    st.markdown("#### Containerized 3-Tier Web Architecture")
    st.write(
        """
        Designed and deployed a high-availability 3-tier web architecture leveraging Docker containers, 
        Nginx as a reverse proxy, Gunicorn as the WSGI server, and a Python web app connected to a database backend.
        """
    )
    st.caption("**Technologies:** Python | Docker | Nginx | Gunicorn | AWS")

with tab2:
    st.markdown("#### AWS EC2 CI/CD Deployment Automation")
    st.write(
        """
        Built a complete continuous integration and deployment pipeline using GitHub Actions to automatically test, 
        build, and deploy Python services directly to AWS EC2 instances.
        """
    )
    st.caption("**Technologies:** GitHub Actions | AWS EC2 | Python | Shell Scripting")

st.divider()

# --- INTERACTIVE CONTACT FORM ---
st.subheader("💬 Get in Touch")

with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    submit = st.form_submit_button("Send Message")

    if submit:
        if name and email and message:
            st.success(f"Thank you {name}! Your message has been sent.")
        else:
            st.warning("Please fill out all fields before submitting.")