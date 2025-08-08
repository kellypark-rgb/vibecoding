import streamlit as st
import os
from google import genai
from google.genai import types

# Initialize Gemini client
@st.cache_resource
def get_gemini_client():
    """Initialize and cache the Gemini client"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        st.stop()
    return genai.Client(api_key=api_key)

def generate_korean_poetry(word: str, client) -> str:
    """
    Generate Korean N-line poetry (행시) using Gemini API
    
    Args:
        word: Korean word to create poetry from
        client: Gemini client instance
    
    Returns:
        Generated poetry string
    """
    try:
        # Clean the input word (avoid encoding operations that cause issues)
        clean_word = word.strip()
        
        # Create a detailed prompt for Korean N-line poetry generation
        prompt = "당신은 한국어 행시 전문가입니다. 주어진 단어의 각 글자로 시작하는 행시를 만들어주세요.\n\n"
        prompt += "규칙:\n"
        prompt += f"1. 단어 '{clean_word}'의 각 글자로 시작하는 행시를 만드세요\n"
        prompt += "2. 각 행은 해당 글자를 대괄호로 감싸서 시작해야 합니다 (예: [바], [다])\n"
        prompt += "3. 각 행은 의미있고 아름다운 문장이어야 합니다\n"
        prompt += "4. 전체적으로 통일감 있는 주제나 이야기가 있으면 좋습니다\n"
        prompt += "5. 각 행은 10-20자 정도의 적당한 길이로 만드세요\n\n"
        prompt += f"단어: {clean_word}\n\n"
        prompt += "행시를 만들어주세요:"

        # Use simple string approach instead of types.Content to avoid encoding issues
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "행시 생성에 실패했습니다. 다시 시도해주세요."
            
    except Exception as e:
        error_msg = str(e)
        if "ascii" in error_msg.lower() or "codec" in error_msg.lower():
            return "한글 처리 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        return f"API 오류가 발생했습니다: {error_msg}"

def validate_korean_input(text: str) -> bool:
    """
    Validate if the input contains Korean characters
    
    Args:
        text: Input text to validate
        
    Returns:
        True if text contains Korean characters, False otherwise
    """
    if not text or not text.strip():
        return False
    
    # Check if text contains Korean characters (Hangul)
    korean_chars = [char for char in text if '\uAC00' <= char <= '\uD7A3']
    return len(korean_chars) > 0

def main():
    """Main Streamlit application"""
    
    # Set page configuration
    st.set_page_config(
        page_title="한국어 N행시 생성기",
        page_icon="📝",
        layout="centered"
    )
    
    # App title and description
    st.title("📝 한국어 N행시 생성기")
    st.markdown("**Gemini AI를 활용한 창의적인 행시 생성**")
    st.markdown("---")
    
    # Instructions
    with st.expander("사용법", expanded=False):
        st.markdown("""
        1. 아래 입력란에 한국어 단어를 입력하세요
        2. '행시 생성하기' 버튼을 클릭하세요
        3. AI가 각 글자로 시작하는 아름다운 행시를 만들어드립니다
        
        **예시:**
        - 입력: 바다
        - 출력: [바]람이 불어오는 / [다]정한 마음으로
        """)
    
    # Initialize Gemini client
    try:
        client = get_gemini_client()
    except Exception as e:
        st.error(f"Gemini API 초기화 실패: {str(e)}")
        st.stop()
    
    # Input section
    st.subheader("단어 입력")
    
    # Text input for Korean word
    user_input = st.text_input(
        "행시를 만들 한국어 단어를 입력하세요:",
        placeholder="예: 바다, 사랑, 희망",
        help="2-10자의 한국어 단어를 입력해주세요"
    )
    
    # Input validation and generation button
    col1, col2 = st.columns([3, 1])
    
    with col2:
        generate_button = st.button("행시 생성하기", type="primary", use_container_width=True)
    
    # Display input validation
    if user_input:
        if not validate_korean_input(user_input):
            st.warning("⚠️ 한국어 단어를 입력해주세요.")
        elif len(user_input.strip()) > 10:
            st.warning("⚠️ 10자 이하의 단어를 입력해주세요.")
        elif len(user_input.strip()) < 2:
            st.warning("⚠️ 2자 이상의 단어를 입력해주세요.")
    
    # Generate poetry when button is clicked
    if generate_button:
        if not user_input or not user_input.strip():
            st.error("단어를 입력해주세요.")
        elif not validate_korean_input(user_input):
            st.error("한국어 단어를 입력해주세요.")
        elif len(user_input.strip()) > 10:
            st.error("10자 이하의 단어를 입력해주세요.")
        elif len(user_input.strip()) < 2:
            st.error("2자 이상의 단어를 입력해주세요.")
        else:
            # Clean the input
            clean_word = user_input.strip()
            
            # Show loading state
            with st.spinner(f"'{clean_word}' 행시를 생성하고 있습니다..."):
                # Generate poetry
                poetry = generate_korean_poetry(clean_word, client)
            
            # Display results
            st.subheader("생성된 행시")
            
            # Create a nice container for the poetry
            with st.container():
                st.markdown("---")
                
                # Display the word
                st.markdown(f"**주제어:** {clean_word}")
                st.markdown("")
                
                # Display the generated poetry
                if poetry and not poetry.startswith("행시 생성에 실패") and not poetry.startswith("API 오류"):
                    # Display poetry with nice formatting
                    poetry_lines = poetry.split('\n')
                    for line in poetry_lines:
                        if line.strip():
                            st.markdown(f"**{line.strip()}**")
                    
                    st.markdown("---")
                    st.success("✅ 행시가 성공적으로 생성되었습니다!")
                    
                    # Option to generate another one
                    if st.button("다른 행시 생성하기", key="regenerate"):
                        st.rerun()
                        
                else:
                    st.error(poetry)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Powered by Google Gemini AI"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
