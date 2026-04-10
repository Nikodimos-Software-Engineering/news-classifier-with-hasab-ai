import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


st.set_page_config(page_title="News Classifier", page_icon="📰", layout="wide")

ENGLISH_CATEGORY_MAP = {
    'tech': 'Technology', 'business': 'Business', 'sport': 'Sports',
    'entertainment': 'Entertainment', 'politics': 'Politics'
}

LANGUAGE_COLORS = {'Amharic': '#10b981', 'English': '#3b82f6', 'Mixed': '#f59e0b'}
CATEGORY_COLORS = {
    'Technology': '#3b82f6', 'Business': '#10b981', 'Sports': '#f97316',
    'Entertainment': '#8b5cf6', 'Politics': '#ef4444', 'ስፖርት': '#f97316',
    'መዝናኛ': '#8b5cf6', 'ሀገር አቀፍ ዜና': '#06b6d4', 'ቢዝነስ': '#10b981',
    'ዓለም አቀፍ ዜና': '#06b6d4', 'ፖለቲካ': '#ef4444'
}

def format_category(category, model_used):
    if model_used == 'English Model':
        return ENGLISH_CATEGORY_MAP.get(category, category.title())
    return category

st.markdown("""
<style>
    .category-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 100px;
        font-weight: 600;
        font-size: 1.1rem;
        color: white;
    }
    .lang-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 100px;
        font-weight: 500;
        font-size: 0.85rem;
        color: white;
    }
    .confidence-box {
        background: #f0fdf4;
        padding: 10px 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #dcfce7;
    }
    .explanation-box {
        background: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 15px 0;
    }
    .warning-box {
        background: #fefce8;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("News Classifier")
st.caption("Paste any news article to classify it and get an explanation from Groq's Llama 3 model.")
st.divider()

headline = st.text_input("Headline", placeholder="e.g., Apple releases new iPhone with advanced AI features")
article_body = st.text_area("Article Body", placeholder="Paste the full article text here...", height=200)
source_url = st.text_input("Source URL (optional)", placeholder="https://example.com/article")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    classify_button = st.button("Classify Article", type="primary", use_container_width=True)

if classify_button:
    if not article_body.strip():
        st.error("Please enter article body text.")
        st.stop()
    
    with st.spinner("Analyzing article..."):
        try:
            payload = {
                "headline": headline,
                "article_body": article_body,
                "source_url": source_url or None
            }
            response = requests.post(f"{BACKEND_URL}/classify", json=payload, timeout=35)
            
            if response.status_code == 200:
                result = response.json()
                
                st.success("Classification Complete")
                st.divider()
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Predicted Category**")
                    cat_display = format_category(result['category'], result['model_used'])
                    color = CATEGORY_COLORS.get(cat_display, '#6b7280')
                    st.markdown(f'<div class="category-badge" style="background:{color}">{cat_display}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Confidence Score**")
                    confidence_pct = f"{result['confidence']:.1f}%"
                    st.markdown(f"""
                    <div class="confidence-box">
                        <div style="font-size:1.5rem; font-weight:700; color:#059669">{confidence_pct}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("**Explanation**")
                st.markdown(f'<div class="explanation-box">{result["explanation"]}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Language**")
                    lang_color = LANGUAGE_COLORS.get(result['language_detected'], '#6b7280')
                    st.markdown(f'<span class="lang-badge" style="background:{lang_color}">{result["language_detected"]}</span>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Model**")
                    st.markdown(f"`{result['model_used']}`")
                
                with col3:
                    if result.get('source_url'):
                        st.markdown("**Source**")
                        st.markdown(f"[Open Link]({result['source_url']})", unsafe_allow_html=True)
                
                if result.get('mixed_warning'):
                    st.markdown(f"""
                    <div class="warning-box">
                        <strong>Mixed Language Detected</strong><br>
                        This article contains mixed Amharic and English content. 
                        It was routed to the <strong>{result['model_used']}</strong> for classification.
                    </div>
                    """, unsafe_allow_html=True)
            
            elif response.status_code == 422:
                st.error("Validation Error: Please check your inputs.")
            else:
                st.error(f"Server Error (HTTP {response.status_code})")
        
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Make sure FastAPI is running.")
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.caption("Groq Llama 3 | FastAPI | Scikit-learn | Streamlit")