# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
# 유니코드 마이너스 기호 설정
plt.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정 시도 (다양한 경로에서 찾기)
font_paths = [
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',  # Linux
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # Linux
    'C:/Windows/Fonts/malgun.ttf',  # Windows
    '/Library/Fonts/NanumGothic.ttf',  # Mac
]

for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            fm.fontManager.addfont(font_path)
            if 'Noto' in font_path or 'NanumGothic' in font_path or 'malgun' in font_path:
                plt.rcParams['font.family'] = 'DejaVu Sans'
                break
        except:
            continue

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

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 분석 결과", "📋 프로젝트 정보", "📖 README"])

# 변수명 매핑 (설문 번호 -> 설문 내용)
variable_mapping = {
    "Q15_1": "학교스포츠클럽 참여 여부",
    "Q15_2_M2": "지역사회 스포츠 활동 참여",
    "Q19": "정기적 운동 빈도",
    "Q26": "1회 운동 시간",
    "Q33": "향후 스포츠 참여 의향"
}

# 군집명 매핑
cluster_name_mapping = {
    0: "비참여\n중심 집단",
    1: "학교 중심\n참여 집단",
    2: "적극\n참여 집단",
    3: "장시간\n운동형 집단"
}

cluster_name_full = {
    0: "비참여 중심 집단",
    1: "학교 중심 참여 집단",
    2: "적극 참여 집단",
    3: "장시간 운동형 집단"
}

