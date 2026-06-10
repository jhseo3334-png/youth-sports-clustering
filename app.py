# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import koreanize_matplotlib

# 페이지 기본 설정
st.set_page_config(
    page_title="청소년 스포츠 참여 유형 분석",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (발표용으로 깔끔하고 전문적인 테마 적용)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1e3a8a; text-align: center; padding-bottom: 20px; font-weight: 800; }
    h2 { color: #2563eb; border-bottom: 2px solid #bfdbfe; padding-bottom: 10px; margin-top: 30px; }
    h3 { color: #334155; margin-top: 20px; }
    .cluster-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid; margin-bottom: 20px; }
    .highlight { background-color: #dbeafe; padding: 5px 10px; border-radius: 5px; font-weight: bold; color: #1e40af; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏃 청소년 스포츠 참여 유형 분석 및 활성화 방안")

# 발표 흐름을 위한 탭 구성
tab1, tab2, tab3 = st.tabs(["📌 연구 개요 및 데이터", "📊 군집분석 결과", "💡 정책 제언"])

# ==================== TAB 1: 연구 개요 및 데이터 ====================
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🎯 연구 목적")
        st.markdown("""
        * **청소년의 스포츠 참여 특성 파악**
        * 학교스포츠클럽 및 지역사회 스포츠 참여 형태 분석
        * **K-Means 군집분석**을 활용한 참여 유형 분류
        * 유형별 맞춤형 **정책적 시사점 도출**
        """)
        
    with col2:
        st.header("📂 분석 데이터")
        st.markdown("""
        * **데이터 출처**: 「2021년 지역사회 청소년 스포츠활동 활성화 방안」 조사 데이터
        * **핵심 변수**: 
            * `Q15_1` (월 스포츠 참여 빈도)
            * `Q15_2_M2` (운동시간)
            * `Q19` (학교스포츠클럽 참여)
            * `Q26` (지역사회 스포츠 참여)
            * `Q33` (향후 참여 의향)
        """)
        
    st.divider()
    
    st.header("🛠️ 데이터 전처리 및 군집화 과정")
    step1, step2, step3 = st.columns(3)
    
    with step1:
        st.info("**1단계: 결측치 정제**\n\n원본 2,238명 중 결측치를 제거하여 **최종 1,503명**의 유효 데이터를 확보했습니다.")
    with step2:
        st.info("**2단계: 변수 표준화**\n\n운동시간(최대 420분)과 참여여부(0/1) 등 단위 차이 극복을 위해 **StandardScaler**를 적용했습니다.")
    with step3:
        st.info("**3단계: 최적 군집 탐색**\n\nElbow Method 적용 결과, K=4 지점에서 그래프가 꺾이는 것을 확인하여 **최종 4개 군집**을 선정했습니다.")

# ==================== TAB 2: 군집분석 결과 ====================
with tab2:
    st.header("📈 군집별 인원 분포")
    
    # PDF에 기재된 하드코딩 데이터
    clusters = ['소극적 참여형', '학교 중심 참여형', '적극 참여형', '집중 운동형']
    counts = [467, 438, 490, 108]
    colors = ['#94a3b8', '#3b82f6', '#10b981', '#f59e0b']
    
    col_chart, col_stat = st.columns([2, 1])
    
    with col_chart:
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(clusters, counts, color=colors, width=0.6)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{height}명', ha='center', va='bottom', fontweight='bold')
            
        ax.set_ylabel("인원수 (명)", fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        
    with col_stat:
        st.markdown("<br>", unsafe_allow_html=True)
        for i in range(4):
            st.markdown(f"**{clusters[i]}**: {counts[i]}명 ({(counts[i]/1503)*100:.1f}%)")

    st.divider()
    st.header("🔍 4대 참여 유형별 세부 특성")
    
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class="cluster-card" style="border-color: #94a3b8;">
            <h3 style="margin-top: 0;">🚫 Cluster 0: 소극적 참여형 (467명)</h3>
            <ul>
                <li>학교스포츠클럽 <b>미참여</b></li>
                <li>지역사회 활동 거의 없음</li>
                <li>향후 참여 의향 매우 낮음</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="cluster-card" style="border-color: #3b82f6;">
            <h3 style="margin-top: 0;">🏫 Cluster 1: 학교 중심 참여형 (438명)</h3>
            <ul>
                <li><b>학교스포츠클럽 적극 참여</b></li>
                <li>전반적인 스포츠 활동 빈도 높음</li>
                <li>상대적으로 지역사회 활동은 적음</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="cluster-card" style="border-color: #10b981;">
            <h3 style="margin-top: 0;">🌟 Cluster 2: 적극 참여형 (490명)</h3>
            <ul>
                <li><b>지역사회 스포츠 적극 참여</b></li>
                <li>스포츠 활동 빈도 전체 1위</li>
                <li>향후 참여 의향 가장 높음</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="cluster-card" style="border-color: #f59e0b;">
            <h3 style="margin-top: 0;">🔥 Cluster 3: 집중 운동형 (108명)</h3>
            <ul>
                <li><b>1회 운동시간이 매우 긴 특징</b></li>
                <li>특정 종목에 장시간 집중하여 수행</li>
                <li>소수 정예 그룹 성격</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3: 정책 제언 ====================
with tab3:
    st.header("📝 핵심 요약")
    st.success("""
    "2021년 청소년 스포츠활동 조사자료를 기준으로 K-Means 군집분석을 실시한 결과, 
    청소년은 **소극적 참여형, 학교 중심 참여형, 적극 참여형, 집중 운동형**의 4개 유형으로 명확히 구분되었습니다."
    """)
    
    st.divider()
    
    st.header("💡 유형별 맞춤형 정책 제언")
    
    st.markdown("""
    청소년 스포츠 정책은 단일화된 접근이 아닌, **각 군집의 특성을 반영한 다각적 지원**이 필요합니다.
    """)
    
    policy1, policy2 = st.columns(2)
    
    with policy1:
        st.markdown("#### 1. 소극적 참여형 (467명)")
        st.error("▶ **참여 동기 강화 프로그램 도입**\n\n흥미 위주의 뉴스포츠 보급 및 진입 장벽이 낮은 기초 체력 증진 프로그램 우선 제공")
        
        st.markdown("#### 2. 학교 중심 참여형 (438명)")
        st.info("▶ **지역사회 스포츠 연계 확대**\n\n방과 후 또는 주말에 학교 밖 지역사회 체육 시설을 활용할 수 있는 바우처 및 연계 프로그램 개발")

    with policy2:
        st.markdown("#### 3. 적극 참여형 (490명)")
        st.success("▶ **지속적이고 다양한 프로그램 제공**\n\n현재의 높은 참여율을 유지할 수 있도록 심화반 운영 및 아마추어 리그전 개최 지원")
        
        st.markdown("#### 4. 집중 운동형 (108명)")
        st.warning("▶ **전문 스포츠 프로그램 지원**\n\n단일 종목 심화 훈련 지원, 안전사고 예방 교육, 체육 진로/진학 컨설팅 연계")
