import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="청소년 스포츠 참여 유형 분석",
    layout="wide"
)

# 제목
st.title("🏃 청소년 스포츠 참여 유형 분석")

st.markdown("""
### 연구 목적

- 청소년 스포츠 참여 특성 파악
- K-Means 군집분석 수행
- 스포츠 참여 유형 분류
- 유형별 정책적 시사점 도출
""")

# 데이터 불러오기
df = pd.read_csv("sports_cluster_result.csv")

st.divider()

st.header("1. 분석 데이터")

col1, col2 = st.columns(2)

with col1:
    st.metric("전체 응답자 수", len(df))

with col2:
    st.metric("변수 수", len(df.columns))

st.dataframe(df.head())

st.divider()

st.header("2. 군집 분포")

cluster_count = df["cluster"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(8,4))
cluster_count.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Cluster")
ax.set_ylabel("인원수")
ax.set_title("군집별 인원수")

st.pyplot(fig)

st.divider()

st.header("3. 군집 특성")

cluster_profile = df.groupby("cluster")[
    [
        "Q15_1",
        "Q15_2_M2",
        "Q19",
        "Q26",
        "Q33"
    ]
].mean()

st.dataframe(cluster_profile.round(2))

st.divider()

st.header("4. 군집 해석")

st.markdown("""
### Cluster 0
- 학교스포츠클럽 비참여 중심
- 지역사회 활동 참여 거의 없음
- 참여 의향 낮음

### Cluster 1
- 학교스포츠클럽 참여 집단
- 스포츠 활동 빈도 높음
- 참여 의향 높음

### Cluster 2
- 지역사회 스포츠 적극 참여
- 스포츠 활동 빈도 가장 높음
- 미래 참여 의향 가장 높음

### Cluster 3
- 장시간 운동형 집단
- 1회 운동 시간이 매우 김
- 특정 종목 집중형 가능성
""")

st.divider()

st.header("5. 결론")

st.success("""
청소년 스포츠 참여는 단일 집단이 아니라
4개의 유형으로 구분되었다.

따라서 유형별 맞춤형 스포츠 정책과
프로그램 제공이 필요하다.
""")
