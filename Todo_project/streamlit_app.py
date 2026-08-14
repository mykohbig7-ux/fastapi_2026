'''
=========================================================================
streamlit_app.py

FastAPI Todo API를 호출해서 화면으로 보여주는 프론트엔드
FastAPI는 계속 uvicorn으로 실행 중
Streamlit도 따로 streamlit run으로 실행을 해야 한다.
=========================================================================
'''
import streamlit as st
import requests

# -----------------------------------------------------------------------------------------
# 기본 설정
# -----------------------------------------------------------------------------------------
API_BASE = 'http://127.0.0.1:8000' # uvicorn으로 띄우는 FastAPI 주소

st.set_page_config(
    page_title='나의 할 일 관리',
    page_icon='⏳',
    layout='centered',
)

st.markdown('''
<style>
.todo-card {
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #e6e6e6;
}
.todo-done {
    background-color: #f0f7f0;
    text-decoration: line-through;
    color: #888;
}
.todo-pending {
    background-color: #fff;
}
</style>
''', unsafe_allow_html=True) # unsafe_allow_html=True --> html/css가 먼저 적용이 되도록 

# -----------------------------------------------------------------------------------------
# 세션 상태(session_state) 초기화
#
#   스트림릿은 버튼을 누를 때 마다 전체 스크립트가 위에서 아래로 다시 실행된다.
#   로그인을 했다라는 사실을 변수에 담아둔다.
#   st.session_state는 재실행되어도 값이 유지되는 유일한 저장공간이다.
#   여기에 토큰/로그인 여부를 저장한다.
# -----------------------------------------------------------------------------------------
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

def get_headers() -> dict:
    """로그인 후 API요청에 매번 붙여야 하는 인증 헤더를 만들어 반환"""
    return {'Authorization': f'Bearer {st.session_state.access_token}'}

def logout():
    """세션 상태를 비워서 로그아웃 처리(서버에 요청 보낼 필요 없다 -> JWT는 Stateless방식)"""
    st.session_state.access_token = None
    st.session_state.user_email = None

def extract_error_message(res: requests.Response, fallback: str) -> str:
    """
    FastAPI 에러 응답에서 사람이 읽을 수 있는 메세지만 뽑아 낸다.

    - 일반적인 HTTPException: {"detail": [{"type": ..., "msg": "Value error, ..."}]} 형태(그대로 사용)
    - 깔끔하게 출력하기 위해서 리스트를 순회하며 msg만 뽑고, "Value error, " 접두어는 잘라낸다.
    - 응답이 JSON이 아니거나 (500 에러 페이지 등) 파싱 자체가 실패하는 경우도 대비
    """
    try:
        detail = res.json().get('detail', fallback)
    except requests.exceptions.JSONDecodeError:
        return f'서버 오류 (status {res.status_code}). uvicorn 터미널을 확인해주세요.'