import streamlit as st
import pandas as pd
import numpy as np
import io
from hitung import (
    calculate_nonlinearity,
    calculate_sac,
    calculate_bic_nl,
    calculate_bic_sac,
    calculate_lap,
    calculate_dap
)

# Fungsi untuk menjelaskan masing-masing analisis
def get_explanation(metric):
    explanations = {
        "Nonlinearity (NL)": "Nonlinearity mengukur ketahanan S-Box terhadap serangan linear cryptanalysis. Semakin tinggi nilai nonlinearity, semakin sulit untuk menyerang S-Box menggunakan analisis linear.",
        "Strict Avalanche Criterion (SAC)": "SAC mengevaluasi apakah perubahan satu bit input mempengaruhi perubahan secara acak di seluruh bit output. Nilai SAC ideal mendekati 0.5.",
        "Bit Independence Criterion (BIC-NL)": "BIC-NL memeriksa apakah nonlinearity dari bit output bersifat independen satu sama lain.",
        "Bit Independence Criterion - SAC (BIC-SAC)": "BIC-SAC menguji independensi Strict Avalanche Criterion di seluruh bit output.",
        "Linear Approximation Probability (LAP)": "LAP menentukan seberapa baik fungsi linear dapat mendekati S-Box. Nilai LAP ideal mendekati 0.",
        "Differential Approximation Probability (DAP)": "DAP menghitung probabilitas pola diferensial tertentu dalam S-Box. Nilai DAP ideal mendekati 0."
    }
    return explanations.get(metric, "Tidak ada penjelasan untuk metrik ini.")

# Header aplikasi
st.markdown(
    """
    <h1 style='text-align: center; color: #0D47A1;'>🔒 S-Box Analysis Tool</h1>
    <p style='text-align: center; color: var(--text-primary);'>
        S-Box Analysis Tools adalah aplikasi berbasis Python untuk menganalisis keamanan matriks S-Box dalam kriptografi.
        Alat ini menghitung berbagai metrik untuk menilai kekuatan dan efektivitas S-Box terhadap serangan kriptografi.
    </p>
    """,
    unsafe_allow_html=True
)

# CSS untuk mendukung mode gelap dan terang
st.markdown(
    """
    <style>
    /* Sesuaikan gaya untuk mode terang */
    .stDataFrame {
        background-color: var(--background-secondary) !important;
        color: var(--text-primary) !important;
    }
    /* Atur tampilan tabel lebih jelas */
    table.dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    table.dataframe th, table.dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    table.dataframe th {
        background-color: var(--background-secondary);
        color: var(--text-primary);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Upload file Excel untuk S-Box
st.sidebar.title("📂 Unggah File")
uploaded_file = st.sidebar.file_uploader("Unggah file Excel untuk S-Box", type=["xlsx"])

if uploaded_file:
    try:
        # Membaca file Excel
        sbox_df = pd.read_excel(uploaded_file, header=None)

        if sbox_df.empty:
            st.error("File Excel kosong atau tidak valid!")
        else:
            # Tampilkan matriks S-Box
            st.markdown("### Matriks S-Box yang Diunggah:")
            st.dataframe(sbox_df)

            # Konversi S-Box ke list
            sbox = sbox_df.values.flatten().tolist()

            # Analisis
            results = {
                "Nonlinearity (NL)": calculate_nonlinearity(sbox),
                "Strict Avalanche Criterion (SAC)": calculate_sac(sbox),
                "Bit Independence Criterion (BIC-NL)": calculate_bic_nl(sbox),
                "Bit Independence Criterion - SAC (BIC-SAC)": calculate_bic_sac(sbox),
                "Linear Approximation Probability (LAP)": calculate_lap(sbox),
                "Differential Approximation Probability (DAP)": calculate_dap(sbox)
            }

            # Bagian hasil analisis
            st.sidebar.title("🔍 Pilih Analisis")
            selected_metric = st.sidebar.selectbox(
                "Pilih metrik untuk ditampilkan:",
                list(results.keys())
            )

            # Tampilkan penjelasan
            st.markdown(f"### {selected_metric}")
            st.info(get_explanation(selected_metric))

            # Tampilkan hasil
            value = results[selected_metric]
            if isinstance(value, float):
                st.success(f"*Hasil:* {value:.5f}")
            else:
                st.success(f"*Hasil:* {value}")

            # Ekspor hasil ke file Excel
            export_data = {
                "Summary": pd.DataFrame.from_dict(
                    results, orient="index", columns=["Value"]
                ).reset_index().rename(columns={"index": "Metric"})
            }

            # Tambahkan matriks untuk hasil tertentu (contoh: SAC atau BIC-SAC)
            if isinstance(results["Strict Avalanche Criterion (SAC)"], np.ndarray):
                export_data["SAC Matrix"] = pd.DataFrame(results["Strict Avalanche Criterion (SAC)"])

            if isinstance(results["Bit Independence Criterion - SAC (BIC-SAC)"], np.ndarray):
                export_data["BIC-SAC Matrix"] = pd.DataFrame(results["Bit Independence Criterion - SAC (BIC-SAC)"])

            # Ekspor ke Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                for sheet_name, df in export_data.items():
                    df.to_excel(writer, index=False, sheet_name=sheet_name)

            st.markdown("### Ekspor Hasil Analisis")
            st.download_button(
                label="📥 Exspor ke Excel",
                data=output.getvalue(),
                file_name="hasil_analisis_sbox.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
else:
    st.info("Silakan unggah file Excel untuk memulai analisis.")

# Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center;'>
        Developed by Group 6 using <b>Streamlit</b>
    </p>
    """,
    unsafe_allow_html=True
)