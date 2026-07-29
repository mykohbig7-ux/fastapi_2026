# ==============================================================================
# ~/bigdata2026/fastapi/Streamlit/08_layout.py
#
#   Streamlit 라이브러리 기초 실습
#
#       - 레이아웃
# ==============================================================================

# 1. 라이브러리 불러오기
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 메인페이지
st.title('This is main page')

# 3. sidebar
with st.sidebar:
    st.title('This is sidebar')
    side_option = st.multiselect(
        label='your selection is',
        options=['Car', 'Airplane', 'Train', 'Ship', 'Bicycle'],
        placeholder='select transportion'
    )

# 4. 이미지 세로 나열
img1 = Image.open('ex2.png')
img2 = Image.open('ex5.png')

st.header('피카츄')
st.image(img1, width=400, caption='귀여운 피카츄')

st.header('포켓몬')
st.image(img2, width=400, caption='메타몽, 피카츄, 꼬부기, 이상해씨, 잠만보')

# 5. 컬럼 레이아웃 (세로 단이 2개)
col1, col2 = st.columns(2) # 똑같은 비율로 나눠진다. 2개
with col1:
    st.header('피카츄')
    st.image(img1, width=300, caption='귀여운 피카츄')

with col2:
    st.header('포켓몬')
    st.image(img2, width=300, caption='메타몽, 피카츄, 꼬부기, 이상해씨, 잠만보')

st.divider()

# 6. 탭 레이아웃
tab1, tab2 = st.tabs(['실습1', '실습2'])

# 판다스로 csv불러와서 데이터프레임 생성
df = pd.read_csv('2026-07-29.csv')

with tab1: # 실습1
    st.table(df.head())

with tab2: # 실습2
    fig, ax = plt.subplot()
    sns.countplot(data=df, ax=ax)
    st.pyplot(fig)