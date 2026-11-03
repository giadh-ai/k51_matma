
import os
import pyodbc
import pandas as pd
import gradio as gr
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)


# ==============================
# 1. CẤU HÌNH KẾT NỐI SQL SERVER
# ==============================

def connect_sql_server():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={os.getenv('SQL_SERVER', '127.0.0.1,1433')};"
        f"DATABASE={os.getenv('SQL_DATABASE', 'northwind')};"
        f"UID={os.getenv('SQL_USER', 'sa')};"
        f"PWD={os.getenv('SQL_PASSWORD', 'Vietnam@123')};"
        "TrustServerCertificate=yes;"
        "Connection Timeout=10;"
    )

    return pyodbc.connect(connection_string)


# ==============================
# 2. ĐỌC DỮ LIỆU VÀ HUẤN LUYỆN
# ==============================

def analyze_revenue():
    conn = None
    fig = None

    try:
        # Kết nối cơ sở dữ liệu
        conn = connect_sql_server()

        query = """
            SELECT
                Quantity,
                UnitPrice,
                (Quantity * UnitPrice) AS Revenue
            FROM [Order Details]
        """

        df = pd.read_sql_query(query, conn)

        if df.empty:
            raise ValueError("Bảng Order Details không có dữ liệu.")

        # Chuẩn hóa dữ liệu
        df = df.dropna(
            subset=["Quantity", "UnitPrice", "Revenue"]
        )

        if len(df) < 5:
            raise ValueError(
                "Cần ít nhất 5 dòng dữ liệu để phân tích."
            )

        # X: biến đầu vào
        X = df[["Quantity", "UnitPrice"]]

        # y: biến cần dự báo
        y = df["Revenue"]

        # Chia dữ liệu huấn luyện và kiểm tra
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        # Huấn luyện mô hình
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Dự báo trên tập kiểm tra
        y_pred = model.predict(X_test)

        # Tạo bảng kết quả
        result_df = X_test.copy()
        result_df["Revenue_Actual"] = y_test
        result_df["Revenue_Predicted"] = y_pred
        result_df["Error"] = (
            result_df["Revenue_Actual"]
            - result_df["Revenue_Predicted"]
        )

        result_df = result_df.reset_index(drop=True)
        result_df = result_df.round(2)

        # Tính các chỉ số đánh giá
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(
            y_test, y_pred
        ) ** 0.5

        # Vẽ biểu đồ
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.scatter(
            y_test,
            y_pred,
            alpha=0.65,
            edgecolors="black",
            label="Dữ liệu dự báo"
        )

        min_value = min(y_test.min(), y_pred.min())
        max_value = max(y_test.max(), y_pred.max())

        ax.plot(
            [min_value, max_value],
            [min_value, max_value],
            linestyle="--",
            label="Dự báo lý tưởng"
        )

        ax.set_xlabel("Doanh thu thực tế")
        ax.set_ylabel("Doanh thu dự báo")
        ax.set_title("So sánh doanh thu thực tế và dự báo")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Thông tin mô hình
        metrics = f"""
### Kết quả phân tích

- **Tổng số bản ghi:** {len(df)}
- **Số mẫu huấn luyện:** {len(X_train)}
- **Số mẫu kiểm tra:** {len(X_test)}
- **R²:** {r2:.4f}
- **MAE:** {mae:.4f}
- **RMSE:** {rmse:.4f}

### Phương trình hồi quy

`Revenue = {model.intercept_:.4f} + `
`({model.coef_[0]:.4f} × Quantity) + `
`({model.coef_[1]:.4f} × UnitPrice)`
"""

        status = (
            "Phân tích thành công! "
            "Đã kết nối SQL Server và huấn luyện mô hình."
        )

        return status, result_df, fig, metrics

    except Exception as e:
        return (
            f"Không thể phân tích dữ liệu: {str(e)}",
            pd.DataFrame(),
            None,
            ""
        )

    finally:
        if conn is not None:
            conn.close()


# ==============================
# 3. THIẾT KẾ GIAO DIỆN GRADIO
# ==============================

with gr.Blocks(
    title="Phân tích doanh thu Northwind",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # 📊 PHÂN TÍCH VÀ DỰ BÁO DOANH THU

        **Cơ sở dữ liệu:** Northwind — SQL Server

        Ứng dụng sử dụng hồi quy tuyến tính để phân tích
        mối quan hệ giữa số lượng, đơn giá và doanh thu.
        """
    )

    with gr.Row():
        analyze_btn = gr.Button(
            "Kết nối SQL Server và phân tích",
            variant="primary"
        )

    status_output = gr.Textbox(
        label="Trạng thái",
        interactive=False
    )

    metrics_output = gr.Markdown(
        label="Chỉ số đánh giá mô hình"
    )

    gr.Markdown("## Biểu đồ dự báo")

    plot_output = gr.Plot(
        label="Doanh thu thực tế và dự báo"
    )

    gr.Markdown("## Bảng kết quả dự báo")

    table_output = gr.Dataframe(
        label="Dữ liệu kiểm tra",
        interactive=False
    )

    analyze_btn.click(
        fn=analyze_revenue,
        inputs=[],
        outputs=[
            status_output,
            table_output,
            plot_output,
            metrics_output
        ]
    )

    gr.Markdown(
        """
        ---
        *Ứng dụng minh họa khai phá dữ liệu và học máy
        trên cơ sở dữ liệu bán hàng Northwind.*
        """
    )


# ==============================
# 4. KHỞI ĐỘNG WEB SERVER
# ==============================

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
