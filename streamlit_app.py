import os
import sys
import requests
import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Multi-Agent Customer Support Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# API
# =========================================================

API_URL = "http://127.0.0.1:8000"


# =========================================================
# SESSION STATE
# =========================================================

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "previous_context" not in st.session_state:
    st.session_state.previous_context = None

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = None


# =========================================================
# SAFE HELPERS
# =========================================================

def as_dict(value):
    """
    Safely convert an agent result to a dictionary.

    Prevents:
    AttributeError: 'str' object has no attribute 'get'
    """

    if isinstance(value, dict):
        return value

    return {}


def get_response_text(response_data):
    """
    Response Agent may return either:

    1. string
    2. dictionary containing response/message/text

    This function handles both.
    """

    if isinstance(response_data, str):

        return response_data

    if isinstance(response_data, dict):

        return (
            response_data.get("response")
            or response_data.get("message")
            or response_data.get("text")
            or "No response generated."
        )

    return "No response generated."


def safe_value(value, default="N/A"):

    if value is None:
        return default

    if isinstance(value, str) and not value.strip():
        return default

    return value


# =========================================================
# API REQUEST
# =========================================================

def process_ticket(
    ticket_text,
    previous_context=None
):

    try:

        response = requests.post(
            f"{API_URL}/process",
            json={
                "ticket_text": ticket_text,
                "previous_context": previous_context
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI.\n\n"
            "Make sure this is running:\n"
            "`python -m api.main`"
        )

        return None

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Request timed out."
        )

        return None

    except requests.exceptions.HTTPError as e:

        st.error(
            f"❌ FastAPI returned an error: {e}"
        )

        try:

            st.json(response.json())

        except Exception:

            st.code(response.text)

        return None

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {e}"
        )

        return None


# =========================================================
# API HEALTH
# =========================================================

def api_is_running():

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        return response.status_code == 200

    except Exception:

        return False


# =========================================================
# SAVE CONTEXT
# =========================================================

def update_context(result, is_follow_up=False):

    intake = as_dict(
        result.get("intake")
    )

    classification = as_dict(
        result.get("classification")
    )

    sentiment = as_dict(
        result.get("sentiment")
    )

    entities = intake.get(
        "entities",
        {}
    )

    if not isinstance(entities, dict):
        entities = {}

    st.session_state.previous_context = {

        "category": classification.get(
            "category"
        ),

        "category_confidence": classification.get(
            "category_confidence"
        ),

        "priority": classification.get(
            "priority"
        ),

        "priority_confidence": classification.get(
            "priority_confidence"
        ),

        "sentiment": sentiment.get(
            "sentiment"
        ),

        "sentiment_confidence": sentiment.get(
            "confidence"
        ),

        "intent": intake.get(
            "intent"
        ),

        "urgency": intake.get(
            "urgency"
        ),

        "entities": entities,

        "is_follow_up": is_follow_up
    }


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 Support Intelligence")

    st.markdown("---")

    st.subheader("System Status")

    if api_is_running():

        st.success(
            "🟢 FastAPI Connected"
        )

    else:

        st.error(
            "🔴 FastAPI Offline"
        )

    st.markdown("---")

    st.subheader("Agent Architecture")

    st.markdown(
        """
        📥 Intake Agent

        ↓

        🧠 Classification Agent

        ↓

        😊 Sentiment Agent

        ↓

        🔎 Retrieval / RAG Agent

        ↓

        💬 Response Agent

        ↓

        🚨 Escalation Agent

        ↓

        📚 Learning Agent
        """
    )

    st.markdown("---")

    st.subheader("Technology")

    st.markdown(
        """
        - Python
        - Scikit-learn
        - TF-IDF
        - Logistic Regression
        - Sentence Transformers
        - FAISS
        - SQLite
        - FastAPI
        - Streamlit
        - CrewAI
        """
    )

    st.markdown("---")

    st.subheader("Conversation Memory")

    if st.session_state.previous_context:

        st.success(
            "Context available"
        )

    else:

        st.info(
            "No context yet"
        )

    st.markdown("---")

    if st.button(
        "🔄 New Conversation",
        use_container_width=True
    ):

        st.session_state.conversation = []

        st.session_state.previous_context = None

        st.session_state.current_result = None

        st.session_state.ticket_id = None

        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.title(
    "🤖 Multi-Agent Customer Support Intelligence Platform"
)

