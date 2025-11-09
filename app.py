# 통합 앱 예제
import streamlit as st
import random
import time

st.set_page_config(page_title="청소년 도박 예방 플랫폼", layout="wide")

# ------------------------------
# 초기 세션 상태
# ------------------------------
if "balance" not in st.session_state:
    st.session_state.balance = 1000

if "card_state" not in st.session_state:
    st.session_state.card_state = [False] * 16
if "card_values" not in st.session_state:
    fruits = ["🍎","🍌","🍊","🍇","🍓","🥝","🍍","🍒"]
    st.session_state.card_values = fruits*2
    random.shuffle(st.session_state.card_values)

if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_choices" not in st.session_state:
    st.session_state.quiz_choices = [None]*5
if "survey_submitted" not in st.session_state:
    st.session_state.survey_submitted = False

# ------------------------------
# 앱 사이드 메뉴
# ------------------------------
menu = st.sidebar.selectbox("메뉴", ["홈","게임","설문","교육","퀴즈","위기연락"])

st.title("청소년 도박 예방 및 교육 플랫폼")

# ------------------------------
# 홈
# ------------------------------
if menu == "홈":
    st.write("환영합니다! 청소년 도박 위험을 예방하고 건강한 습관을 형성하는 플랫폼입니다.")
    st.write(f"현재 포인트: {st.session_state.balance}원")

# ------------------------------
# 게임
# ------------------------------
elif menu == "게임":
    st.subheader("🎰 슬롯머신")
    if st.button("슬롯머신 돌리기 (-50원)"):
        st.session_state.balance -= 50
        result = [random.choices(["🍎","🍌","🍊","🍇","🍓","🥝","🍍","🍒"], k=3)[0] for _ in range(3)]
        st.write("결과:", result)
        if result[0] == result[1] == result[2]:
            st.session_state.balance += 1000
            st.success("🎉 3개 일치! 1000원 획득!")
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            st.session_state.balance += 0
            st.info("2개 일치! 보상 없음.")
        else:
            st.info("꽝!")
    st.write(f"현재 포인트: {st.session_state.balance}원")

    st.subheader("🃏 카드 뒤집기")
    cols = st.columns(4)
    for i in range(16):
        with cols[i%4]:
            if st.button(st.session_state.card_values[i] if not st.session_state.card_state[i] else "✅", key=f"card_{i}"):
                st.session_state.card_state[i] = True
    if all(st.session_state.card_state):
        st.session_state.balance += 200
        st.success("모든 카드 맞추기 완료! 200원 획득!")
        st.session_state.card_state = [False]*16
        random.shuffle(st.session_state.card_values)
    st.write(f"현재 포인트: {st.session_state.balance}원")

# ------------------------------
# 설문
# ------------------------------
elif menu == "설문":
    st.subheader("📋 청소년 도박 선별 설문")
    if st.session_state.survey_submitted:
        st.info("이미 제출하였습니다.")
    else:
        survey = {}
        survey["도박 경험"] = st.radio("최근 1년 내 도박 경험이 있나요?", ["없음","1~5회","6~10회","10회 이상"])
        survey["온라인 결제 사용"] = st.radio("온라인 결제를 자주 사용하나요?", ["전혀 없음","가끔","자주","매일"])
        if st.button("제출"):
            st.session_state.survey_submitted = True
            st.success("설문 제출 완료!")
            st.write("설문 결과:", survey)

# ------------------------------
# 교육
# ------------------------------
elif menu == "교육":
    st.subheader("📖 디지털 리터러시 및 금융교육")
    lessons = [
        "도박은 장기적으로 손해가 나는 구조입니다.",
        "자기 통제와 계획이 도박 중독 예방에 중요합니다.",
        "온라인 결제와 게임 속 과금 습관을 기록하고 점검하세요.",
    ]
    st.session_state.lesson_idx = st.session_state.get("lesson_idx",0)
    st.write(lessons[st.session_state.lesson_idx])
    if st.session_state.lesson_idx < len(lessons)-1:
        if st.button("다음"):
            st.session_state.lesson_idx +=1
    else:
        st.success("모든 교육 내용 완료! 🎓")

# ------------------------------
# 퀴즈
# ------------------------------
elif menu == "퀴즈":
    st.subheader("📝 교육 퀴즈")
    QUESTIONS = [
        {"q":"도박은 장기적으로 손해인가요?","opts":["예","아니오"],"answer":0},
        {"q":"자기 통제가 중요합니까?","opts":["예","아니오"],"answer":0},
        {"q":"온라인 결제 기록 점검이 도움이 되나요?","opts":["예","아니오"],"answer":0},
        {"q":"교육을 모두 완료해야 퀴즈를 풀 수 있나요?","opts":["예","아니오"],"answer":0},
        {"q":"모든 카드 맞추기 완료 후 보상을 받나요?","opts":["예","아니오"],"answer":0}
    ]
    if not st.session_state.quiz_answered:
        for i,q in enumerate(QUESTIONS):
            choice_idx = st.radio(
                q["q"],
                options=list(range(len(q["opts"]))),
                format_func=lambda x: q["opts"][x],
                index=0 if st.session_state.quiz_choices[i] is None else st.session_state.quiz_choices[i],
                key=f"radio_{i}"
            )
            st.session_state.quiz_choices[i] = choice_idx
        if st.button("제출"):
            score = sum([1 if st.session_state.quiz_choices[i]==q["answer"] else 0 for i,q in enumerate(QUESTIONS)])
            st.session_state.quiz_score = score
            st.session_state.balance += score*50
            st.session_state.quiz_answered = True
            st.success(f"퀴즈 완료! {score}/5 맞음. 포인트 +{score*50}원")
    else:
        st.info(f"이미 퀴즈를 제출했습니다! 점수: {st.session_state.quiz_score}/5")

# ------------------------------
# 위기연락
# ------------------------------
elif menu == "위기연락":
    st.subheader("📞 위기 상황 연락")
    st.write("위기 상황 시 즉시 연락 가능한 버튼:")
    if st.button("친구에게 연락"):
        st.success("친구에게 연락 메시지를 전송했습니다!")
    if st.button("부모에게 연락"):
        st.success("보호자에게 연락 메시지를 전송했습니다!")
