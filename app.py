import streamlit as st

# 1. إعداد واجهة البرنامج وتنسيق الصفحة
st.set_page_config(
    page_title="دليل الخرج الشامل", page_icon="🌟", layout="centered"
)

st.title("🌟 دليل الخرج الشامل للتصنيفات والمعالم")
st.markdown(
    "استكشف جميع الأماكن والمقاهي والمعالم في الخرج، مع إمكانية التصفية"
    " حسب أي تصنيف، الترتيب حسب التقييم أو الأبجدية، والبحث المباشر وفتح"
    " المواقع على خرائط جوجل."
)

# 2. قاعدة البيانات الشاملة القابلة للتصنيف
attractions = [
    {
        "name": "أبارت كافيه (Apart Cafe)",
        "category": "مقاهي ومطاعم",
        "rating": 4.9,
        "location": "الخرج",
        "desc": (
            "مقهى متخصص عصري يتميز بديكورات راقية وجلسات هادئة، ويقدم تشكيلة"
            " مميزة من القهوة المختصة والمخبوزات الطازجة."
        ),
    },
    {
        "name": "قصر الملك عبد العزيز التاريخي",
        "category": "معالم تاريخية",
        "rating": 4.8,
        "location": "وسط الخرج",
        "desc": (
            "من أهم المعالم التاريخية، بُني في عام 1359 هـ بتصميم معماري نجدي فريد"
            " من الطين."
        ),
    },
    {
        "name": "مزارع الخرج الزراعية",
        "category": "سياحة بيئية",
        "rating": 4.7,
        "location": "الخرج",
        "desc": "تشتهر بمزارع النخيل الشاسعة وتوفر تجارب سياحة ريفية فريدة.",
    },
    {
        "name": "عيون الخرج (عين الضلع)",
        "category": "طبيعة",
        "rating": 4.5,
        "location": "أطراف الخرج",
        "desc": "عيون أرتوازية طبيعية تاريخية كانت شريان الحياة الزراعي قديماً.",
    },
    {
        "name": "منتزه البرج",
        "category": "منتزهات وترفيه",
        "rating": 4.2,
        "location": "الخرج",
        "desc": "وجهة عائلية ممتازة تضم مساحات خضراء ومناطق ألعاب أطفال.",
    },
]

# 3. الشريط الجانبي: التصفية الديناميكية والترتيب
st.sidebar.header("⚙️ أدوات التصفية والبحث")

# استخراج كل التصنيفات المتاحة ديناميكياً لتصنيف أي شيء
all_categories = ["الكل"] + sorted(
    list(set([item["category"] for item in attractions]))
)
selected_category = st.sidebar.selectbox("اختر التصنيف:", all_categories)

# خيارات الترتيب
sort_option = st.sidebar.selectbox(
    "ترتيب النتائج حسب:",
    ["التقييم (الأعلى أولاً)", "الترتيب الأبجدي (أ - ي)"],
)

# 4. تصفية البيانات بناءً على التصنيف المختار
if selected_category == "الكل":
  filtered_data = attractions.copy()
else:
  filtered_data = [
      item for item in attractions if item["category"] == selected_category
  ]

# 5. تطبيق الترتيب
if sort_option == "التقييم (الأعلى أولاً)":
  filtered_data = sorted(filtered_data, key=lambda x: x["rating"], reverse=True)
elif sort_option == "الترتيب الأبجدي (أ - ي)":
  filtered_data = sorted(filtered_data, key=lambda x: x["name"])

# 6. قسم البحث النصي الحر
search_query = st.text_input(
    "🔍 ابحث عن أي مكان أو مقهى (مثال: أبارت، قصر، عيون):"
)
if search_query:
  filtered_data = [
      item
      for item in filtered_data
      if search_query.lower() in item["name"].lower()
      or search_query.lower() in item["desc"].lower()
      or search_query.lower() in item["category"].lower()
  ]

# 7. عرض النتائج بشكل مرتب ومنظم مع روابط خرائط جوجل
st.markdown("---")
st.subheader(f"📋 النتائج المعروضة ({len(filtered_data)} مكان):")

if not filtered_data:
  st.warning("عذراً، لم نجد نتائج مطابقة لبحثك أو التصنيف المختار.")
else:
  for place in filtered_data:
    with st.container():
      col1, col2 = st.columns([3, 1])
      with col1:
        st.subheader(f"{place['name']} ({place['rating']} ⭐)")
        st.write(
            f"**التصنيف:** {place['category']} | **الموقع:**"
            f" {place['location']}"
        )
        st.write(place["desc"])
      with col2:
        maps_url = (
            f"https://www.google.com/maps/search/?api=1&query={place['name']}"
            " الخرج"
        )
        st.link_button("🗺️ خرائط جوجل", maps_url)
      st.markdown("---")
