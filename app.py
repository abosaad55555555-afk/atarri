import re
import unicodedata
from urllib.parse import quote_plus

import streamlit as st


# إعداد الصفحة
st.set_page_config(
    page_title="دليل الخرج الشامل",
    page_icon="🌟",
    layout="centered",
)

# دعم اتجاه الكتابة من اليمين إلى اليسار
st.markdown(
    """
    <style>
        .stApp {
            direction: rtl;
            text-align: right;
        }

        section[data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;
        }

        div[data-testid="stTextInput"] input {
            direction: rtl;
            text-align: right;
        }

        div[data-testid="stSelectbox"] {
            direction: rtl;
            text-align: right;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌟 دليل الخرج الشامل للتصنيفات والمعالم")
st.markdown(
    """
    استكشف الأماكن والمقاهي والمعالم في الخرج، مع إمكانية التصفية حسب
    التصنيف، والترتيب حسب التقييم أو الأبجدية، والبحث المباشر، وفتح
    المواقع على خرائط Google.
    """
)


# قاعدة البيانات
attractions = [
    {
        "name": "أبارت كافيه (Apart Cafe)",
        "category": "مقاهي ومطاعم",
        "rating": 4.9,
        "location": "الخرج",
        "desc": (
            "مقهى متخصص عصري يتميز بديكورات راقية وجلسات هادئة، "
            "ويقدم تشكيلة مميزة من القهوة المختصة والمخبوزات الطازجة."
        ),
    },
    {
        "name": "قصر الملك عبد العزيز التاريخي",
        "category": "معالم تاريخية",
        "rating": 4.8,
        "location": "وسط الخرج",
        "desc": (
            "من أهم المعالم التاريخية، بني في عام 1359 هـ "
            "بتصميم معماري نجدي فريد من الطين."
        ),
    },
    {
        "name": "مزارع الخرج الزراعية",
        "category": "سياحة بيئية",
        "rating": 4.7,
        "location": "الخرج",
        "desc": (
            "تشتهر بمزارع النخيل الشاسعة وتوفر تجارب سياحة ريفية فريدة."
        ),
    },
    {
        "name": "عيون الخرج (عين الضلع)",
        "category": "طبيعة",
        "rating": 4.5,
        "location": "أطراف الخرج",
        "desc": (
            "عيون ارتوازية طبيعية تاريخية كانت شريان الحياة الزراعي قديما."
        ),
    },
    {
        "name": "منتزه البرج",
        "category": "منتزهات وترفيه",
        "rating": 4.2,
        "location": "الخرج",
        "desc": (
            "وجهة عائلية ممتازة تضم مساحات خضراء ومناطق ألعاب أطفال."
        ),
    },
]


def normalize_arabic(text: str) -> str:
    """توحيد النص العربي لتحسين البحث والترتيب."""
    text = unicodedata.normalize("NFKD", text.strip().lower())

    # حذف التشكيل والتطويل
    text = re.sub(r"[\u064B-\u065F\u0670\u0640]", "", text)

    # توحيد أكثر أشكال الحروف اختلافا في الكتابة
    replacements = str.maketrans(
        {
            "أ": "ا",
            "إ": "ا",
            "آ": "ا",
            "ٱ": "ا",
            "ى": "ي",
            "ؤ": "و",
            "ئ": "ي",
            "ة": "ه",
        }
    )
    text = text.translate(replacements)

    # حذف المسافات المتكررة
    return " ".join(text.split())


def matches_search(place: dict, query: str) -> bool:
    """التحقق من وجود عبارة البحث في بيانات المكان."""
    normalized_query = normalize_arabic(query)

    searchable_fields = [
        place["name"],
        place["category"],
        place["location"],
        place["desc"],
    ]

    return any(
        normalized_query in normalize_arabic(field)
        for field in searchable_fields
    )


# أدوات التصفية
st.sidebar.header("⚙️ أدوات التصفية والبحث")

all_categories = ["الكل"] + sorted(
    {item["category"] for item in attractions},
    key=normalize_arabic,
)

selected_category = st.sidebar.selectbox(
    "اختر التصنيف:",
    all_categories,
)

sort_option = st.sidebar.selectbox(
    "ترتيب النتائج حسب:",
    [
        "التقييم (الأعلى أولا)",
        "الترتيب الأبجدي (أ - ي)",
    ],
)

minimum_rating = st.sidebar.slider(
    "الحد الأدنى للتقييم:",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
)


# البحث
search_query = st.text_input(
    "🔍 ابحث باسم المكان أو الوصف أو التصنيف أو الموقع:",
    placeholder="مثال: أبارت، قصر، عيون",
)


# تطبيق التصفية
filtered_data = [
    place
    for place in attractions
    if (
        selected_category == "الكل"
        or place["category"] == selected_category
    )
    and place["rating"] >= minimum_rating
    and (
        not search_query.strip()
        or matches_search(place, search_query)
    )
]


# تطبيق الترتيب
if sort_option == "التقييم (الأعلى أولا)":
    filtered_data.sort(
        key=lambda place: place["rating"],
        reverse=True,
    )
else:
    filtered_data.sort(
        key=lambda place: normalize_arabic(place["name"]),
    )


# عرض النتائج
st.divider()
st.subheader(f"📋 النتائج المعروضة: {len(filtered_data)} مكان")

if not filtered_data:
    st.warning(
        "عذرا، لم نجد نتائج مطابقة للبحث أو خيارات التصفية المحددة."
    )
else:
    for place in filtered_data:
        with st.container(border=True):
            details_column, map_column = st.columns([3, 1])

            with details_column:
                st.subheader(place["name"])
                st.markdown(
                    f"**التصنيف:** {place['category']}  \n"
                    f"**الموقع:** {place['location']}  \n"
                    f"**التقييم:** {place['rating']:.1f} من 5 ⭐"
                )
                st.progress(place["rating"] / 5)
                st.write(place["desc"])

            with map_column:
                map_query = quote_plus(
                    f"{place['name']}، {place['location']}، السعودية"
                )
                maps_url = (
                    "[google.com](https://www.google.com/maps/search/)"
                    f"?api=1&query={map_query}"
                )

                st.link_button(
                    "🗺️ خرائط Google",
                    maps_url,
                    use_container_width=True,
                )
