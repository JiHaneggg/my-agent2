
import re
import requests
import streamlit as st

from PIL import Image, ImageDraw, ImageFont


# ==========================================
# 1. Streamlit 설정
# ==========================================

st.set_page_config(
    page_title="FX CHAT | 환율 조회 챗봇",
    page_icon="💱",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ==========================================
# 2. Binance 스타일 CSS
# ==========================================

st.markdown("""
<style>
:root {
    --bg: #0b0e11;
    --card: #1e2329;
    --border: #2b3139;
    --yellow: #fcd535;
    --text: #eaecef;
    --muted: #929aa5;
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

.block-container {
    max-width: 900px !important;
    padding-top: 5.5rem !important;
    padding-bottom: 7rem !important;
    margin: 0 auto !important;
}

.fx-title {
    color: var(--yellow);
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.fx-subtitle {
    color: var(--muted);
    font-size: 12px;
    letter-spacing: 1px;
    margin-top: 6px;
}

.fx-welcome {
    text-align: center;
    padding: 65px 10px 35px;
}

.fx-welcome h2 {
    color: #ffffff;
    font-size: 32px;
}

.fx-welcome p {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.8;
}

/* 채팅 메시지 */
[data-testid="stChatMessage"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 18px !important;
    margin-bottom: 12px !important;
}

[data-testid="stChatMessage"] p {
    color: var(--text);
    line-height: 1.7;
}

[data-testid="stChatMessage"] h3 {
    color: var(--yellow) !important;
}

[data-testid="stChatMessage"] img {
    border-radius: 50%;
}

/* 채팅 입력창 */
[data-testid="stChatInput"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
}

[data-testid="stChatInput"] button {
    color: var(--yellow) !important;
}

/* 일반 버튼 */
div.stButton > button {
    background: var(--card);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    min-height: 42px;
}

div.stButton > button:hover {
    color: var(--yellow);
    border-color: var(--yellow);
}

a {
    color: var(--yellow) !important;
}

/* 만원 지폐 로딩 */
.money-loading {
    height: 125px;
    position: relative;
    overflow: hidden;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
}

.money-runner {
    position: absolute;
    left: -170px;
    top: 25px;
    animation: money-run 2.7s linear infinite;
}

.money-bill {
    width: 150px;
    height: 66px;
    box-sizing: border-box;
    padding: 9px;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #a3bd8d;
    border: 2px solid #d0dfb5;
    border-radius: 6px;
    box-shadow: 0 5px 14px #0006;
    animation: money-jump .42s
        ease-in-out infinite alternate;
}

.bill-seal {
    width: 40px;
    height: 40px;
    border: 2px solid #e8f1cc;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 800;
    color: #214b37;
}

.bill-info {
    display: flex;
    flex-direction: column;
    color: #173c29;
}

.bill-info span {
    font-size: 12px;
    font-weight: 700;
}

.bill-info strong {
    font-size: 17px;
    font-weight: 800;
}

.loading-text {
    position: absolute;
    bottom: 10px;
    width: 100%;
    text-align: center;
    color: var(--muted);
    font-size: 12px;
}

@keyframes money-run {
    from { left: -170px; }
    to { left: calc(100% + 15px); }
}

@keyframes money-jump {
    from {
        transform: translateY(14px) rotate(-8deg);
    }
    to {
        transform: translateY(-12px) rotate(9deg);
    }
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 5rem !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    .fx-title {
        font-size: 23px;
    }

    .fx-welcome h2 {
        font-size: 26px;
    }
}

@media (prefers-reduced-motion: reduce) {
    .money-runner,
    .money-bill {
        animation: none;
    }

    .money-runner {
        left: calc(50% - 75px);
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 코인 프로필
# ==========================================

def make_coin(symbol, background, foreground):
    image = Image.new(
        "RGBA", (96, 96), (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(image)

    draw.ellipse(
        (4, 4, 92, 92),
        fill=background,
        outline="#F0B90B",
        width=4
    )

    draw.ellipse(
        (15, 15, 81, 81),
        outline=foreground,
        width=2
    )

    font = ImageFont.load_default()
    display_symbol = symbol

    for path in [
        "C:/Windows/Fonts/malgunbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]:
        try:
            font = ImageFont.truetype(path, 46)
            break
        except OSError:
            continue
    else:
        if symbol == "₩":
            display_symbol = "W"

    draw.text(
        (48, 47),
        display_symbol,
        fill=foreground,
        font=font,
        anchor="mm"
    )

    return image


USER_AVATAR = make_coin(
    "$", "#2b3139", "#fcd535"
)

BOT_AVATAR = make_coin(
    "₩", "#fcd535", "#181a20"
)


# ==========================================
# 4. 만원 지폐 로딩 애니메이션
# ==========================================

LOADING_HTML = """
<div class="money-loading">
    <div class="money-runner">
        <div class="money-bill">
            <div class="bill-seal">₩</div>
            <div class="bill-info">
                <span>만원</span>
                <strong>₩10,000</strong>
            </div>
        </div>
    </div>
    <div class="loading-text">
        환율을 조회하고 있습니다...
    </div>
</div>
"""


# ==========================================
# 5. 통화 정보
# ==========================================

CURRENCIES = {
    "미국달러": "USD",
    "달러": "USD",
    "불": "USD",
    "원화": "KRW",
    "한국원": "KRW",
    "원": "KRW",
    "엔화": "JPY",
    "엔": "JPY",
    "유로": "EUR",
    "파운드": "GBP",
    "위안화": "CNY",
    "위안": "CNY",
    "프랑": "CHF",
    "호주달러": "AUD",
    "캐나다달러": "CAD",
    "usd": "USD",
    "krw": "KRW",
    "jpy": "JPY",
    "eur": "EUR",
    "gbp": "GBP",
    "cny": "CNY",
    "chf": "CHF",
    "aud": "AUD",
    "cad": "CAD",
}

CURRENCY_NAMES = {
    "USD": "미국 달러",
    "KRW": "대한민국 원",
    "JPY": "일본 엔",
    "EUR": "유로",
    "GBP": "영국 파운드",
    "CNY": "중국 위안",
    "CHF": "스위스 프랑",
    "AUD": "호주 달러",
    "CAD": "캐나다 달러",
}


# ==========================================
# 6. Frankfurter 환율 API
# ==========================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_exchange_rate(base, target):
    if base == target:
        return 1.0, "동일 통화"

    url = (
        "https://api.frankfurter.dev/v2/rate/"
        f"{base}/{target}"
    )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

    return float(data["rate"]), data["date"]


# ==========================================
# 7. 질문에서 금액 및 통화 추출
# ==========================================

def parse_question(question):
    text = question.lower()

    # 숫자와 단위 추출
    amount_match = re.search(
        r"(\d[\d,]*(?:\.\d+)?)\s*(억|만|천)?",
        text
    )

    if amount_match:
        amount = float(
            amount_match.group(1).replace(",", "")
        )

        unit = amount_match.group(2)

        multipliers = {
            "천": 1000,
            "만": 10000,
            "억": 100000000
        }

        amount *= multipliers.get(unit, 1)
    else:
        amount = 1.0

    # 통화 이름 검색
    names = sorted(
        CURRENCIES.keys(),
        key=len,
        reverse=True
    )

    pattern = "|".join(
        re.escape(name) for name in names
    )

    matches = list(
        re.finditer(pattern, text)
    )

    if not matches:
        if "환율" in text:
            return amount, "USD", "KRW"
        return None

    found = [
        (match, CURRENCIES[match.group()])
        for match in matches
    ]

    # '원화로', '달러로'처럼 목표 통화 탐색
    target_matches = []

    for match, code in found:
        following = text[match.end():]

        if re.match(r"\s*(?:으로|로|에)", following):
            target_matches.append((match, code))

    if target_matches:
        target_match, target = target_matches[-1]

        sources = [
            code
            for match, code in found
            if match != target_match
        ]

        if sources:
            base = sources[0]
        else:
            base = "USD" if target == "KRW" else "KRW"

    else:
        base = found[0][1]

        other_codes = [
            code for _, code in found[1:]
            if code != base
        ]

        if other_codes:
            target = other_codes[0]
        else:
            target = "USD" if base == "KRW" else "KRW"

    return amount, base, target


# ==========================================
# 8. 챗봇 답변 생성
# ==========================================

def get_answer(question):
    text = question.strip().lower()

    # 간단한 대화
    if text in ["안녕", "안녕하세요", "ㅎㅇ", "하이"]:
        return (
            "안녕하세요! 💱 FX CHAT입니다.\n\n"
            "환율에 대해 자유롭게 질문해주세요.\n\n"
            "예: **100달러는 원화로 얼마야?**"
        )

    if text in ["고마워", "감사합니다", "감사해"]:
        return "도움이 되었다니 기쁩니다! 다른 환율도 궁금하신가요?"

    if text in ["도움말", "사용법", "뭐할수있어?"]:
        return (
            "저는 환율 조회 전문 챗봇입니다.\n\n"
            "- 100달러는 원화로 얼마야?\n"
            "- 1000엔을 원화로 바꿔줘\n"
            "- 오늘 달러 환율 알려줘\n"
            "- 50유로를 달러로 환산해줘\n\n"
            "Frankfurter API의 최신 제공 환율을 사용합니다."
        )

    parsed = parse_question(question)

    if parsed is None:
        return (
            "저는 환율 조회 전문 챗봇입니다.\n\n"
            "현재는 일반적인 AI 질문보다는 "
            "**환율 조회 및 통화 변환**을 도와드릴 수 있어요.\n\n"
            "예: 100달러는 원화로 얼마야?"
        )

    amount, base, target = parsed

    try:
        rate, date = get_exchange_rate(
            base, target
        )

        converted = amount * rate

        # 원화와 엔화는 정수 중심 표시
        if target in ["KRW", "JPY"]:
            converted_text = f"{converted:,.0f}"
        else:
            converted_text = f"{converted:,.2f}"

        return (
            "환율 조회 결과입니다.\n\n"
            f"### {amount:,.2f} {base} "
            f"= {converted_text} {target}\n\n"
            "---\n\n"
            f"**기준 통화:** {CURRENCY_NAMES[base]}\n\n"
            f"**변환 통화:** {CURRENCY_NAMES[target]}\n\n"
            f"**적용 환율:** "
            f"1 {base} = {rate:,.4f} {target}\n\n"
            f"**환율 기준일:** {date}\n\n"
            "**출처:** "
            "[Frankfurter API](https://frankfurter.dev/)\n\n"
            "※ 실제 은행 환전 환율과 차이가 있을 수 있습니다."
        )

    except requests.RequestException:
        return (
            "현재 환율 서버에 연결할 수 없습니다.\n\n"
            "잠시 후 다시 시도해주세요."
        )

    except (ValueError, KeyError, TypeError):
        return (
            "환율 데이터를 처리하는 중 문제가 발생했습니다."
        )


# ==========================================
# 9. Streamlit 대화 기록
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================
# 10. 상단 헤더
# ==========================================

left, right = st.columns(
    [4, 1],
    vertical_alignment="center"
)

with left:
    st.markdown(
        '<div class="fx-title">◆ FX CHAT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="fx-subtitle">'
        'CURRENCY EXCHANGE ASSISTANT'
        '</div>',
        unsafe_allow_html=True
    )

with right:
    if st.button(
        "새 대화",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

st.divider()


# ==========================================
# 11. 환영 화면
# ==========================================

if not st.session_state.messages:
    st.markdown("""
    <div class="fx-welcome">
        <h2>환율이 궁금하신가요?</h2>
        <p>
            복잡한 계산 없이 질문만 입력하세요.<br>
            원하는 통화의 기준 환율을 조회해드립니다.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 12. 이전 대화 출력
# ==========================================

for message in st.session_state.messages:
    avatar = (
        USER_AVATAR
        if message["role"] == "user"
        else BOT_AVATAR
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])


# ==========================================
# 13. 사용자 입력
# ==========================================

prompt = st.chat_input(
    "환율에 대해 무엇이든 질문하세요..."
)

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message(
        "user",
        avatar=USER_AVATAR
    ):
        st.markdown(prompt)

    with st.chat_message(
        "assistant",
        avatar=BOT_AVATAR
    ):
        loading = st.empty()

        # 만원 지폐 애니메이션
        loading.markdown(
            LOADING_HTML,
            unsafe_allow_html=True
        )

        try:
            answer = get_answer(prompt)
        except Exception:
            answer = (
                "요청을 처리하는 중 오류가 발생했습니다."
            )
        finally:
            loading.empty()

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ==========================================
# 14. 하단 안내
# ==========================================

st.caption(
    "FX CHAT · Powered by Frankfurter API · "
    "실제 환전 금액은 은행별로 다를 수 있습니다."
)
