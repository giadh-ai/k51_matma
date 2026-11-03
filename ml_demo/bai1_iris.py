import pandas as pd
file_path = 'data/iris.csv'
df = pd.read_csv(file_path)

# --- Chuẩn bị dữ liệu ---
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# --- Huấn luyện mô hình SVM ---
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import plotly.graph_objects as go
import numpy as np

# Mã hóa nhãn
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Chia tập train/test
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Khởi tạo và huấn luyện mô hình SVM
model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# --- Ánh xạ lại nhãn số thành tên loài ---
y_test_labels = le.inverse_transform(y_test)
y_pred_labels = le.inverse_transform(y_pred)

# --- Đánh giá mô hình ---
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=le.classes_)

print("🔹 Độ chính xác của mô hình SVM:", round(accuracy * 100, 2), "%")
print("\n🔹 Báo cáo chi tiết:\n", report)

# --- Kết luận tự động dựa vào độ chính xác ---
if accuracy == 1.0:
    conclusion = "✅ Mô hình SVM rất tốt (có thể đang overfit – cần kiểm tra thêm dữ liệu)."
    conclusion_color = "green"
elif accuracy >= 0.8:
    conclusion = "🟩 Mô hình SVM hoạt động ổn, có thể dùng để dự đoán."
    conclusion_color = "limegreen"
elif accuracy >= 0.6:
    conclusion = "🟨 Mô hình SVM tạm ổn nhưng cần tinh chỉnh thêm tham số."
    conclusion_color = "orange"
else:
    conclusion = "🟥 Mô hình SVM yếu, cần cải thiện hoặc thay đổi kernel."
    conclusion_color = "red"

# --- Biểu đồ Gauge: Độ chính xác mô hình ---
fig1 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=accuracy * 100,
    title={'text': "🎯 Độ chính xác mô hình SVM (%)"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "green" if accuracy > 0.8 else "red"},
        'steps': [
            {'range': [0, 50], 'color': "lightcoral"},
            {'range': [50, 80], 'color': "khaki"},
            {'range': [80, 100], 'color': "lightgreen"}
        ],
        'threshold': {'line': {'color': "blue", 'width': 4}, 'value': accuracy * 100}
    }
))
fig1.add_annotation(text="🟥 0–50%: Mô hình yếu", x=0.5, y=-0.18, showarrow=False, font=dict(size=12, color="red"))
fig1.add_annotation(text="🟨 50–80%: Trung bình", x=0.5, y=-0.25, showarrow=False, font=dict(size=12, color="orange"))
fig1.add_annotation(text="🟩 80–100%: Tốt", x=0.5, y=-0.32, showarrow=False, font=dict(size=12, color="green"))
fig1.add_annotation(
    text=f"📋 Kết luận: {conclusion}",
    x=0.5, y=-0.45, showarrow=False, font=dict(size=14, color=conclusion_color)
)
fig1.update_layout(height=420, margin=dict(t=60, b=140))
fig1.show()

# --- Ma trận nhầm lẫn ---
fig2 = go.Figure(data=go.Heatmap(
    z=cm,
    x=le.classes_,
    y=le.classes_,
    text=cm,
    texttemplate="%{text}",
    hoverongaps=False,
    colorscale='Viridis',
    colorbar=dict(title='Số lượng')
))
fig2.update_layout(
    title='📊 Ma trận nhầm lẫn mô hình SVM theo tên loài',
    xaxis_title='Nhãn dự đoán',
    yaxis_title='Nhãn thực tế',
    annotations=[
        dict(
            text="💡 Màu càng đậm = số dự đoán đúng càng cao",
            x=0.5, y=-0.2, showarrow=False, xref="paper", yref="paper",
            font=dict(size=12, color="gray")
        )
    ]
)
fig2.show()

# --- Biểu đồ cột: So sánh nhãn thực tế và nhãn dự đoán ---
fig3 = go.Figure()
fig3.add_trace(go.Bar(name='Thực tế', x=np.arange(len(y_test_labels)), y=y_test_labels))
fig3.add_trace(go.Bar(name='Dự đoán', x=np.arange(len(y_pred_labels)), y=y_pred_labels))
fig3.update_layout(
    barmode='group',
    title='🔍 So sánh nhãn thực tế và nhãn dự đoán theo tên loài (SVM)',
    xaxis_title='Mẫu kiểm tra',
    yaxis_title='Tên loài',
    annotations=[
        dict(
            text="🟦 Thanh xanh: nhãn thật | 🟥 Thanh đỏ: nhãn dự đoán",
            x=0.5, y=-0.25, showarrow=False, xref="paper", yref="paper",
            font=dict(size=12, color="gray")
        )
    ]
)
fig3.show()
