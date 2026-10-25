
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="우리 회사 챗봇",
    page_icon="💬"
)

# 챗봇 제목
st.title("우리 회사 챗봇")
st.write("안녕하세요! 무엇을 도와드릴까요?")

# 챗봇 답변 함수
def chatbot_response(message):
    message = message.strip().lower()

    if "안녕" in message:
        return "안녕하세요! 반갑습니다 😊"

    elif "이름" in message:
        return "저는 우리 회사 챗봇입니다!"

    elif "회사" in message:
        return "회사에 관한 질문을 남겨주세요."

    elif "고마워" in message or "감사" in message:
        return "천만에요! 또 궁금한 점이 있으면 질문해주세요."

    else:
        return f"'{message}'라고 말씀하셨군요! 아직 해당 질문에 대한 답변은 준비되지 않았습니다."

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 메시지 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    
    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # 챗봇 답변 생성
    response = chatbot_response(prompt)

    # 챗봇 답변 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistpant"):
        st.write(response)