# ==================== TAB 1: 분석 결과 ====================
with tab1:
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
            fig, ax = plt.subplots(figsize=(12, 6))
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            
            # x축 위치 설정
            x_pos = np.arange(len(cluster_count))
            bars = ax.bar(x_pos, cluster_count.values, color=colors, edgecolor='black', linewidth=1.5, width=0.6)
            
            # 막대 위에 값 표시
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontweight='bold', fontsize=12)
            
            # x축 레이블을 군집 이름으로 설정
            ax.set_xticks(x_pos)
            ax.set_xticklabels([cluster_name_mapping[i] for i in cluster_count.index], 
                             fontsize=11, fontweight='bold')
            ax.set_ylabel("인원수 (명)", fontsize=12, fontweight='bold')
            ax.set_title("군집별 인원수 분포", fontsize=14, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_ylim(0, max(cluster_count.values) * 1.1)
            
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            st.subheader("군집 통계")
            stats_data = {
                '군집': [cluster_name_full[i] for i in cluster_count.index],
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
        
        # 인덱스를 한글 이름으로 변경
        cluster_profile.index = [cluster_name_full[i] for i in cluster_profile.index]
        
        # 컬럼명을 설문 내용으로 변경
        cluster_profile_renamed = cluster_profile.copy()
        cluster_profile_renamed.columns = [variable_mapping[col] for col in cluster_profile_renamed.columns]
        
        st.subheader("각 군집의 평균 특성")
        st.dataframe(cluster_profile_renamed.round(2), use_container_width=True)
        
        st.divider()
        
        st.header("4️⃣ 군집 해석")
        
        cluster_info = {
            "비참여 중심 집단": {
                "title": "🚫 비참여 중심 집단",
                "icon": "⚠️",
                "description": [
                    "학교스포츠클럽 비참여 중심",
                    "지역사회 활동 참여 거의 없음",
                    "스포츠 참여 의향 낮음"
                ],
                "color": "#ff6b6b"
            },
            "학교 중심 참여 집단": {
                "title": "🏫 학교 중심 참여 집단",
                "icon": "✅",
                "description": [
                    "학교스포츠클럽 참여 집단",
                    "정기적 스포츠 활동",
                    "참여 의향 높음"
                ],
                "color": "#4ecdc4"
            },
            "적극 참여 집단": {
                "title": "🌟 적극 참여 집단",
                "icon": "⭐",
                "description": [
                    "지역사회 스포츠 적극 참여",
                    "스포츠 활동 빈도 가장 높음",
                    "미래 참여 의향 가장 높음"
                ],
                "color": "#95e1d3"
            },
            "장시간 운동형 집단": {
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
        
        • **비참여 중심 집단**: 스포츠의 접근성과 흥미 유발 프로그램 필요
        
        • **학교 중심 참여 집단**: 학교 스포츠클럽 지원 강화 및 확대
        
        • **적극 참여 집단**: 고급 프로그램 및 경쟁 기회 제공
        
        • **장시간 운동형 집단**: 전문 지도 및 부상 예방 교육 강화
        """)
        
        st.info("""
        📌 **이 분석의 의미**
        
        청소년층의 다양한 스포츠 참여 패턴을 이해함으로써 
        효과적이고 포용적인 체육 정책을 수립할 수 있습니다.
        """)
        
    except FileNotFoundError:
        st.error("❌ 데이터 파일을 찾을 수 없습니다: 'sports_cluster_result.csv'")
        st.info("📝 sports_cluster_result.csv 파일을 같은 디렉토리에 저장해주세요.")

# ==================== TAB 2: 프로젝트 정보 ====================
with tab2:
    st.header("📋 프로젝트 개요")
    st.markdown("""
    청소년들의 스포츠 참여 패턴을 분석하고 K-Means 군집분석을 통해 
    서로 다른 참여 유형을 분류하는 프로젝트입니다.
    """)
    
    st.divider()
    
    st.header("📊 데이터 수집")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 데이터 출처")
        st.markdown("""
        - **출처**: 한국청소년정책연구원 / 공공데이터포털
        - **조사명**: 청소년 스포츠 참여 실태 조사
        - **조사 기간**: 2023년
        - **조사 대상**: 전국 초·중·고등학교 재학 청소년
        """)
    
    with col2:
        st.subheader("📁 데이터 형식")
        st.markdown("""
        - **파일명**: `sports_cluster_result.csv`
        - **형식**: CSV (Comma Separated Values)
        - **인코딩**: UTF-8
        """)
    
    st.divider()
    
    st.subheader("📈 데이터 규모")
    data_info = {
        "항목": ["표본수", "변수수", "결측치 처리"],
        "수치": ["2,500명", "33개", "결측값 제거 후 분석"]
    }
    st.dataframe(pd.DataFrame(data_info), use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("🔍 주요 변수")
    variables = {
        "변수명": ["Q15_1", "Q15_2_M2", "Q19", "Q26", "Q33"],
        "설명": [
            "학교스포츠클럽 참여 여부",
            "지역사회 스포츠 활동 참여",
            "정기적 운동 빈도",
            "1회 운동 시간",
            "향후 스포츠 참여 의향"
        ]
    }
    st.dataframe(pd.DataFrame(variables), use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("🛠️ 필수 라이브러리")
    st.code("""
streamlit
pandas
numpy
matplotlib
scikit-learn
matplotlib-font-manager
    """)

# ==================== TAB 3: README ====================
with tab3:
    st.header("📖 프로젝트 README")
    st.markdown("""
# 청소년 스포츠 참여 유형 분석 (Youth Sports Clustering)

## 📋 프로젝트 개요
청소년들의 스포츠 참여 패턴을 분석하고 K-Means 군집분석을 통해 서로 다른 참여 유형을 분류하는 프로젝트입니다.

---

## 📊 데이터 수집

### 📌 데이터 출처
- **출처**: 한국청소년정책연구원 / 공공데이터포털
- **조사명**: 청소년 스포츠 참여 실태 조사
- **조사 기간**: 2023년 (조사 연도)
- **조사 대상**: 전국 초·중·고등학교 재학 청소년

### 📁 데이터 형식
- **파일명**: `sports_cluster_result.csv`
- **형식**: CSV (Comma Separated Values)
- **인코딩**: UTF-8

### 📈 데이터 규모
| 항목 | 수치 |
|------|------|
| **표본수** | 2,500명 |
| **변수수** | 33개 |
| **결측치 처리** | 결측값 제거 후 분석 |

### 🔍 주요 변수
- **Q15_1**: 학교스포츠클럽 참여 여부
- **Q15_2_M2**: 지역사회 스포츠 활동 참여
- **Q19**: 정기적 운동 빈도
- **Q26**: 1회 운동 시간
- **Q33**: 향후 스포츠 참여 의향

---

## 📁 프로젝트 구조

```
youth-sports-clustering/
├── README.md                      # 프로젝트 설명 문서
├── app.py                         # Streamlit 분석 대시보드
├── sports_cluster_result.csv      # 분석 데이터
└── requirements.txt               # 필요 라이브러리
```

---

## 🛠️ 필수 라이브러리

```
streamlit
pandas
numpy
matplotlib
scikit-learn
matplotlib-font-manager
```

### 설치 방법
```bash
pip install -r requirements.txt
```

---

## 🚀 실행 방법

```bash
streamlit run app.py
```

---

## 📊 분석 결과

### 4개 군집 분류
1. **비참여 중심 집단**: 🚫 학교스포츠클럽 비참여 중심
2. **학교 중심 참여 집단**: 🏫 학교스포츠클럽 참여 집단
3. **적극 참여 집단**: 🌟 지역사회 스포츠 적극 참여
4. **장시간 운동형 집단**: 💪 1회 운동 시간이 매우 긴 집단

---

## 💡 주요 시사점

청소년 스포츠 참여는 단순한 참여/비참여가 아니라 **다양한 패턴**을 보이며, 각 집단의 특성에 맞는 **맞춤형 정책**이 필요합니다.

---
    """)
pip install koreanize-matplotlib
