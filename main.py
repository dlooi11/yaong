from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="고양이 택배",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .stApp {
        background: linear-gradient(180deg, #1d1230 0%, #302044 100%);
        color: #fff4e0;
      }
      .block-container {
        max-width: 1120px;
        padding-top: 1.5rem;
        padding-bottom: 1rem;
      }
      h1, h2, p { color: #fff4e0; }
      div[data-testid="stMarkdownContainer"] p { line-height: 1.65; }
      .game-frame {
        border: 1px solid rgba(255, 210, 122, .45);
        border-radius: 14px;
        overflow: hidden;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("고양이 택배")
st.caption("노을 지는 골목, 오늘도 택배를 배달해요.")

with st.container(border=True):
    st.markdown("**조작 방법**")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("- **이동:** ← → 또는 A / D")
        st.markdown("- **점프:** Space / ↑ / W")
        st.markdown("- **2단 점프:** 공중에서 점프 한 번 더")
    with c2:
        st.markdown("- **슬라이딩:** Left Shift 또는 S / ↓")
        st.markdown("- **벽 점프:** 벽에 붙어서 점프")
        st.markdown("- **일시정지:** Esc")

game_file = Path(__file__).with_name("고양이_택배.html")
if not game_file.exists():
    st.error("게임 파일을 찾을 수 없습니다. app.py와 고양이_택배.html을 같은 폴더에 두세요.")
    st.stop()

html = game_file.read_text(encoding="utf-8")

st.markdown('<div class="game-frame">', unsafe_allow_html=True)
components.html(
    html,
    height=610,
    scrolling=False,
)
st.markdown("</div>", unsafe_allow_html=True)

st.caption("게임이 표시되지 않으면 인터넷 연결을 확인해 주세요. Phaser 라이브러리를 CDN에서 불러옵니다.")
