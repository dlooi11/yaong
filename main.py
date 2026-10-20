
import time
import streamlit as st
from streamlit_keypress import key_press_events

st.set_page_config(
    page_title="고양이 택배",
    page_icon="🐱",
    layout="wide",
)

# -------------------------
# 레벨 설정
# -------------------------
LEVELS = [
    {
        "name": "1. 골목 입문",
        "time": 50,
        "width": 48,
        "start": (2, 11),
        "goal": (42, 10),
        "platforms": [
            (0, 14, 36), (39, 14, 9),
            (12, 12, 2), (20, 12, 2),
            (28, 12, 3),
        ],
        "checks": [(23, 13)],
    },
    {
        "name": "2. 지붕 코스",
        "time": 70,
        "width": 70,
        "start": (2, 8),
        "goal": (63, 5),
        "platforms": [
            (0, 11, 10), (13, 10, 8),
            (24, 12, 7), (31, 11, 3),
            (34, 9, 6), (43, 11, 6),
            (52, 10, 6), (61, 8, 9),
        ],
        "checks": [(27, 11), (45, 10), (55, 9)],
    },
    {
        "name": "3. 시장 거리",
        "time": 85,
        "width": 80,
        "start": (2, 11),
        "goal": (73, 5),
        "platforms": [
            (0, 14, 20), (20, 8, 5),
            (28, 11, 5), (43, 11, 17),
            (63, 8, 17),
        ],
        "checks": [
            (14, 13), (30, 10), (45, 10), (57, 10)
        ],
    },
]

STORIES = [
    (
        "파란 대문 할머니",
        "매일 오던 택배 고양이구나. 우유 한 잔 줄까?",
    ),
    (
        "꼬마 민수",
        "잃어버린 줄 알았던 편지가 도착했어요!",
    ),
    (
        "시장 국밥집 이모",
        "천막 위에서 뛰면 어떡하니! 이거나 먹고 가.",
    ),
]

HEIGHT = 17
VIEW_WIDTH = 30


# -------------------------
# 게임 초기화
# -------------------------
def new_game(level_index=0):
    level = LEVELS[level_index]
    x, y = level["start"]

    return {
        "level": level_index,
        "x": x,
        "y": y,
        "checkpoint": (x, y),
        "air_jump": 1,
        "started": time.time(),
        "status": "play",
        "message": "",
        "stars": 0,
    }


if "game" not in st.session_state:
    st.session_state.game = new_game()

game = st.session_state.game
level = LEVELS[game["level"]]


