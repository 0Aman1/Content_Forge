"""
ContentForge - AI Content Generator

Forge your content with AI. Powerfully.
A free, open-source platform for generating content using cloud AI models via Groq.
"""

import streamlit as st
import os
import time
from datetime import datetime
from typing import List, Dict, Any

# Load .env file if present (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional; keys can be set via environment

# Import local modules
from db import Database
from generator import ContentGenerator, GroqManager
from prompts import (
    ContentAnalyzer,
    CONTENT_TYPES,
    TONES,
    STYLES,
    LENGTHS,
    LANGUAGES,
)
from export_utils import ExportManager
from templates import TemplateLibrary
from settings import Settings, SessionMemory

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="ContentForge - AI Content Generator",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown(
    """
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-bg: #1f2937;
    }
    
    /* Custom styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Dashboard metrics - enhanced contrast */
    .stMetric {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        color: #1f2937 !important;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        border: 1px solid #bae6fd;
    }
    
    .stMetric label, .stMetric [data-testid="metric-label"], .stMetric [data-testid="metric-value"] {
        color: #1f2937 !important;
    }
    
    .stMetric [data-testid="metric-label"] {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #6b7280 !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        color: #1f2937 !important;
    }
    
    .stMetric div, .stMetric span, .stMetric p {
        color: #374151 !important;
    }
    
    /* Sidebar metrics styling */
    [data-testid="stSidebar"] .stMetric {
        background-color: #f0f4ff;
        border: 2px solid #6366f1;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
    }
    
    [data-testid="stSidebar"] .stMetric [data-testid="metric-label"] {
        color: #4f46e5 !important;
    }
    
    [data-testid="stSidebar"] .stMetric [data-testid="metric-value"] {
        color: #1f2937 !important;
    }
    
    stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #155724;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #721c24;
        border-left: 4px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        color: #1e40af;
        border-left: 4px solid #2563eb;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .card {
        background: linear-gradient(135deg, #faf8ff 0%, #f3e8ff 100%);
        color: #1f2937 !important;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        border: 1px solid #e9d5ff;
    }
    
    /* Apply text color to all elements inside white backgrounds */
    [data-testid="metric"], [data-testid="column"] {
        color: #1f2937 !important;
    }
    
    [data-testid="metric"] * {
        color: #374151 !important;
    }
    
    /* Sidebar text - enhanced visibility */
    [data-testid="stSidebar"] {
        color: #1f2937 !important;
        background-color: #f9fafb;
    }
    
    [data-testid="stSidebar"] * {
        color: #374151 !important;
    }
    
    /* Sidebar markdown text */
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h1 {
        color: #1f2937 !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #374151 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================


def init_session_state():
    """Initialize session state variables"""

    if "db" not in st.session_state:
        st.session_state.db = Database()

    if "groq_manager" not in st.session_state:
        st.session_state.groq_manager = GroqManager()

    if "generator" not in st.session_state:
        st.session_state.generator = ContentGenerator(st.session_state.groq_manager)

    if "export_manager" not in st.session_state:
        st.session_state.export_manager = ExportManager()

    if "settings" not in st.session_state:
        st.session_state.settings = Settings()

    if "session_memory" not in st.session_state:
        st.session_state.session_memory = SessionMemory()

    if "generated_outputs" not in st.session_state:
        st.session_state.generated_outputs = []

    if "current_output_index" not in st.session_state:
        st.session_state.current_output_index = 0

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Dashboard"

    if "pending_rewrite" not in st.session_state:
        st.session_state.pending_rewrite = None

    if "rewrite_type" not in st.session_state:
        st.session_state.rewrite_type = None

    if "show_rewrite_comparison" not in st.session_state:
        st.session_state.show_rewrite_comparison = False


init_session_state()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def check_groq_availability():
    """Check if the Groq API key is configured and show instructions if not"""

    if not GroqManager.is_api_configured():
        st.error(
            """
        ❌ **Groq API Key Not Configured**
        
        ContentForge requires a Groq API key to generate content.
        
        **Setup Instructions:**
        
        1. Get a free API key from [https://console.groq.com](https://console.groq.com)
        2. Set the `GROQ_API_KEY` environment variable:
           - **Hugging Face Spaces:** Add it as a Secret in your Space settings.
           - **Local development:** Create a `.env` file with `GROQ_API_KEY=your_key_here`
        3. Refresh this page (press F5)
        
        **Supported Models:**
        - gpt-oss-20b (GPT OSS 20B — fast, recommended)
        - gpt-oss-120b (GPT OSS 120B — most powerful)
        - qwen-27b (Qwen 3.8 27B)
        - allam-7b (Allam 2 7B — lightweight)
        """
        )
        return False

    return True


def display_dashboard():
    """Display dashboard with key metrics and quick actions"""

    st.title("📊 Dashboard")

    # Check Groq API
    if not check_groq_availability():
        return

    # Get statistics
    stats = st.session_state.db.get_history_stats()
    session_stats = st.session_state.session_memory.get_stats()

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📝 Content Generated",
            stats["total_generated"],
            f"{session_stats['generation_count']} this session",
        )

    with col2:
        st.metric(
            "📊 Total Words",
            f"{stats['total_words']:,}",
            f"{session_stats['total_words_generated']:,} this session",
        )

    with col3:
        templates = st.session_state.db.get_templates()
        st.metric("📚 Saved Templates", len(templates))

    with col4:
        favorites = st.session_state.db.get_favorites()
        st.metric("⭐ Favorites", len(favorites))

    st.divider()

    # Quick action buttons
    st.subheader("🚀 Quick Actions")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("✍️ Blog Writer", use_container_width=True):
            st.session_state.selected_page = "Generator"
            st.rerun()

    with col2:
        if st.button("📧 Email Writer", use_container_width=True):
            st.session_state.selected_page = "Generator"
            st.rerun()

    with col3:
        if st.button("🛍️ Product Copy", use_container_width=True):
            st.session_state.selected_page = "Generator"
            st.rerun()

    with col4:
        if st.button("📱 Social Media", use_container_width=True):
            st.session_state.selected_page = "Generator"
            st.rerun()

    with col5:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.selected_page = "Settings"
            st.rerun()

    st.divider()

    # Content statistics by type
    st.subheader("📈 Content Statistics")

    if stats["content_stats"]:
        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(
                {
                    item["content_type"]: item["count"]
                    for item in stats["content_stats"]
                }
            )

        with col2:
            st.info(
                f"""
            **Statistics Summary:**
            
            • Total Generations: {stats['total_generated']}
            • Total Words Generated: {stats['total_words']:,}
            • Types of Content: {len(stats['content_stats'])}
            • Session Favorite Count: {len(st.session_state.db.get_favorites())}
            """
            )
    else:
        st.info("📊 No content generated yet. Start generating to see statistics!")


def display_generator():
    """Display content generator module"""

    st.title("✨ Content Generator")

    if not check_groq_availability():
        return

    # Create tabs for different sections
    tab1, tab2 = st.tabs(["Generate", "Advanced"])

    with tab1:
        # Main generator interface
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Content Configuration")

            # Content type
            content_type = st.selectbox(
                "📰 Content Type",
                list(CONTENT_TYPES.keys()),
                help="Select the type of content you want to generate",
            )

            # Topic
            topic = st.text_input(
                "📍 Topic / Subject",
                placeholder="E.g., 'How to learn Python programming'",
                help="Provide the main topic for content generation",
            )

            # Audience
            audience = st.text_input(
                "👥 Target Audience",
                placeholder="E.g., 'Beginners', 'Technical professionals', 'Business owners'",
                help="Describe who the content is for",
            )

            # Tone and Style in columns
            col_tone, col_style = st.columns(2)

            with col_tone:
                tone = st.selectbox("🎭 Tone", TONES, help="Select the tone of voice")

            with col_style:
                style = st.selectbox(
                    "🎨 Style", STYLES, help="Select the writing style"
                )

            # Length and Language in columns
            col_length, col_lang = st.columns(2)

            with col_length:
                length = st.selectbox(
                    "📏 Length",
                    list(LENGTHS.keys()),
                    help="Select desired content length",
                )

            with col_lang:
                language = st.selectbox(
                    "🌐 Language",
                    list(LANGUAGES.keys()),
                    help="Select output language",
                )

            # Keywords
            keywords = st.text_input(
                "🔑 Keywords (optional)",
                placeholder="E.g., 'python, programming, tutorial'",
                help="Enter keywords separated by commas",
            )

            # Number of outputs
            num_outputs = st.slider(
                "📑 Number of Outputs",
                min_value=1,
                max_value=3,
                value=1,
                help="Generate 1-3 different versions",
            )

        with col2:
            st.subheader("⚙️ Advanced Settings")

            # Creativity slider
            creativity = st.slider(
                "🎲 Creativity Level",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Lower = more factual, Higher = more creative",
            )

            # Current model
            current_model = st.session_state.settings.get_default_model()
            st.info(f"🤖 Current Model: **{current_model}**")

            if st.button("Change Model", use_container_width=True):
                st.session_state.selected_page = "Settings"
                st.rerun()

        # Generate button
        st.divider()

        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            generate_button = st.button(
                "🚀 Generate Content", key="generate_btn", use_container_width=True
            )

        if generate_button:
            if not topic or not audience:
                st.error("❌ Please fill in Topic and Audience fields")
            else:
                with st.spinner("⏳ Generating content..."):
                    try:
                        outputs = st.session_state.generator.generate_content(
                            content_type=content_type,
                            topic=topic,
                            audience=audience,
                            tone=tone,
                            style=style,
                            length=length,
                            language=language,
                            keywords=keywords,
                            creativity=creativity,
                            num_outputs=num_outputs,
                        )

                        st.session_state.generated_outputs = outputs
                        st.session_state.current_output_index = 0

                        # Save to history
                        for output in outputs:
                            st.session_state.db.add_history(
                                content_type=content_type,
                                topic=topic,
                                audience=audience,
                                tone=tone,
                                style=style,
                                model=current_model,
                                generated_text=output,
                            )

                        # Update session memory
                        st.session_state.session_memory.update_last_generation(
                            content=outputs[0],
                            content_type=content_type,
                            topic=topic,
                            model=current_model,
                        )

                        st.success("✅ Content generated successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Error generating content: {str(e)}")

    with tab2:
        st.subheader("🔍 Advanced Options")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            **Tips for Better Results:**
            
            ✓ Be specific in your topic
            ✓ Clearly define your target audience
            ✓ Use relevant keywords
            ✓ Adjust creativity based on content type
            ✓ Adjust length for different platforms
            """
            )

        with col2:
            st.markdown(
                """
            **Tone Guide:**
            
            • **Professional**: Business and formal
            • **Friendly**: Conversational and warm
            • **Persuasive**: Sales and marketing
            • **Technical**: Complex topics
            • **Casual**: Relaxed and informal
            • **Funny**: Humorous and entertaining
            """
            )

    # Display generated outputs if any
    if st.session_state.generated_outputs:
        st.divider()
        display_generated_outputs()


def display_generated_outputs():
    """Display and manage generated outputs"""

    outputs = st.session_state.generated_outputs

    st.subheader("📄 Generated Content")

    # Output navigation
    if len(outputs) > 1:
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Version", f"{st.session_state.current_output_index + 1}/{len(outputs)}")

        with col2:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_output_index = (
                    st.session_state.current_output_index - 1
                ) % len(outputs)
                st.rerun()

        with col3:
            pass

        with col4:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_output_index = (
                    st.session_state.current_output_index + 1
                ) % len(outputs)
                st.rerun()

        with col5:
            pass

    current_output = outputs[st.session_state.current_output_index]

    # Display output
    st.text_area(
        "Generated Content:",
        value=current_output,
        height=300,
        disabled=True,
        key="output_area",
    )

    # Analytics
    st.subheader("📊 Content Analytics")

    col1, col2, col3, col4 = st.columns(4)

    word_count = ContentAnalyzer.count_words(current_output)
    char_count = ContentAnalyzer.count_characters(current_output)
    reading_time = ContentAnalyzer.estimate_reading_time(current_output)

    with col1:
        st.metric("Words", word_count)

    with col2:
        st.metric("Characters", char_count)

    with col3:
        st.metric("Reading Time", f"{reading_time} min")

    with col4:
        # Get last generation data from session
        last_gen = st.session_state.session_memory.get_last_generation()
        keywords = st.session_state.session_memory.memory.get("last_keywords", "")

    # Action buttons
    st.subheader("🎯 Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.success("✅ Copied to clipboard!")

    with col2:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.info("Regenerating with same settings...")

    with col3:
        if st.button("⭐ Add to Favorites", use_container_width=True):
            st.session_state.session_memory.add_favorite(current_output)
            st.success("✅ Added to favorites!")

    with col4:
        if st.button("💾 Export", use_container_width=True):
            st.session_state.selected_page = "Export"
            st.rerun()

    # Rewrite options
    st.subheader("✏️ Rewrite Options")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📉 Make Shorter", use_container_width=True, key="shorter"):
            with st.spinner("⏳ Rewriting..."):
                try:
                    rewritten = st.session_state.generator.rewrite_content(
                        current_output, "shorter"
                    )
                    st.session_state.pending_rewrite = rewritten
                    st.session_state.rewrite_type = "Make Shorter"
                    st.session_state.show_rewrite_comparison = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col2:
        if st.button("📈 Make Longer", use_container_width=True, key="longer"):
            with st.spinner("⏳ Rewriting..."):
                try:
                    rewritten = st.session_state.generator.rewrite_content(
                        current_output, "longer"
                    )
                    st.session_state.pending_rewrite = rewritten
                    st.session_state.rewrite_type = "Make Longer"
                    st.session_state.show_rewrite_comparison = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col3:
        if st.button("✍️ Improve Grammar", use_container_width=True, key="grammar"):
            with st.spinner("⏳ Improving..."):
                try:
                    improved = st.session_state.generator.rewrite_content(
                        current_output, "grammar"
                    )
                    st.session_state.pending_rewrite = improved
                    st.session_state.rewrite_type = "Improve Grammar"
                    st.session_state.show_rewrite_comparison = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col4:
        if st.button("🔍 SEO Optimize", use_container_width=True, key="seo"):
            with st.spinner("⏳ Optimizing..."):
                try:
                    optimized = st.session_state.generator.rewrite_content(
                        current_output, "seo"
                    )
                    st.session_state.pending_rewrite = optimized
                    st.session_state.rewrite_type = "SEO Optimize"
                    st.session_state.show_rewrite_comparison = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Show rewrite comparison if pending
    if st.session_state.show_rewrite_comparison and st.session_state.pending_rewrite:
        st.divider()
        st.subheader(f"📊 Rewrite Comparison - {st.session_state.rewrite_type}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Original Content:**")
            st.text_area(
                "Original:",
                value=current_output,
                height=300,
                disabled=True,
                key="original_comparison",
            )

        with col2:
            st.markdown("**New Content:**")
            st.text_area(
                "Rewritten:",
                value=st.session_state.pending_rewrite,
                height=300,
                disabled=True,
                key="rewritten_comparison",
            )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Accept Rewrite", use_container_width=True, key="accept_rewrite"):
                outputs[st.session_state.current_output_index] = st.session_state.pending_rewrite
                st.session_state.pending_rewrite = None
                st.session_state.rewrite_type = None
                st.session_state.show_rewrite_comparison = False
                st.success("✅ Rewrite accepted!")
                st.rerun()

        with col2:
            if st.button("❌ Reject Rewrite", use_container_width=True, key="reject_rewrite"):
                st.session_state.pending_rewrite = None
                st.session_state.rewrite_type = None
                st.session_state.show_rewrite_comparison = False
                st.info("Rewrite rejected.")
                st.rerun()

        with col3:
            pass


def display_history():
    """Display generation history"""

    st.title("📜 Generation History")

    # Get history
    history = st.session_state.db.get_history()

    if not history:
        st.info("📭 No generation history yet. Start creating content!")
        return

    # Search and filter
    col1, col2, col3 = st.columns(3)

    with col1:
        search_topic = st.text_input("🔍 Search by topic")

    with col2:
        content_types = ["All"] + list(CONTENT_TYPES.keys())
        selected_type = st.selectbox("📂 Filter by type", content_types)

    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()

    st.divider()

    # Filter results
    filtered_history = history

    if search_topic:
        filtered_history = [
            h
            for h in filtered_history
            if search_topic.lower() in h.get("topic", "").lower()
        ]

    if selected_type != "All":
        filtered_history = [
            h for h in filtered_history if h.get("content_type") == selected_type
        ]

    # Display history as expandable items
    for idx, item in enumerate(filtered_history):
        with st.expander(
            f"📝 {item['content_type']} - {item['topic']} ({item['date']})",
            expanded=False,
        ):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.text_area(
                    "Content:",
                    value=item["generated_text"],
                    height=200,
                    disabled=True,
                    key=f"content_{idx}",
                )

            with col2:
                st.markdown(f"""
                **Metadata:**
                - **Type:** {item['content_type']}
                - **Topic:** {item['topic']}
                - **Tone:** {item['tone']}
                - **Model:** {item['model']}
                - **Words:** {item['word_count']}
                - **Date:** {item['date']}
                """)

                if st.button("✅ Use Again", key=f"use_{idx}"):
                    st.success("Content copied to clipboard!")

                if st.button("❌ Delete", key=f"delete_{idx}"):
                    st.session_state.db.delete_history_entry(item["id"])
                    st.success("Deleted!")
                    st.rerun()

    # Bulk actions
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.db.clear_history()
            st.success("✅ History cleared!")
            st.rerun()

    with col2:
        if st.button("📊 Export History as CSV", use_container_width=True):
            # Convert to CSV
            import pandas as pd

            df = pd.DataFrame(filtered_history)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"content_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )


def display_templates():
    """Display template library"""

    st.title("📚 Template Library")

    # Tabs for prebuilt vs custom
    tab1, tab2 = st.tabs(["Prebuilt Templates", "Saved Templates"])

    with tab1:
        st.subheader("🎯 Prebuilt Templates")

        prebuilt = TemplateLibrary.get_prebuilt_templates()

        col1, col2 = st.columns([2, 1])

        with col1:
            selected_template = st.selectbox(
                "Select a template:", list(prebuilt.keys())
            )

        with col2:
            if st.button("Use This Template", use_container_width=True):
                st.session_state.selected_template = selected_template
                st.rerun()

        # Display selected template
        if selected_template:
            template = prebuilt[selected_template]

            st.markdown(f"**Description:** {template['description']}")
            st.markdown(f"**Content Type:** {template['content_type']}")

            st.text_area(
                "Template Preview:",
                value=template["template_text"],
                height=300,
                disabled=True,
                key="template_preview",
            )

            # Fill template placeholders
            st.divider()
            st.subheader("Fill Template Placeholders")

            placeholders = TemplateLibrary.get_placeholders(selected_template)

            placeholder_values = {}
            for placeholder in placeholders:
                placeholder_values[placeholder] = st.text_input(
                    f"Enter {placeholder}:",
                    placeholder=f"Value for {placeholder}",
                )

            if st.button("🚀 Generate from Template", use_container_width=True):
                with st.spinner("Generating..."):
                    try:
                        rendered = TemplateLibrary.render_template(
                            selected_template, placeholder_values
                        )

                        # Generate content based on template
                        template_obj = prebuilt[selected_template]
                        outputs = st.session_state.generator.generate_from_template(
                            rendered, placeholder_values
                        )

                        st.session_state.generated_outputs = [outputs]
                        st.session_state.current_output_index = 0

                        # Save to history
                        st.session_state.db.add_history(
                            content_type=template_obj["content_type"],
                            topic=selected_template,
                            audience="Template-based",
                            tone="From Template",
                            style="From Template",
                            model=st.session_state.settings.get_default_model(),
                            generated_text=outputs,
                        )

                        st.success("✅ Content generated from template!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with tab2:
        st.subheader("💾 Saved Templates")

        # Save new template
        with st.expander("➕ Create New Template"):
            template_name = st.text_input("Template Name", placeholder="My Awesome Template")

            template_type = st.selectbox(
                "Content Type:", list(CONTENT_TYPES.keys())
            )

            template_description = st.text_area(
                "Description", placeholder="Brief description of this template"
            )

            template_content = st.text_area(
                "Template Content",
                placeholder="Use {placeholder} for replaceable fields",
                height=200,
            )

            if st.button("💾 Save Template"):
                if template_name and template_content:
                    success = st.session_state.db.add_template(
                        name=template_name,
                        content_type=template_type,
                        description=template_description,
                        template_text=template_content,
                    )

                    if success:
                        st.success("✅ Template saved!")
                        st.rerun()
                    else:
                        st.error("❌ Template with this name already exists")
                else:
                    st.error("❌ Please fill in all required fields")

        st.divider()

        # Display saved templates
        saved_templates = st.session_state.db.get_templates()

        if not saved_templates:
            st.info("📭 No saved templates yet. Create one above!")
        else:
            for template in saved_templates:
                with st.expander(f"{template['name']} ({template['content_type']})"):
                    st.markdown(f"**Description:** {template['description']}")

                    st.text_area(
                        "Content:",
                        value=template["template_text"],
                        height=200,
                        disabled=True,
                        key=f"saved_template_{template['id']}",
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{template['id']}"):
                            st.info("Edit functionality coming soon")

                    with col2:
                        if st.button("📋 Copy", key=f"copy_{template['id']}"):
                            st.success("Copied!")

                    with col3:
                        if st.button(
                            "🗑️ Delete", key=f"delete_template_{template['id']}"
                        ):
                            st.session_state.db.delete_template(template["id"])
                            st.success("Deleted!")
                            st.rerun()


def display_export():
    """Display export center"""

    st.title("💾 Export Center")

    if not st.session_state.generated_outputs:
        st.info("📭 No generated content to export. Generate content first!")
        return

    current_output = st.session_state.generated_outputs[
        st.session_state.current_output_index
    ]

    st.subheader("📥 Export Current Output")

    col1, col2 = st.columns([2, 1])

    with col1:
        filename = st.text_input(
            "Filename (without extension):",
            value=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        )

    with col2:
        export_format = st.selectbox("Format:", ["txt", "docx", "pdf"])

    # Metadata to include
    st.subheader("📋 Metadata to Include")

    include_metadata = st.checkbox("Include metadata in exported file", value=True)

    metadata = {}
    if include_metadata:
        col1, col2 = st.columns(2)

        with col1:
            metadata["Author"] = st.text_input("Author", value="AI Content Studio")

        with col2:
            metadata["Title"] = st.text_input(
                "Title",
                value=f"Generated Content - {datetime.now().strftime('%Y-%m-%d')}",
            )

        col1, col2 = st.columns(2)

        with col1:
            metadata["Word Count"] = ContentAnalyzer.count_words(current_output)

        with col2:
            metadata["Date Generated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Export button
    st.divider()

    if st.button(
        f"📤 Export as {export_format.upper()}", use_container_width=True
    ):
        try:
            if export_format == "txt":
                filepath = st.session_state.export_manager.export_txt(
                    current_output, filename, metadata if include_metadata else None
                )

            elif export_format == "docx":
                filepath = st.session_state.export_manager.export_docx(
                    current_output, filename, metadata if include_metadata else None
                )

            elif export_format == "pdf":
                filepath = st.session_state.export_manager.export_pdf(
                    current_output, filename, metadata if include_metadata else None
                )

            st.success(f"✅ Exported to: {filepath}")

        except Exception as e:
            st.error(f"❌ Export error: {str(e)}")

    st.divider()

    # Export all
    st.subheader("📤 Export All Outputs")

    if len(st.session_state.generated_outputs) > 1:
        all_format = st.selectbox("Format for all outputs:", ["txt", "docx", "pdf"])

        if st.button("📤 Export All Versions", use_container_width=True):
            try:
                filepaths = st.session_state.export_manager.export_multiple_outputs(
                    st.session_state.generated_outputs,
                    "content",
                    filename,
                    all_format,
                )

                st.success(f"✅ Exported {len(filepaths)} files!")

            except Exception as e:
                st.error(f"❌ Export error: {str(e)}")

    st.divider()

    # File manager
    st.subheader("📂 Exported Files")

    files = st.session_state.export_manager.get_export_files()

    if files:
        for file in files[:10]:  # Show last 10
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

            with col1:
                st.text(file["filename"])

            with col2:
                st.caption(f"Modified: {file['modified']}")

            with col3:
                st.caption(f"Size: {file['size']} bytes")

            with col4:
                if st.button("🗑️", key=f"delete_file_{file['filename']}"):
                    st.session_state.export_manager.delete_export_file(
                        file["filename"]
                    )
                    st.success("Deleted!")
                    st.rerun()
    else:
        st.info("📭 No exported files yet")


def display_settings():
    """Display settings page"""

    st.title("⚙️ Settings")

    # Model settings
    st.subheader("🤖 AI Model Settings")

    col1, col2 = st.columns([2, 1])

    with col1:
        available_models = GroqManager.get_available_models()

        current_model = st.session_state.settings.get_default_model()
        selected_model = st.selectbox(
            "Select Model:",
            available_models,
            index=available_models.index(current_model)
            if current_model in available_models
            else 0,
        )

        if selected_model != current_model:
            st.session_state.settings.set_default_model(selected_model)
            st.session_state.groq_manager.set_model(selected_model)
            st.success(f"✅ Model changed to {selected_model}")

    with col2:
        if st.button("🔌 Test Connection", use_container_width=True):
            with st.spinner("Testing..."):
                if st.session_state.groq_manager.test_connection():
                    st.success("✅ Connection successful!")
                else:
                    st.error("❌ Connection failed. Check your GROQ_API_KEY.")

    # API Status
    st.subheader("🔑 API Status")

    status = st.session_state.groq_manager.get_status()
    if status["api_configured"]:
        st.success(f"{status['status']}\n\n**Active Model:** `{status['groq_model_id']}`")
    else:
        st.error(
            f"{status['status']}\n\n"
            "Set the `GROQ_API_KEY` environment variable or add it as a "
            "Secret in your Hugging Face Space settings."
        )

    # Display available models info
    st.info("""
    **Available Models (powered by Groq):**
    - **gpt-oss-20b**: GPT OSS 20B — fast and efficient (recommended)
    - **gpt-oss-120b**: GPT OSS 120B — most powerful, complex reasoning
    - **qwen-27b**: Qwen 3.8 27B — balanced performance
    - **allam-7b**: Allam 2 7B — lightweight tasks
    """)

    st.divider()

    # Content generation defaults
    st.subheader("📝 Default Content Settings")

    col1, col2 = st.columns(2)

    with col1:
        default_tone = st.selectbox(
            "Default Tone:",
            TONES,
            index=TONES.index(st.session_state.settings.get_default_tone()),
        )
        st.session_state.settings.set_default_tone(default_tone)

    with col2:
        default_style = st.selectbox(
            "Default Style:",
            STYLES,
            index=STYLES.index(st.session_state.settings.get_default_style()),
        )
        st.session_state.settings.set_default_style(default_style)

    col1, col2 = st.columns(2)

    with col1:
        default_language = st.selectbox(
            "Default Language:",
            list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(
                st.session_state.settings.get_default_language()
            ),
        )
        st.session_state.settings.set_default_language(default_language)

    with col2:
        export_format = st.selectbox(
            "Default Export Format:",
            ["txt", "docx", "pdf"],
            index=["txt", "docx", "pdf"].index(
                st.session_state.settings.get_export_format()
            ),
        )
        st.session_state.settings.set_export_format(export_format)

    st.divider()

    # Feature settings
    st.subheader("✨ Feature Settings")

    auto_save = st.checkbox(
        "Auto-save generation history",
        value=st.session_state.settings.is_auto_save_enabled(),
    )
    st.session_state.settings.enable_auto_save(auto_save)

    session_memory = st.checkbox(
        "Enable session memory (favorites, quick access)",
        value=st.session_state.settings.is_session_memory_enabled(),
    )
    st.session_state.settings.enable_session_memory(session_memory)

    st.divider()

    # Theme settings
    st.subheader("🎨 Appearance")

    theme = st.selectbox(
        "Theme:",
        ["light", "dark"],
        index=0 if st.session_state.settings.get_theme() == "light" else 1,
    )
    st.session_state.settings.set_theme(theme)

    st.info("Note: Theme changes will take effect on next refresh (F5)")

    st.divider()

    # Storage and cache
    st.subheader("💾 Storage & Cache")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.db.clear_history()
            st.success("✅ History cleared!")
            st.rerun()

    with col2:
        if st.button("🔄 Reset Settings", use_container_width=True):
            st.session_state.settings.reset_to_defaults()
            st.success("✅ Settings reset to defaults!")
            st.rerun()

    st.divider()

    # About
    st.subheader("ℹ️ About")

    st.markdown("""
**ContentForge - AI Content Generator**
            
            Version: 2.0.0
            
            Forge your content with AI. Powerfully.
    
    **Features:**
    - Generate blogs, emails, social media posts, and more
    - Powered by Groq API (ultra-fast cloud inference)
    - Export to multiple formats (TXT, DOCX, PDF)
    - Template library with prebuilt templates
    - Full generation history
    - Session memory and favorites
    
    **Tech Stack:**
    - Streamlit (Frontend)
    - Groq API (LLM Inference)
    - SQLite (Database)
    
    **Requirements:**
    - A free Groq API key (https://console.groq.com)
    - Python 3.8+
    """)


# ============================================================================
# MAIN APP LAYOUT
# ============================================================================

def main():
    """Main app function"""

    # Sidebar navigation
    with st.sidebar:
        st.title("🔥 ContentForge")

        selected = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Generator",
                "History",
                "Templates",
                "Export",
                "Settings",
            ],
            index=[
                "Dashboard",
                "Generator",
                "History",
                "Templates",
                "Export",
                "Settings",
            ].index(st.session_state.selected_page),
        )

        # Update session state with selected page
        st.session_state.selected_page = selected

        st.sidebar.divider()

        # Favorites in sidebar
        favorites = st.session_state.session_memory.get_favorites()
        if favorites:
            st.sidebar.subheader("⭐ Session Favorites")
            for i, fav in enumerate(favorites[:3]):
                if st.sidebar.button(f"Favorite {i+1}...", use_container_width=True):
                    st.session_state.generated_outputs = [fav]
                    st.session_state.current_output_index = 0

        st.sidebar.divider()

        # Session stats
        stats = st.session_state.session_memory.get_stats()
        st.sidebar.markdown("""
        **Session Stats:**
        """)
        st.sidebar.metric("Generated", stats["generation_count"])
        st.sidebar.metric("Words", stats["total_words_generated"])

    # Main content area
    if st.session_state.selected_page == "Dashboard":
        display_dashboard()

    elif st.session_state.selected_page == "Generator":
        display_generator()

    elif st.session_state.selected_page == "History":
        display_history()

    elif st.session_state.selected_page == "Templates":
        display_templates()

    elif st.session_state.selected_page == "Export":
        display_export()

    elif st.session_state.selected_page == "Settings":
        display_settings()


if __name__ == "__main__":
    main()
