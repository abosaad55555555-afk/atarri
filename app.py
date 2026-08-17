import json
import streamlit as st
from openai import OpenAI

# 1. إعداد واجهة البرنامج وتنسيق الصفحة
st.set_page_config(
    page_title="دليل الخرج السياحي الذكي", page_icon="📍", layout="centered"
)

st.title("📍 مرشد الخرج السياحي الذكي")
st.markdown(
    "أهلاً بك في مدينة الخرج! أنا مساعدك السياحي الرقمي، تفضل واسألني عن"
    " الأماكن التاريخية، المقاهي العصرية، أو المعالم والمنتزهات."
)

# 2. قاعدة بيانات المعالم المتكاملة لمدينة الخرج
db = {
    "alkharj_attractions": [
        {
            "id": 1,
            "name": "قصر الملك عبد العزيز التاريخي",
            "category": "معالم تاريخية",
            "description": (
                "من أهم المعالم التاريخية في الخرج، بُني في عام 1359 هـ، ويتميز"
                " بتصميمه المعماري النجدي الفريد المصنوع من الطين اللبن وأسقف"
                " خشب الأثل."
            ),
            "location": "وسط مدينة الخرج",
            "best_time": "العصر والمساء",
        },
        {
            "id": 2,
            "name": "عيون الخرج (عين الضلع / سمحة)",
            "category": "طبيعة ومعالم تاريخية",
            "description": (
                "تعتبر من العيون الأرتوازية الطبيعية التاريخية التي كانت تمثل"
                " شريان الحياة الزراعي وتغذي مزارع النخيل في المحافظة قديماً."
            ),
            "location": "أطراف مدينة الخرج",
            "best_time": "فصل الشتاء وأوقات الغروب",
        },
        {
            "id": 3,
            "name": "أبارت كافيه (Apart Cafe)",
            "category": "مقاهي ومطاعم",
            "description": (
                "مقهى متخصص عصري في الخرج، يتميز بديكورات راقية وجلسات هادئة،"
                " ويقدم تشكيلة مميزة من القهوة المختصة والمخبوزات الطازجة."
            ),
            "location": "الخرج",
            "best_time": "طوال اليوم (الصباح والمساء)",
        },
        {
            "id": 4,
            "name": "منتزه البرج / برج المياه",
            "category": "متنزهات وترفيه",
            "description": (
                "معلم بارز يحيط به مساحات مسطحة خضراء ومناطق ألعاب أطفال، ويُعد"
                " وجهة عائلية ممتازة للتنزه وقضاء أوقات ممتعة."
            ),
            "location": "الخرج",
            "best_time": "المساء",
        },
        {
            "id": 5,
            "name": "مزارع الخرج الزراعية (سياحة المزارع)",
            "category": "سياحة بيئية",
            "description": (
                "الخرج سلة غذاء كبرى وتشتهر بمزارع النخيل الشاسعة ومنتجات الألبان"
                " والخضروات العضوية، وتتيح تجارب سياحة ريفية فريدة."
            ),
            "location": "مختلف أنحاء المحافظة",
            "best_time": "الصباح الباكر أو الشتاء",
        },
    ]
}

attractions_context = json.dumps(db, ensure_ascii=False)

# 3. إعداد الاتصال بمحرك الذكاء الاصطناعي
# استبدل النص التالي بمفتاح الـ API الخاص بك من OpenAI
client = OpenAI(api_key="ضع_مفتاحك_هنا")

# 4. بناء السياق الموجه للنموذج (System Prompt)
system_prompt = f"""
أنت مرشد سياحي خبير ومحترف بمدينة الخرج في المملكة العربية السعودية.
اعتمد في إجاباتك حصرياً على قاعدة البيانات التالية الخاصة بمعالم الخرج:
{attractions_context}

تعليمات صارمة:
- أجب بأسلوب ودود ومضياف يعكس أصالة وكرم أهل الخرج.
- قدم تفاصيل دقيقة ومباشرة بناءً على قاعدة البيانات (الموقع، وقت الزيارة الأفضل، الوصف).
- إذا سأل المستخدم عن مكان أو خدمة غير موجودة في قاعدة البيانات، اعتذر بلطف شديد ووجهه لأقرب خيار متاح ضمن المعالم المتوفرة.
"""

# 5. إدارة جلسة المحادثة (Chat History)
if "messages" not in st.session_state:
  st.session_state.messages = [{"role": "system", "content": system_prompt}]

# عرض رسائل المحادثة السابقة
for message in st.session_state.messages[1:]:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# 6. استقبال مدخلات المستخدم وعرض الردود
if prompt := st.chat_input("ما الذي تود اكتشافه في الخرج اليوم؟"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("جاري استكشاف الخرج لأجلك..."):
      try:
        response = client.chat.completions.create(
            model="gpt-4o", messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        st.session_state.messages.append(
            {"role": "assistant", "content": msg}
        )
      except Exception as e:
        st.error(
            f"حدث خطأ في الاتصال، تأكد من صحة مفتاح الـ API الخاص بك. التفاصيل:"
            f" {e}"
        )