st.markdown(
    """
    Intelligent eCommerce support powered by multiple specialized
    agents for ticket understanding, classification, sentiment,
    retrieval, response generation, escalation, and learning.
    """
)


# =========================================================
# API WARNING
# =========================================================

if not api_is_running():

    st.warning(
        "FastAPI is not currently running."
    )

    st.code(
        "python -m api.main",
        language="bash"
    )


# =========================================================
# CONVERSATION
# =========================================================

if st.session_state.conversation:

    st.markdown("---")

    st.subheader("💬 Conversation")

    for message in st.session_state.conversation:

        role = message.get(
            "role",
            "assistant"
        )

        content = message.get(
            "content",
            ""
        )

        with st.chat_message(role):

            st.write(content)


# =========================================================
# INITIAL TICKET
# =========================================================

if not st.session_state.conversation:

    st.markdown("---")

    st.subheader(
        "📩 Submit Customer Ticket"
    )

    initial_text = st.text_area(
        "Customer message",
        height=160,
        placeholder=(
            "Example:\n\n"
            "My order ORD7824512 for Wireless Headphones "
            "was delivered yesterday, but the headphones are "
            "completely damaged and don't turn on. I already "
            "tried charging them for several hours. I want a "
            "replacement instead of a refund because I need "
            "them urgently."
        )
    )

    if st.button(
        "🚀 Process Customer Ticket",
        type="primary",
        use_container_width=True
    ):

        if not initial_text.strip():

            st.warning(
                "Please enter a customer message."
            )

        else:

            with st.spinner(
                "🤖 Multi-agent system processing..."
            ):

                result = process_ticket(
                    initial_text.strip()
                )

            if result:

                st.session_state.current_result = result

                response_text = get_response_text(
                    result.get("response")
                )

                st.session_state.conversation = [

                    {
                        "role": "user",
                        "content": initial_text.strip()
                    },

                    {
                        "role": "assistant",
                        "content": response_text
                    }

                ]

                update_context(
                    result,
                    is_follow_up=False
                )

                st.session_state.ticket_id = result.get(
                    "database_ticket_id"
                )

                st.rerun()


# =========================================================
# FOLLOW-UP
# =========================================================

else:

    st.markdown("---")

    st.subheader(
        "↩️ Continue Conversation"
    )

    follow_up_text = st.text_area(
        "Follow-up message",
        height=120,
        placeholder=(
            "Example:\n\n"
            "I don't want a refund. Please arrange "
            "the replacement as soon as possible."
        )
    )

    if st.button(
        "📨 Send Follow-Up",
        type="primary",
        use_container_width=True
    ):

        if not follow_up_text.strip():

            st.warning(
                "Please enter a follow-up message."
            )

        else:

            with st.spinner(
                "🤖 Agents analyzing your follow-up..."
            ):

                result = process_ticket(
                    follow_up_text.strip(),
                    previous_context=(
                        st.session_state.previous_context
                    )
                )

            if result:

                st.session_state.current_result = result

                response_text = get_response_text(
                    result.get("response")
                )

                st.session_state.conversation.append(
                    {
                        "role": "user",
                        "content": follow_up_text.strip()
                    }
                )

                st.session_state.conversation.append(
                    {
                        "role": "assistant",
                        "content": response_text
                    }
                )

                update_context(
                    result,
                    is_follow_up=True
                )

                st.session_state.ticket_id = result.get(
                    "database_ticket_id"
                )

                st.rerun()


