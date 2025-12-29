
import streamlit as st
import json
from deduction_engine_enhanced import DeductionEngine

# Page configuration
st.set_page_config(
    page_title="Sherlock Holmes Deduction System",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        color: #8B4513;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.2em;
    }
    .sub-header {
        text-align: center;
        color: #555;
        font-style: italic;
        margin-bottom: 2em;
    }
    .body-part-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: white;
    }
    .context-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        color: white;
    }
    .profile-card {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: white;
    }
    .profile-card-danger {
        border: 3px solid #dc3545;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: #fff5f5;
        box-shadow: 0 0 20px rgba(220, 53, 69, 0.3);
    }
    .insight-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .warning-box {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #721c24;
    }
    .confidence-critical {
        color: #dc3545;
        font-weight: bold;
    }
    .confidence-high {
        color: #fd7e14;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .confidence-low {
        color: #6c757d;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'selected_cues' not in st.session_state:
    st.session_state.selected_cues = []
if 'selected_contexts' not in st.session_state:
    st.session_state.selected_contexts = []
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

# Initialize engine
engine = DeductionEngine()

# Header
st.markdown('<div class="main-header">🔍 THE SHERLOCK SYSTEM 🔍</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">"You see, but you do not observe." - Sherlock Holmes</div>', unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("## 👤 Human Observation Interface")

    # Context Bar
    st.markdown('<div class="context-section"><h3>🌍 Environmental Context</h3></div>', unsafe_allow_html=True)
    context_options = engine.get_context_options()
    selected_contexts = st.multiselect(
        "Select environmental factors that may influence interpretation:",
        context_options,
        key="context_select"
    )
    st.session_state.selected_contexts = selected_contexts

    st.markdown("---")

    # Get all cues by category
    all_cues = engine.get_all_cues_by_category()

    # Body part sections with emojis
    body_parts = {
        "🧠 Head & Face": ["MICRO_EXPRESSIONS", "BEHAVIORAL_CLUSTERS"],
        "✋ Hands & Arms": ["PHYSICAL_MARKERS"],
        "🗣️ Speech & Voice": ["FORENSIC_LINGUISTICS", "VOCAL_MARKERS"],
        "💭 Behavioral Patterns": ["DARK_TRIAD_MARKERS", "BEHAVIORAL_CLUSTERS"]
    }

    selected_cues = []

    for body_part, categories in body_parts.items():
        with st.expander(body_part, expanded=False):
            for category in categories:
                if category in all_cues:
                    st.markdown(f"**{category.replace('_', ' ')}**")
                    for cue in all_cues[category]:
                        unique_key = f"cue_{category}_{cue}"
                        if st.checkbox(
                            cue.replace('_', ' ').title(), 
                            key=unique_key
                        ):
                            selected_cues.append(cue)

    st.session_state.selected_cues = selected_cues

    # Analyze button
    st.markdown("---")
    if st.button("🔬 ANALYZE SUBJECT", type="primary", use_container_width=True):
        if len(selected_cues) == 0:
            st.error("⚠️ Please select at least one observable cue before analysis.")
        else:
            st.session_state.analysis_done = True
            st.rerun()

with col2:
    st.markdown("## 📊 Deduction Dashboard")

    if st.session_state.analysis_done and len(st.session_state.selected_cues) > 0:
        # Run analysis
        report, conflicts = engine.analyze(
            st.session_state.selected_cues,
            st.session_state.selected_contexts
        )

        # Check for Dark Triad markers
        dark_triad_detected = any(
            profile in ["Psychopathy", "Narcissism", "Machiavellianism", 
                       "Manipulator", "Dark_Persuasion", "Antisocial"]
            for item in report for profile in [item["Profile"]]
        )

        # Display warning if Dark Triad detected
        if dark_triad_detected:
            st.markdown("""
                <div class="warning-box">
                    <h3>⚠️ CAUTION: HIGH MANIPULATION RISK DETECTED</h3>
                    <p>Subject exhibits markers consistent with Dark Triad personality traits. 
                    Exercise extreme caution in interactions. Verify all claims independently.</p>
                </div>
            """, unsafe_allow_html=True)

        # Display incongruence findings
        if conflicts:
            st.markdown("### 🎯 Sherlock's Insights (Incongruence Analysis)")
            for conflict in conflicts:
                st.markdown(f"""
                    <div class="insight-box">
                        <strong>💡 {conflict}</strong>
                    </div>
                """, unsafe_allow_html=True)

        # Display profile cards
        st.markdown("### 🧩 Psychological Profile Analysis")

        if report:
            for idx, profile_data in enumerate(report[:8]):  # Top 8 profiles
                profile = profile_data["Profile"]
                score = profile_data["Probability_Score"]
                confidence = profile_data["Confidence"]
                threat = profile_data["Threat_Level"]

                # Determine if this is a high-risk profile
                is_danger = profile in [
                    "Psychopathy", "Narcissism", "Machiavellianism", 
                    "Deception", "Manipulator", "Hostility"
                ] and confidence in ["High", "Very High", "Critical/Certain"]

                card_class = "profile-card-danger" if is_danger else "profile-card"

                # Confidence color
                conf_class = {
                    "Critical/Certain": "confidence-critical",
                    "Very High": "confidence-critical",
                    "High": "confidence-high",
                    "Medium": "confidence-medium",
                    "Low": "confidence-low"
                }.get(confidence, "confidence-low")

                # Threat indicator
                threat_emoji = {
                    "Extreme": "🔴",
                    "High": "🟠",
                    "Moderate": "🟡",
                    "Low": "🟢",
                    "Normal": "⚪"
                }.get(threat, "⚪")

                st.markdown(f"""
                    <div class="{card_class}">
                        <h4>{threat_emoji} {profile.replace('_', ' ')}</h4>
                        <p><strong>Probability Score:</strong> {score}</p>
                        <p><strong>Confidence:</strong> <span class="{conf_class}">{confidence}</span></p>
                        <p><strong>Threat Assessment:</strong> {threat}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No significant profiles detected with current observations.")

        # Observation summary
        with st.expander("📝 Observation Summary", expanded=False):
            st.markdown("**Selected Cues:**")
            for cue in st.session_state.selected_cues:
                st.markdown(f"- {cue.replace('_', ' ').title()}")

            if st.session_state.selected_contexts:
                st.markdown("**Environmental Context:**")
                for ctx in st.session_state.selected_contexts:
                    st.markdown(f"- {ctx.replace('_', ' ').title()}")

        # Reset button
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.analysis_done = False
            st.session_state.selected_cues = []
            st.session_state.selected_contexts = []
            st.rerun()

    else:
        st.info("👈 Select observable cues from the left panel and click 'ANALYZE SUBJECT' to generate a psychological profile.")

        # Display example
        with st.expander("📖 Example Analysis", expanded=True):
            st.markdown("""
                **Example Scenario:**

                Subject displays:
                - Inward watch face
                - Tactical nail cut
                - Peripheral scanning
                - Past tense when describing present events
                - Voice pitch elevation

                **Context:** Job Interview

                **Likely Profile:**
                - Military/Security background (High confidence)
                - Deception detected (Medium-High confidence)
                - High stress/anxiety (Adjusted for context)
            """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        <p>⚖️ Forensic Psychology Principles | 🧠 Behavioral Analysis | 🔬 Evidence-Based Profiling</p>
        <p style="font-size: 0.8em; font-style: italic;">
            Disclaimer: This tool is for educational and entertainment purposes. 
            Professional forensic analysis requires extensive training and multiple data points.
        </p>
    </div>
""", unsafe_allow_html=True)
