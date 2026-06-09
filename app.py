# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# 한글 폰트 설정
rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="청소년 스포츠 참여 유형 분석",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
    <style>
    /* 전체 배경 */
    .main {
        background-color: #f5f7fa;
    }
    
    /* 제목 스타일 */
    h1 {
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
        font-size: 2.5em;
        font-weight: bold;
    }
    
    h2 {
        color: #2c3e50;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    /* 메트릭 박스 */
    [data-testid="metric-container"] {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    
    /* 데이터프레임 */
    [data-testid="dataframe"] {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목
st.title("🏃 청소년 스포츠 참여 유형 분석")

# 연구 목적
st.markdown("""
#### 📋 연구 목적
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("🔍 청소년 스포츠\n참여 특성 파악")
with col2:
    st.info("📊 K-Means\n군집분석 수행")
with col3:
    st.info("🎯 스포츠 참여\n유형 분류")
with col4:
    st.info("💡 유형별 정책적\n시사점 도출")

st.divider()

# 데이터 불러오기
try:
    df = pd.read_csv("sports_cluster_result.csv")
    
    st.header("1️⃣ 분석 데이터")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📌 전체 응답자 수", f"{len(df):,}명")
    
    with col2:
        st.metric("📊 변수 수", f"{len(df.columns)}개")
    
    with col3:
        st.metric("🔢 군집 수", f"{df['cluster'].nunique()}개")
    
    st.subheader("데이터 미리보기")
    st.dataframe(df.head(10), use_container_width=True)
    
    st.divider()
    
    st.header("2️⃣ 군집 분포")
    
    cluster_count = df["cluster"].value_counts().sort_index()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        bars = ax.bar(cluster_count.index, cluster_count.values, color=colors, edgecolor='black', linewidth=1.5)
        
        # 막대 위에 값 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax.set_xlabel("군집", fontsize=12, fontweight='bold')
        ax.set_ylabel("인원수", fontsize=12, fontweight='bold')
        ax.set_title("군집별 인원수 분포", fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("군집 통계")
        stats_data = {
            '군집': list(cluster_count.index),
            '인원수': list(cluster_count.values),
            '비율(%)': [f"{(v/len(df)*100):.1f}%" for v in cluster_count.values]
        }
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.header("3️⃣ 군집 특성")
    
    cluster_profile = df.groupby("cluster")[
        [
            "Q15_1",
            "Q15_2_M2",
            "Q19",
            "Q26",
            "Q33"
        ]
    ].mean()
    
    st.subheader("각 군집의 평균 특성")
    st.dataframe(cluster_profile.round(2), use_container_width=True)
    
    st.divider()
    
    st.header("4️⃣ 군집 해석")
    
    cluster_info = {
        "Cluster 0": {
            "title": "🚫 비참여 중심 집단",
            "icon": "⚠️",
            "description": [
                "학교스포츠클럽 비참여 중심",
                "지역사회 활동 참여 거의 없음",
                "스포츠 참여 의향 낮음"
            ],
            "color": "#ff6b6b"
        },
        "Cluster 1": {
            "title": "🏫 학교 중심 참여 집단",
            "icon": "✅",
            "description": [
                "학교스포츠클럽 참여 집단",
                "정기적 스포츠 활동",
                "참여 의향 높음"
            ],
            "color": "#4ecdc4"
        },
        "Cluster 2": {
            "title": "🌟 적극 참여 집단",
            "icon": "⭐",
            "description": [
                "지역사회 스포츠 적극 참여",
                "스포츠 활동 빈도 가장 높음",
                "미래 참여 의향 가장 높음"
            ],
            "color": "#95e1d3"
        },
        "Cluster 3": {
            "title": "💪 장시간 운동형 집단",
            "icon": "🏋️",
            "description": [
                "1회 운동 시간이 매우 김",
                "특정 종목 집중형 가능성",
                "고강도 운동 선호"
            ],
            "color": "#f9ca24"
        }
    }
    
    for cluster_key, info in cluster_info.items():
        with st.container():
            st.markdown(f"""
            <div style="background-color: {info['color']}; padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h4 style="color: white; margin: 0;">{info['icon']} {info['title']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for desc in info['description']:
                st.markdown(f"• {desc}")
            st.markdown("")
    
    st.divider()
    
    st.header("5️⃣ 결론 및 정책 제언")
    
    st.success("""
    🎯 **주요 발견사항**
    
    청소년 스포츠 참여는 단일 집단이 아니라 **4개의 서로 다른 유형**으로 구분됩니다.
    
    각 집단의 특성과 필요에 맞는 맞춤형 정책이 필요합니다.
    """)
    
    st.warning("""
    💡 **정책 제언**
    
    • **Cluster 0 (비참여 집단)**: 스포츠의 접근성과 흥미 유발 프로그램 필요
    
    • **Cluster 1 (학교 중심)**: 학교 스포츠클럽 지원 강화 및 확대
    
    • **Cluster 2 (적극 참여)**: 고급 프로그램 및 경쟁 기회 제공
    
    • **Cluster 3 (장시간 운동)**: 전문 지도 및 부상 예방 교육 강화
    """)
    
    st.info("""
    📌 **이 분석의 의미**
    
    청소년층의 다양한 스포츠 참여 패턴을 이해함으로써 
    효과적이고 포용적인 체육 정책을 수립할 수 있습니다.
    """)
    
except FileNotFoundError:
    st.error("❌ 데이터 파일을 찾을 수 없습니다: 'sports_cluster_result.csv'")
    st.info("📝 sports_cluster_result.csv 파일을 같은 디렉토리에 저장해주세요.")