# =========================================================
# RESULT
# =========================================================

result = st.session_state.current_result


if result:

    # =====================================================
    # RESPONSE
    # =====================================================

    st.markdown("---")

    st.subheader(
        "💬 Response Agent"
    )

    response_data = result.get(
        "response"
    )

    response_text = get_response_text(
        response_data
    )

    st.success(
        response_text
    )


    # =====================================================
    # ANALYSIS
    # =====================================================

    st.markdown("---")

    st.subheader(
        "📊 Ticket Analysis"
    )

    intake = as_dict(
        result.get("intake")
    )

    classification = as_dict(
        result.get("classification")
    )

    sentiment = as_dict(
        result.get("sentiment")
    )

    escalation = as_dict(
        result.get("escalation")
    )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Category",
            safe_value(
                classification.get(
                    "category"
                )
            )
        )

        category_confidence = classification.get(
            "category_confidence"
        )

        if category_confidence is not None:

            st.caption(
                f"Confidence: "
                f"{float(category_confidence):.2f}%"
            )


    with col2:

        st.metric(
            "Priority",
            safe_value(
                classification.get(
                    "priority"
                )
            )
        )

        priority_confidence = classification.get(
            "priority_confidence"
        )

        if priority_confidence is not None:

            st.caption(
                f"Confidence: "
                f"{float(priority_confidence):.2f}%"
            )


    with col3:

        st.metric(
            "Sentiment",
            safe_value(
                sentiment.get(
                    "sentiment"
                )
            )
        )

        sentiment_confidence = sentiment.get(
            "confidence"
        )

        if sentiment_confidence is not None:

            st.caption(
                f"Confidence: "
                f"{float(sentiment_confidence):.2f}%"
            )


    with col4:

        st.metric(
            "Escalation",
            safe_value(
                escalation.get(
                    "decision"
                )
            )
        )

        escalation_score = escalation.get(
            "score"
        )

        if escalation_score is not None:

            st.caption(
                f"Score: {escalation_score}"
            )


    # =====================================================
    # TEAM
    # =====================================================

    team = classification.get(
        "assigned_team"
    )

    st.markdown(
        "### 👥 Assigned Team"
    )

    st.info(
        safe_value(
            team,
            "Not assigned"
        )
    )


    # =====================================================
    # INTAKE
    # =====================================================

    with st.expander(
        "📥 Intake Agent"
    ):

        st.write(
            "**Intent:**",
            safe_value(
                intake.get("intent")
            )
        )

        st.write(
            "**Urgency:**",
            safe_value(
                intake.get("urgency")
            )
        )

        st.write(
            "**Follow-Up:**",
            safe_value(
                intake.get(
                    "is_follow_up"
                ),
                "False"
            )
        )

        entities = intake.get(
            "entities",
            {}
        )

        if not isinstance(
            entities,
            dict
        ):

            entities = {}

        st.write(
            "**Order ID:**",
            safe_value(
                entities.get(
                    "order_id"
                )
            )
        )

        st.write(
            "**Product:**",
            safe_value(
                entities.get(
                    "product"
                )
            )
        )

        st.write(
            "**Cleaned Text:**",
            safe_value(
                intake.get(
                    "cleaned_text"
                )
            )
        )


    # =====================================================
    # CLASSIFICATION
    # =====================================================

    with st.expander(
        "🧠 Classification Agent"
    ):

        st.write(
            "**Category:**",
            safe_value(
                classification.get(
                    "category"
                )
            )
        )

        st.write(
            "**Category Confidence:**",
            safe_value(
                classification.get(
                    "category_confidence"
                )
            )
        )

        st.write(
            "**Priority:**",
            safe_value(
                classification.get(
                    "priority"
                )
            )
        )

        st.write(
            "**Priority Confidence:**",
            safe_value(
                classification.get(
                    "priority_confidence"
                )
            )
        )

        st.write(
            "**Assigned Team:**",
            safe_value(
                classification.get(
                    "assigned_team"
                )
            )
        )

        st.write(
            "**Follow-Up:**",
            safe_value(
                classification.get(
                    "is_follow_up"
                ),
                "False"
            )
        )


    # =====================================================
    # SENTIMENT
    # =====================================================

    with st.expander(
        "😊 Sentiment Agent"
    ):

        st.write(
            "**Sentiment:**",
            safe_value(
                sentiment.get(
                    "sentiment"
                )
            )
        )

        st.write(
            "**Confidence:**",
            safe_value(
                sentiment.get(
                    "confidence"
                )
            )
        )

        signals = sentiment.get(
            "signals",
            []
        )

        if isinstance(
            signals,
            list
        ) and signals:

            st.write(
                "**Detected Signals:**"
            )

            for signal in signals:

                st.write(
                    f"- {signal}"
                )


    # =====================================================
    # RAG
    # =====================================================

    with st.expander(
        "🔎 Retrieval / RAG Agent"
    ):

        retrieval = as_dict(
            result.get("retrieval")
        )

        retrieval_results = retrieval.get(
            "results",
            []
        )

        if not isinstance(
            retrieval_results,
            list
        ):

            retrieval_results = []

        st.write(
            "**Results Retrieved:**",
            len(retrieval_results)
        )

        faq_count = 0

        historical_count = 0

        for item in retrieval_results:

            if not isinstance(
                item,
                dict
            ):

                continue

            source_type = str(
                item.get(
                    "source_type",
                    ""
                )
            ).upper()

            if source_type == "FAQ":

                faq_count += 1

            elif source_type == "TICKET":

                historical_count += 1

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "FAQ Results",
                faq_count
            )

        with col2:

            st.metric(
                "Historical Tickets",
                historical_count
            )


        for i, item in enumerate(
            retrieval_results,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):

                continue

            st.markdown(
                f"**Result {i}**"
            )

            st.write(
                "**Source:**",
                safe_value(
                    item.get(
                        "source_type"
                    )
                )
            )

            st.write(
                "**ID:**",
                safe_value(
                    item.get(
                        "source_id"
                    )
                )
            )

            st.write(
                "**Category:**",
                safe_value(
                    item.get(
                        "category"
                    )
                )
            )

            st.write(
                "**Similarity:**",
                safe_value(
                    item.get(
                        "similarity"
                    )
                )
            )

            issue = item.get(
                "issue"
            )

            if issue:

                st.write(
                    "**Issue:**",
                    issue
                )

            resolution = item.get(
                "resolution"
            )

            if resolution:

                st.write(
                    "**Resolution:**",
                    resolution
                )

            st.markdown("---")


    # =====================================================
    # RESPONSE DETAILS
    # =====================================================

    with st.expander(
        "💬 Response Agent Details"
    ):

        st.write(
            "**Generated Response:**"
        )

        st.write(
            response_text
        )

        if isinstance(
            response_data,
            dict
        ):

            st.write(
                "**Intent:**",
                safe_value(
                    response_data.get(
                        "intent"
                    )
                )
            )

            st.write(
                "**Source:**",
                safe_value(
                    response_data.get(
                        "source"
                    )
                )
            )


    # =====================================================
    # ESCALATION
    # =====================================================

    with st.expander(
        "🚨 Escalation Agent"
    ):

        st.write(
            "**Decision:**",
            safe_value(
                escalation.get(
                    "decision"
                )
            )
        )

        st.write(
            "**Score:**",
            safe_value(
                escalation.get(
                    "score"
                )
            )
        )

        reasons = escalation.get(
            "reasons",
            []
        )

        if isinstance(
            reasons,
            list
        ) and reasons:

            st.write(
                "**Reasons:**"
            )

            for reason in reasons:

                st.write(
                    f"- {reason}"
                )


    # =====================================================
    # LEARNING
    # =====================================================

    with st.expander(
        "📚 Learning Agent"
    ):

        learning = as_dict(
            result.get("learning")
        )

        if learning:

            st.success(
                "Learning report generated."
            )

            ticket_statistics = as_dict(
                learning.get(
                    "ticket_statistics"
                )
            )

            if ticket_statistics:

                st.write(
                    "**Tickets Analyzed:**",
                    safe_value(
                        ticket_statistics.get(
                            "total_tickets"
                        )
                    )
                )

            st.write(
                "**Automation Rate:**",
                safe_value(
                    learning.get(
                        "automation_rate"
                    )
                )
            )

            st.write(
                "**Escalation Rate:**",
                safe_value(
                    learning.get(
                        "escalation_rate"
                    )
                )
            )
            retrieval_statistics = learning.get(
                "retrieval_statistics"
            )

            if retrieval_statistics:

                st.write(
                    "**Retrieval Statistics:**"
                )

                st.json(
                    retrieval_statistics
                )

        else:

            st.info(
                "Learning report unavailable."
            )


    # =====================================================
    # DATABASE + REAL AGENT LOGS
    # =====================================================

    with st.expander(
        "🗄️ Database & Agent Logs"
    ):

        ticket_id = st.session_state.ticket_id

        st.write(
            "**Database Ticket ID:**",
            safe_value(ticket_id)
        )

        if ticket_id:

            try:

                log_response = requests.get(
                    f"{API_URL}/logs/{ticket_id}",
                    timeout=10
                )

                if log_response.status_code == 200:

                    log_data = log_response.json()

                    logs = log_data.get(
                        "logs",
                        []
                    )

                    st.write(
                        f"**Agent Log Count:** "
                        f"{len(logs)}"
                    )

                    for log in logs:

                        if not isinstance(
                            log,
                            dict
                        ):

                            continue

                        agent_name = log.get(
                            "agent_name",
                            "Unknown Agent"
                        )

                        status = log.get(
                            "status",
                            "Unknown"
                        )

                        summary = log.get(
                            "output_summary",
                            ""
                        )

                        st.markdown(
                            f"**{agent_name}** "
                            f"— `{status}`"
                        )

                        if summary:

                            st.caption(
                                summary
                            )

                else:

                    st.warning(
                        "Could not load agent logs."
                    )

            except Exception as e:

                st.warning(
                    f"Could not retrieve logs: {e}"
                )


    # =====================================================
    # MEMORY
    # =====================================================

    with st.expander(
        "🧠 Conversation Memory"
    ):

        if st.session_state.previous_context:

            st.json(
                st.session_state.previous_context
            )

        else:

            st.info(
                "No conversation context."
            )


    # =====================================================
    # FEEDBACK
    # =====================================================

    st.markdown("---")

    st.subheader(
        "⭐ Customer Feedback"
    )

    rating = st.select_slider(
        "How helpful was the response?",
        options=[1, 2, 3, 4, 5],
        value=5
    )

    feedback_text = st.text_input(
        "Optional feedback",
        placeholder=(
            "Tell us how we can improve..."
        )
    )

    if st.button(
        "Submit Feedback",
        use_container_width=True
    ):

        ticket_id = st.session_state.ticket_id

        if not ticket_id:

            st.warning(
                "No ticket ID available."
            )

        else:

            try:

                feedback_response = requests.post(
                    f"{API_URL}/feedback/{ticket_id}",
                    json={
                        "rating": rating,
                        "feedback_text": feedback_text
                    },
                    timeout=10
                )

                if feedback_response.status_code == 200:

                    st.success(
                        "✅ Feedback submitted successfully."
                    )

                else:

                    st.error(
                        "Could not submit feedback."
                    )

            except Exception as e:

                st.error(
                    f"Feedback error: {e}"
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Multi-Agent Customer Support Intelligence Platform "
    "• ML + RAG + Multi-Agent Architecture"
)