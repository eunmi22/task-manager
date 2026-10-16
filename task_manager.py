import streamlit as st

st.set_page_config(
    page_title="업무 우선순위 관리",
    page_icon="📋"
)


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


# 2. 세부 평가 점수 자동 계산 함수 (추가 기능)
def 자동점수_계산(점수목록):
    # 3개 지표의 평균을 구합니다.
    평균 = sum(점수목록) / len(점수목록)

    # 평균을 반올림하여 1~5점 정수로 만듭니다.
    return int(평균 + 0.5)


# 3. 화면 제목
st.title("📋 업무 우선순위 관리")
st.write("6가지 세부 지표를 평가하여 업무 우선순위를 자동 계산합니다.")


# 4. session_state로 업무 목록 유지
if "업무목록" not in st.session_state:
    st.session_state["업무목록"] = []

if "다음번호" not in st.session_state:
    st.session_state["다음번호"] = 1


# 5. 업무 입력 화면
with st.form("업무입력", clear_on_submit=True):

    업무명 = st.text_input(
        "업무명",
        placeholder="예: 주간 보고서 작성"
    )

    # 중요도 세부 평가 지표 3개
    st.subheader("① 중요도 평가")

    st.caption("각 항목을 1점(낮음)부터 5점(높음)까지 평가하세요.")

    업무영향력 = st.selectbox(
        "업무 영향력",
        [1, 2, 3, 4, 5],
        index=2,
        help="개인 업무에 미치는 영향부터 조직 전체에 미치는 영향까지 평가"
    )

    성과기여도 = st.selectbox(
        "성과 기여도",
        [1, 2, 3, 4, 5],
        index=2,
        help="업무가 조직의 목표와 성과에 기여하는 정도"
    )

    미수행손실 = st.selectbox(
        "미수행 시 손실",
        [1, 2, 3, 4, 5],
        index=2,
        help="업무를 수행하지 않았을 때 발생하는 손실 정도"
    )

    # 긴급도 세부 평가 지표 3개
    st.subheader("② 긴급도 평가")

    마감시급성 = st.selectbox(
        "마감 시급성",
        [1, 2, 3, 4, 5],
        index=2,
        help="1점: 7일 초과 / 5점: 오늘 마감"
    )

    지연피해 = st.selectbox(
        "지연 시 피해",
        [1, 2, 3, 4, 5],
        index=2,
        help="업무가 지연되었을 때 발생하는 피해 정도"
    )

    즉시대응 = st.selectbox(
        "즉시 대응 필요성",
        [1, 2, 3, 4, 5],
        index=2,
        help="업무를 즉시 처리해야 하는 정도"
    )

    # 6. 중요도와 긴급도 자동 계산
    중요도 = 자동점수_계산([
        업무영향력,
        성과기여도,
        미수행손실
    ])

    긴급도 = 자동점수_계산([
        마감시급성,
        지연피해,
        즉시대응
    ])

    # 최종 우선순위 계산
    점수, 등급 = 우선순위_계산(중요도, 긴급도)

    # 계산 결과 안내
    st.info(
        f"중요도 {중요도}점 × 긴급도 {긴급도}점 "
        f"= {점수}점 ({등급})"
    )

    등록 = st.form_submit_button("업무 추가")


# 7. 업무 추가 버튼 처리
if 등록:

    이름 = 업무명.strip()

    # 빈 업무명 또는 공백만 입력한 경우
    if not 이름:
        st.error("업무명을 입력해 주세요.")

    else:
        새업무 = {
            "번호": st.session_state["다음번호"],
            "업무명": 이름,
            "중요도": 중요도,
            "긴급도": 긴급도,
            "점수": 점수,
            "우선순위": 등급
        }

        # 업무 목록에 추가
        st.session_state["업무목록"].append(새업무)

        # 다음 업무 번호 증가
        st.session_state["다음번호"] += 1

        st.success(f"'{이름}' 업무를 등록했습니다.")


# 8. 등록된 업무 목록 표시
st.subheader("③ 등록된 업무 목록")

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

    # 9. 선택한 업무 삭제
    st.subheader("④ 업무 삭제")

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


# 10. 안내 문구
st.caption(
    "업무 목록은 현재 브라우저 세션 동안 유지됩니다."
)
