import streamlit as st

st.set_page_config(page_title="업무 우선순위 관리", page_icon="📋")

# 1. 우선순위 계산 함수
def 우선순위_계산(중요도, 긴급도):
    점수 = 중요도 * 긴급도

    if 점수 >= 16:
        등급 = "최우선"
    elif 점수 >= 9:
        등급 = "일반"
    else:
        등급 = "낮음"

    return 점수, 등급


# 2. 화면 제목
st.title("📋 업무 우선순위 관리")
st.write("중요도와 긴급도를 선택해 업무의 우선순위를 관리하세요.")

# 3. session_state로 업무 목록 유지
if "업무목록" not in st.session_state:
    st.session_state["업무목록"] = []

if "다음번호" not in st.session_state:
    st.session_state["다음번호"] = 1

# 4. 업무 입력 화면
with st.form("업무입력", clear_on_submit=True):
    업무명 = st.text_input("업무명", placeholder="예: 주간 보고서 작성")

    중요도 = st.selectbox(
        "중요도 (1~5)", [1, 2, 3, 4, 5], index=2
    )

    긴급도 = st.selectbox(
        "긴급도 (1~5)", [1, 2, 3, 4, 5], index=2
    )

    등록 = st.form_submit_button("업무 추가")

# 5. 업무 추가 버튼 처리
if 등록:
    이름 = 업무명.strip()

    # 빈 업무명 또는 공백만 입력한 경우
    if not 이름:
        st.error("업무명을 입력해 주세요.")

    else:
        점수, 등급 = 우선순위_계산(중요도, 긴급도)

        새업무 = {
            "번호": st.session_state["다음번호"],
            "업무명": 이름,
            "중요도": 중요도,
            "긴급도": 긴급도,
            "점수": 점수,
            "우선순위": 등급
        }

        st.session_state["업무목록"].append(새업무)
        st.session_state["다음번호"] += 1

        st.success(f"'{이름}' 업무를 등록했습니다.")

# 6. 등록된 업무 목록 표시
st.subheader("등록된 업무 목록")

if not st.session_state["업무목록"]:
    st.info("등록된 업무가 없습니다. 위에서 업무를 추가해 주세요.")

else:
    # 점수가 높은 순서로 정렬
    # 동점이면 먼저 등록한 업무가 먼저 나옵니다.
    정렬목록 = sorted(
        st.session_state["업무목록"],
        key=lambda 업무: (-업무["점수"], 업무["번호"])
    )

    st.write(f"총 {len(정렬목록)}건의 업무")
    st.dataframe(
        정렬목록,
        hide_index=True,
        use_container_width=True
    )

    # 7. 선택한 업무 삭제
    st.subheader("업무 삭제")

    # 업무 번호를 사용하므로 같은 업무명도 구별할 수 있습니다.
    선택번호 = st.selectbox(
        "삭제할 업무 선택",
        options=[업무["번호"] for 업무 in 정렬목록],
        format_func=lambda 번호: next(
            f"#{업무['번호']} | {업무['업무명']} ({업무['점수']}점)"
            for 업무 in 정렬목록
            if 업무["번호"] == 번호
        )
    )

    if st.button("선택 업무 삭제"):
        st.session_state["업무목록"] = [
            업무 for 업무 in st.session_state["업무목록"]
            if 업무["번호"] != 선택번호
        ]

        # 삭제 후 화면을 다시 그립니다.
        st.rerun()
