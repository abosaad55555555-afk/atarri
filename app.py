import re
import unicodedata
from urllib.parse import quote_plus
import streamlit as st
import pandas as pd

# ==========================================
# 1. إعداد الصفحة والاتجاه (RTL)
# ==========================================
st.set_page_config(
    page_title="دليل الخرج الشامل",
    page_icon="🌟",
    layout="centered",
)

st.markdown(
    """
    <style>
        .stApp {
            direction: rtl;
            text-align: right;
            font-family: 'Tajawal', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        section[data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;
        }
        div[data-testid="stTextInput"] input, 
        div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
            direction: rtl;
            text-align: right;
        }
        .place-card {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            background-color: #fcfcfc;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: 0.3s;
        }
        .place-card:hover {
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        .map-btn {
            text-decoration: none;
            background-color: #3498db;
            color: white !important;
            padding: 8px 16px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 10px;
            font-weight: bold;
            font-size: 14px;
        }
        .map-btn:hover {
            background-color: #2980b9;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. العنوان والوصف
# ==========================================
st.title("🌟 دليل الخرج الشامل للتصنيفات والمعالم")
st.markdown("استكشف الأماكن، المقاهي، والمعالم في الخرج. يمكنك البحث بالكلمات الإنجليزية أو العربية (مثل: cafe, مطعم, السيح).")
st.markdown("---")

# ==========================================
# 3. البيانات التجريبية
# ==========================================
@st.cache_data
def load_data():
    data = [
        {"الاسم": "مقهى البيك", "التصنيف": "مقاهي", "التقييم": 4.5, "المنطقة": "السيح"},
        {"الاسم": "مطعم الشاورجي", "التصنيف": "مطاعم", "التقييم": 4.2, "المنطقة": "السيح"},
        {"الاسم": "حديقة الملك فهد", "التصنيف": "حدائق", "التقييم": 4.7, "المنطقة": "السيح"},
        {"الاسم": "قصر الملك عبدالعزيز التاريخي", "التصنيف": "معالم", "التقييم": 4.9, "المنطقة": "الدلم"},
        {"الاسم": "مقهى سكسبري", "التصنيف": "مقاهي", "التقييم": 4.3, "المنطقة": "الدلم"},
        {"الاسم": "مقهى كافيهات", "التصنيف": "مقاهي", "التقييم": 4.8, "المنطقة": "السيح"},
        {"الاسم": "مطعم كودو", "التصنيف": "مطاعم", "التقييم": 4.0, "المنطقة": "السيح"},
        {"الاسم": "مطعم البيك", "التصنيف": "مطاعم", "التقييم": 4.6, "المنطقة": "الدلم"},
        {"الاسم": "حديقة الصالحية", "التصنيف": "حدائق", "التقييم": 4.4, "المنطقة": "الصالحية"},
        {"الاسم": "سد الملك فهد", "التصنيف": "معالم", "التقييم": 4.6, "المنطقة": "الخرج"},
    ]
    return pd.DataFrame(data)

df = load_data()

# ==========================================
# 4. أدوات التصفية والبحث (Filters)
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    search_query = st.text_input("🔍 البحث الذكي", placeholder="اكتب: cafe, مطعم, السيح...")

with col2:
    categories = ["الكل"] + sorted(df["التصنيف"].unique().tolist())
    selected_category = st.selectbox("📂 التصنيف", categories)

with col3:
    sort_options = ["التقييم (الأعلى أولاً)", "الاسم (أبجدياً)"]
    sort_by = st.selectbox("⬇️ ترتيب حسب", sort_options)

# ==========================================
# 5. منطق البحث الذكي (Smart Search Logic)
# ==========================================
filtered_df = df.copy()

# قاموس لتحويل الكلمات الإنجليزية والشائعة إلى التصنيفات العربية
search_aliases = {
    "cafe": "مقاهي", "cafes": "مقاهي", "coffee": "مقاهي", "مقهى": "مقاهي",
    "restaurant": "مطاعم", "restaurants": "مطاعم", "food": "مطاعم", "مطعم": "مطاعم",
    "park": "حدائق", "parks": "حدائق", "garden": "حدائق", "حديقة": "حدائق",
    "landmark": "معالم", "landmarks": "معالم", "معلم": "معالم", "historical": "معالم"
}

if search_query:
    query_lower = search_query.strip().lower()
    
    # 1. التحقق مما إذا كانت الكلمة المطابقة هي "تصنيف" (مثل كتابة cafe)
    if query_lower in search_aliases:
        target_category = search_aliases[query_lower]
        filtered_df = filtered_df[filtered_df["التصنيف"] == target_category]
    else:
        # 2. إذا لم تكن تصنيفاً، نبحث في (الاسم، التصنيف، المنطقة) معاً
        mask = (
            filtered_df["الاسم"].str.contains(search_query, case=False, na=False) |
            filtered_df["التصنيف"].str.contains(search_query, case=False, na=False) |
            filtered_df["المنطقة"].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

# تطبيق التصفية من القائمة المنسدلة (إذا لم يكن "الكل")
if selected_category != "الكل":
    filtered_df = filtered_df[filtered_df["التصنيف"] == selected_category]

# ==========================================
# 6. الترتيب وعرض النتائج
# ==========================================
if sort_by == "التقييم (الأعلى أولاً)":
    filtered_df = filtered_df.sort_values(by="التقييم", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="الاسم")

# عرض النتائج
if filtered_df.empty:
    st.warning("⚠️ لا توجد نتائج مطابقة لبحثك. حاول تغيير معايير البحث.")
else:
    st.success(f"✅ تم العثور على {len(filtered_df)} نتيجة.")
    
    for index, row in filtered_df.iterrows():
        location_query = quote_plus(f"{row['الاسم']} {row['المنطقة']} الخرج")
        map_url = f"https://www.google.com/maps/search/?api=1&query={location_query}"
        
        icon = "☕" if row["التصنيف"] == "مقاهي" else "🍽️" if row["التصنيف"] == "مطاعم" else "🌳" if row["التصنيف"] == "حدائق" else "🏛️"
        
        st.markdown(
            f"""
            <div class="place-card">
                <h3 style="margin:0 0 10px 0; color:#2c3e50;">{icon} {row['الاسم']}</h3>
                <p style="margin:5px 0; color:#7f8c8d; font-size:15px;">
                    📍 <strong>المنطقة:</strong> {row['المنطقة']} &nbsp; | &nbsp; 
                    ⭐ <strong>التقييم:</strong> {row['التقييم']} &nbsp; | &nbsp; 
                    🏷️ <strong>التصنيف:</strong> {row['التصنيف']}
                </p>
                <a href="{map_url}" target="_blank" class="map-btn">
                    🗺️ فتح في خرائط Google
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )