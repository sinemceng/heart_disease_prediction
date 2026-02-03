import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import time
import io

st.set_page_config(
    page_title="Kalp Riski Analiz Paneli",
    page_icon="❤️",
    layout="wide"
)
def apply_custom_styles():
    st.markdown("""
        <style>
        .stApp { background-color: #F8F4F9; }
        div.stButton > button:first-child {
            color: #ffffff;
            background-color: #C39BD3;
            border-radius: 12px;
            border: none;
            height: 3em;
            width: 100%;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #A569BD;
            border: 1px solid #7D3C98;
        }
        [data-testid="stMetricValue"] { color: #5B2C6F; }
        </style>
        """, unsafe_allow_html=True)

# ---  VERİ VE MODEL YÜKLEME ---
@st.cache_resource
def load_model_assets():
    try:
        model = joblib.load('heart_rf_model.pkl')
        features = joblib.load('features.pkl')
        return model, features
    except FileNotFoundError:
        st.error("Model dosyaları bulunamadı!")
        return None, None


model, features = load_model_assets()

# ---  SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# ---  SIDEBAR ---
with st.sidebar:
    st.title("📊 Model Paneli")
    st.info("Bu sistem, Random Forest algoritması kullanarak %83.70 doğrulukla tahminleme yapar.")

    if len(st.session_state.history) > 0:
        if st.button("🗑️ Geçmişi Temizle"):
            st.session_state.history = []
            st.rerun()

        st.divider()
        st.markdown("### 🕒 Son Analiz Detayları")
        for h in reversed(st.session_state.history[-5:]):
            with st.expander(f"{h['Tarih']} - {h['Sonuç']}"):
                st.write(f"**Yaş:** {h['age']}")
                st.write(f"**Kolesterol:** {h['chol']}")
                st.write(f"**Güven Oranı:** {h['prob']}")
    else:
        st.warning("Henüz bir analiz yapılmadı.")

    st.divider()
    st.markdown("### 👩‍💻 Geliştirici")
    st.write("**Sinem Özdemir**")
    st.caption("Bilgisayar Mühendisliği Öğrencisi")
    st.divider()
    st.warning(
        "**⚠️ Uyarı:** Bu uygulama yalnızca **eğitim amaçlı** bir prototiptir ve **tıbbi tavsiye yerine geçmez.**")

# ---  ANA EKRAN TASARIMI ---
apply_custom_styles()
st.title("❤️ Kalp Hastalığı Riski Tahmin Sistemi")
st.write("Verilerinizi girerek yapay zeka destekli risk analizini başlatabilirsiniz.")

input_container = st.container()
with input_container:
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Yaş", 1, 110, 23, help="Yaş, damar sağlığı üzerinde doğrudan etkilidir.")
        sex = st.selectbox("Cinsiyet", ["Male", "Female"])
        trestbps = st.number_input("Dinlenme Kan Basıncı (mmHg)", 80, 200, 120)
        chol = st.number_input("Kolesterol (mg/dl)", 100, 600, 200)
    with col2:
        cp = st.selectbox("Göğüs Ağrısı Tipi", ["typical angina", "atypical angina", "non-anginal", "asymptomatic"])
        thalch = st.number_input("Maksimum Kalp Atış Hızı", 60, 220, 150)
        exang = st.checkbox("Egzersizle Gelen Göğüs Ağrısı Var mı?")
        oldpeak = st.slider("ST Depresyonu (Oldpeak)", 0.0, 6.0, 1.0, step=0.1)

# --- 6. TAHMİN VE ANALİZ ---
st.divider()
if st.button("🚀 Analizi Gerçekleştir"):
    with st.spinner('Yapay zeka katmanları kontrol ediliyor...'):
        time.sleep(1.2)

        input_data = pd.DataFrame({
            'age': [age], 'trestbps': [trestbps], 'chol': [chol],
            'thalch': [thalch], 'oldpeak': [oldpeak],
            'fbs': [False], 'exang': [exang], 'sex': [sex],
            'cp': [cp], 'restecg': ['normal']
        })

        input_encoded = pd.get_dummies(input_data)
        for col in features:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[features]

        # Tahmin ve Olasılık Hesaplama
        prediction = model.predict(input_encoded)[0]
        prob = model.predict_proba(input_encoded)[0]
        risk_olasiligi = prob[1] * 100
        current_time = time.strftime("%d/%m/%Y %H:%M:%S")

        # --- YENİ: Risk Seviyesi ve Renk Belirleme ---
        if risk_olasiligi < 30:
            risk_seviyesi = "Düşük"
            res_text = "✅ Düşük Risk"
            risk_color = "green"
        elif 30 <= risk_olasiligi < 65:
            risk_seviyesi = "Orta"
            res_text = "⚠️ Orta Risk"
            risk_color = "orange"
        else:
            risk_seviyesi = "Yüksek"
            res_text = "🚨 Yüksek Risk"
            risk_color = "red"

        # Geçmişe detaylı veriyi ekle
        st.session_state.history.append({
            "Tarih": current_time,
            "Sonuç": res_text,
            "Risk Seviyesi": risk_seviyesi,
            "age": age,
            "chol": chol,
            "prob": f"%{risk_olasiligi:.1f}"
        })

        # --- SONUÇ PANELİ ---
        st.subheader(f"📌 Analiz Sonucu (Derecelendirilmiş)")
        res_col1, res_col2, res_col3 = st.columns(3)

        with res_col1:
            if risk_seviyesi == "Düşük":
                st.success(f"**Düşük Risk**\n\nOlasılık: %{risk_olasiligi:.2f}")
            elif risk_seviyesi == "Orta":
                st.warning(f"**Orta Risk**\n\nOlasılık: %{risk_olasiligi:.2f}")
            else:
                st.error(f"**Yüksek Risk**\n\nOlasılık: %{risk_olasiligi:.2f}")

        with res_col2:
            st.metric("Sizin Kolesterolünüz", f"{chol}", delta=f"{chol - 200} (Ref: 200)", delta_color="inverse")
        with res_col3:
            st.metric("Kan Basıncı", f"{trestbps}", delta=f"{trestbps - 120} (Ref: 120)", delta_color="inverse")

        # --- 7. GÖRSELLEŞTİRME ---
        st.divider()
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("💡 Model Karar Faktörleri")
            importances = model.feature_importances_
            feat_df = pd.DataFrame({'Özellik': features, 'Önem': importances}).sort_values(by='Önem',
                                                                                           ascending=False).head(5)
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(x='Önem', y='Özellik', data=feat_df, palette="Purples_r", ax=ax)
            st.pyplot(fig)

        with c2:
            st.subheader("🩺 Tavsiyeler")
            if risk_seviyesi == "Yüksek":
                st.error("🚨 Kritik risk seviyesi! Acil bir tıbbi kontrol önerilir.")
            elif risk_seviyesi == "Orta":
                st.warning("⚠️ Bazı değerleriniz sınırda. Yaşam tarzı değişikliği ve kontrol gerekebilir.")
            else:
                st.info("✅ Verileriniz model bazında güvenli bölgede görünüyor. Sağlıklı yaşama devam!")

        # --- 8. ANA SAYFA İNDİRME BUTONU ---
        st.divider()
        st.subheader("📥 Raporlama")
        history_df = pd.DataFrame(st.session_state.history)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            history_df.to_excel(writer, index=False, sheet_name='Analiz_Gecmisi')

        st.download_button(
            label="📥 Tüm Analiz Geçmişini Excel Olarak İndir",
            data=buffer.getvalue(),
            file_name=f'kalp_analiz_raporu_{time.strftime("%Y%m%d")}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )