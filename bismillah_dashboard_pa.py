# -*- coding: utf-8 -*-
"""Bismillah Dashboard PA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yX_LQnrGndmMBsV7D5ptjZ8qpJeuRncT
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, roc_curve, auc

# Load data
train_data = pd.read_csv("TRAIN.csv")
test_data = pd.read_csv("TEST.csv")
smote = pd.read_csv("SMOTE.csv")

# Memisahkan fitur dan target untuk data training
X_train = smote[['TX_TIME_DAYS', 'TX_AMOUNT']]
y_train = smote['TX_FRAUD']

# Memisahkan fitur dan target untuk data testing
X_test = test_data[['TX_TIME_DAYS', 'TX_AMOUNT']]
y_test = test_data['TX_FRAUD']

# Train model
base_estimator = DecisionTreeClassifier(max_depth=1)
model = AdaBoostClassifier(estimator=base_estimator, n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Model metrics
y_pred_train = model.predict(X_train)
accuracy = accuracy_score(y_train, y_pred_train)

true_negatives = np.sum(np.logical_and(y_train == 0, y_pred_train == 0))
false_positives = np.sum(np.logical_and(y_train == 0, y_pred_train == 1))
specificity = true_negatives / (true_negatives + false_positives)

true_positives = np.sum(np.logical_and(y_train == 1, y_pred_train == 1))
false_negatives = np.sum(np.logical_and(y_train == 1, y_pred_train == 0))
sensitivity = true_positives / (true_positives + false_negatives)

fpr, tpr, _ = roc_curve(y_train, model.predict_proba(X_train)[:, 1])
auc_score = auc(fpr, tpr)

# Statistik deskriptif
mean_amount = smote['TX_AMOUNT'].mean()
mean_days = smote['TX_TIME_DAYS'].mean()
min_amount = smote['TX_AMOUNT'].min()
max_amount = smote['TX_AMOUNT'].max()
min_days = smote['TX_TIME_DAYS'].min()
max_days = smote['TX_TIME_DAYS'].max()

# Streamlit app
st.set_page_config(page_title="Dashboard PA", layout="wide")

# Sidebar for navigation
st.sidebar.title("Dashboard Navigasi")
page = st.sidebar.selectbox("Pilih halaman", ["Informasi", "Prediksi"])

if page == "Informasi":
    st.title("💳 Deteksi Penipuan Kartu Kredit")
    st.write("## Apa Itu Penipuan Kartu Kredit?")
    st.write("""
        Penipuan kartu kredit adalah tindakan kriminal yang melibatkan penggunaan kartu kredit milik orang lain tanpa izin untuk melakukan transaksi. Tindakan ini bisa merugikan korban secara finansial dan merusak reputasi mereka. Dashboard ini bertujuan untuk mengembangkan model deteksi dini penipuan kartu kredit yang efektif dan akurat menggunakan model AdaBoost untuk mengklasifikasikan apakah suatu transaksi kartu kredit tergolong sah atau penipuan.
    """)

    st.write("## Apa itu AdaBoost?")
    st.write("""
        Adaptive Boosting (AdaBoost) merupakan metode ensemble yang menggabungkan beberapa model lemah menjadi satu model yang lebih kuat dengan memberikan bobot lebih kepada data yang sulit diprediksi. AdaBoost digunakan untuk mengklasifikasi data pada kelasnya masing-masing. AdaBoost mencari kategori kelas berdasarkan dengan nilai bobot yang dimiliki oleh kelas, proses ini terus dilakukan berulang sehingga terdapat pembaruan nilai pada kelas. Pada adaboost nilai bobot akan terus bertambah pada setiap iterasinya dari bobot nilai yang salah pada setiap iterasinya.
    """)

    st.write("## Bagaimana hasil evaluasi model Adaboost?")
    st.write(f"Akurasi AdaBoost: {accuracy:.4f}")
    st.write(f"Sensitivitas AdaBoost: {sensitivity:.4f}")
    st.write(f"Spesifisitas AdaBoost: {specificity:.4f}")
    st.write(f"AUC Score Adaboost: {auc_score:.4f}")

    st.write("### Kurva ROC:")
    plt.figure(figsize=(10, 6))
    plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc_score:.4f})', color='darkgreen', linewidth=2)
    plt.plot([0, 1], [0, 1], color='navy', linewidth=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    st.pyplot(plt)

elif page == "Prediksi":
    st.title("Karakteristik Data")
    # CSS for centering text and background color
    st.markdown("""
        <style>
        .card {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 150px;
        }
        .card h5 {
            margin: 0;
            padding: 0;
            font-size: 16px;
        }
        .card h6 {
            margin: 0;
            padding: 0;
            font-size: 14px;

        }
        </style>
        """, unsafe_allow_html=True)

    # Display statistics in cards with colored background
    cols = st.columns(6)

    with cols[0]:
        st.markdown("<div class='card'><h5>Rata-Rata Nilai Transaksi</h5><h6>{:.2f} USD</h6></div>".format(mean_amount), unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='card'><h5>Rata-Rata Jeda Hari Transaksi</h5><h6>{:.2f} Hari</h6></div>".format(mean_days), unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='card'><h5>Nilai Transaksi Minimum</h5><h6>{:.2f} USD</h6></div>".format(min_amount), unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='card'><h5>Nilai Transaksi Maksimum</h5><h6>{:.2f} USD</h6></div>".format(max_amount), unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='card'><h5>Jeda Hari Minimum</h5><h6>{} Hari</h6></div>".format(min_days), unsafe_allow_html=True)

    with cols[5]:
        st.markdown("<div class='card'><h5>Jeda Hari Maksimum</h5><h6>{} Hari</h6></div>".format(max_days), unsafe_allow_html=True)

    st.title("Prediksi")
    st.write("### Input Manual untuk Prediksi")
    tx_time_days = st.number_input("Masukkan TX_TIME_DAYS")
    tx_amount = st.number_input("Masukkan TX_AMOUNT")

    if st.button("Prediksi"):
        X_new = np.array([[tx_time_days, tx_amount]])
        y_new_pred = model.predict(X_new)[0]
        prediction_label = "Penipuan" if y_new_pred == 1 else "Sah"
        st.write(f"Transaksi tersebut diprediksi: {prediction_label}")

        fig = px.scatter(smote, x='TX_AMOUNT', y='TX_FRAUD', color='TX_FRAUD',
                         title="Scatter Plot - Nilai Transaksi (USD) vs TX_FRAUD",
                         labels={'TX_AMOUNT': 'Nilai Transaksi (USD)', 'TX_FRAUD': 'Jenis Transaksi'},
                         color_discrete_map={0: '#3498db', 1: '#34495E'})
        fig.add_trace(go.Scatter(x=[tx_amount], y=[y_new_pred], mode='markers', name='Data Prediksi',
                                 marker=dict(color='black', size=15, symbol='x', line=dict(color='blue', width=2))))
        fig.update_layout(
            legend=dict(
                title="Kategori",
                itemsizing='constant',
                traceorder='normal',
                font=dict(size=12)
            )
        )
        st.plotly_chart(fig)