# -------------------------
# 화면 디자인
# -------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            180deg, #1d1230, #493052, #9b526d
        );
        color: #fff4e0;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }

    h1, h2, h3, p, label {
        color: #fff4e0;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #ffd27a;
        min-height: 45px;
        font-weight: bold;
    }

    .game-map {
        white-space: pre;
        overflow-x: auto;
        background: rgba(22, 13, 35, .85);
        border: 1px solid #76536f;
        border-radius: 14px;
        padding: 16px;
        line-height: 1.5;
        font-family: monospace;
        font-size: 17px;
        color: #fff4e0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🐱 고양이 택배")
st.write("노을 지는 골목, 오늘도 택배를 배달해요.")

with st.expander("🎮 조작 방법", expanded=True):
    st.markdown(
        """
        - **← / A** : 왼쪽 이동
        - **→ / D** : 오른쪽 이동
        - **↑ / W / Space** : 점프
        - **Shift** : 슬라이딩

        키보드 입력이 동작하지 않으면 아래 화면 버튼을 사용하세요.
        """
    )


# -------------------------
# 타이머
# -------------------------
elapsed = int(time.time() - game["started"])
remaining = max(0, level["time"] - elapsed)

if game["status"] == "play" and remaining <= 0:
    game["status"] = "fail"

col1, col2, col3 = st.columns(3)

col1.metric("현재 코스", level["name"])
col2.metric("남은 시간", f"{remaining}초")
col3.metric(
    "택배 상태",
    "📦 배달 중"
    if game["status"] == "play"
    else "🏁 종료",
)


# -------------------------
# 발판 판정
# -------------------------
def is_platform(x, y):
    for px, py, width in level["platforms"]:
        if px <= x < px + width and y == py - 1:
            return True
    return False


# -------------------------
# 지도 그리기
# -------------------------
def draw_map():
    start = max(
        0,
        min(
            game["x"] - VIEW_WIDTH // 2,
            level["width"] - VIEW_WIDTH,
        ),
    )

    end = min(start + VIEW_WIDTH, level["width"])
    rows = []

    for y in range(HEIGHT):
        row = []

        for x in range(start, end):
            cell = "　"

            # 바닥
            if y >= HEIGHT - 3:
                cell = "🟪"

            # 발판
            for px, py, width in level["platforms"]:
                if px <= x < px + width and y == py:
                    cell = "🧱"

            # 체크포인트
            for cx, cy in level["checks"]:
                if x == cx and y == cy:
                    cell = "🚩"

            # 목적지
            gx, gy = level["goal"]
            if gx <= x <= gx + 2 and gy <= y <= gy + 1:
                cell = "🏠"

            # 플레이어와 택배
            if (x, y) == (game["x"], game["y"]):
                cell = "🐱"
            elif (
                x == game["x"] + 1
                and y == game["y"]
                and game["status"] == "play"
            ):
                cell = "📦"

            row.append(cell)

        rows.append("".join(row))

    return "\n".join(rows)


st.subheader("🌇 골목 지도")

st.markdown(
    f'<div class="game-map">{draw_map()}</div>',
    unsafe_allow_html=True,
)

st.caption(
    "🐱 고양이 | 📦 택배 | 🧱 발판 | "
    "🚩 체크포인트 | 🏠 배달 장소"
)

if game["message"]:
    st.info(game["message"])


# -------------------------
# 이동 처리
# -------------------------
def move(action):
    if game["status"] != "play":
        return

    x = game["x"]
    y = game["y"]

    if action == "left":
        x = max(0, x - 2)

    elif action == "right":
        x = min(level["width"] - 1, x + 2)

    elif action == "jump":
        if is_platform(x, y + 1) or y >= HEIGHT - 4:
            y = max(0, y - 3)
            game["air_jump"] = 1

        elif game["air_jump"] > 0:
            y = max(0, y - 2)
            game["air_jump"] -= 1

        else:
            game["message"] = "공중 점프를 모두 사용했어요."

    elif action == "slide":
        x = min(level["width"] - 1, x + 4)

    # 간단한 중력 처리
    if action != "jump":
        if not is_platform(x, y + 1) and y < HEIGHT - 4:
            y += 1
        else:
            game["air_jump"] = 1

    # 체크포인트
    for cx, cy in level["checks"]:
        if x >= cx:
            game["checkpoint"] = (cx, cy)

    # 낙하 시 체크포인트로 복귀
    if y >= HEIGHT - 3:
        x, y = game["checkpoint"]
        game["message"] = "체크포인트에서 다시 시작했어요."

    game["x"] = x
    game["y"] = y

    # 목표 도착
    gx, gy = level["goal"]

    if abs(x - gx) <= 2 and abs(y - gy) <= 2:
        game["status"] = "success"

        ratio = remaining / level["time"]

        if ratio > 0.5:
            game["stars"] = 3
        elif ratio > 0.25:
            game["stars"] = 2
        else:
            game["stars"] = 1

        game["message"] = "택배 배달 성공!"


# -------------------------
# 키보드 입력
# -------------------------
KEY_ACTIONS = {
    "ArrowLeft": "left",
    "Left": "left",
    "a": "left",
    "A": "left",

    "ArrowRight": "right",
    "Right": "right",
    "d": "right",
    "D": "right",

    "ArrowUp": "jump",
    "Up": "jump",
    "w": "jump",
    "W": "jump",
    " ": "jump",
    "Space": "jump",
    "Spacebar": "jump",

    "Shift": "slide",
    "ShiftLeft": "slide",
    "ShiftRight": "slide",
}


# 라이브러리에서 키 이벤트를 가져옵니다.
# 라이브러리 버전에 따라 반환 형식이 다를 수 있습니다.
try:
    pressed_key = key_press_events()
except Exception:
    pressed_key = None

# 키 이벤트가 문자열이거나 이벤트 딕셔너리인 경우를 처리합니다.
if isinstance(pressed_key, dict):
    pressed_key = (
        pressed_key.get("key")
        or pressed_key.get("event")
        or pressed_key.get("code")
    )

if isinstance(pressed_key, str):
    action = KEY_ACTIONS.get(pressed_key)

    if action and game["status"] == "play":
        # 중복 입력 방지
        last_event = (pressed_key, int(time.time() * 2))

        if st.session_state.get("last_key_event") != last_event:
            st.session_state.last_key_event = last_event
            move(action)
            st.rerun()


# -------------------------
# 화면 버튼 조작
# -------------------------
if game["status"] == "play":
    st.subheader("🎮 고양이 움직이기")

    c1, c2, c3, c4 = st.columns(4)

    if c1.button("⬅️ 왼쪽", use_container_width=True):
        move("left")
        st.rerun()

    if c2.button("⬆️ 점프", use_container_width=True):
        move("jump")
        st.rerun()

    if c3.button("➡️ 오른쪽", use_container_width=True):
        move("right")
        st.rerun()

    if c4.button("💨 슬라이딩", use_container_width=True):
        move("slide")
        st.rerun()


# -------------------------
# 성공 화면
# -------------------------
elif game["status"] == "success":
    name, story = STORIES[game["level"]]

    st.success("🎉 배달 완료!")
    st.header("⭐" * game["stars"] + "☆" * (3 - game["stars"]))
    st.subheader(name)
    st.write(story)

    c1, c2 = st.columns(2)

    if game["level"] < len(LEVELS) - 1:
        if c1.button("다음 레벨 ▶", use_container_width=True):
            st.session_state.game = new_game(game["level"] + 1)
            st.rerun()
    else:
        if c1.button("처음으로", use_container_width=True):
            st.session_state.game = new_game(0)
            st.rerun()

    if c2.button("다시 하기", use_container_width=True):
        st.session_state.game = new_game(game["level"])
        st.rerun()


# -------------------------
# 실패 화면
# -------------------------
elif game["status"] == "fail":
    st.error("시간 초과… 😿")
    st.write("택배가 식어버리기 전에 다시 도전해요!")

    if st.button("다시 도전"):
        st.session_state.game = new_game(game["level"])
        st.rerun()
