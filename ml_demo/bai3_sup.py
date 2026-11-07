
import os
import requests
import pandas as pd
import gradio as gr
import plotly.express as px

from sklearn.cluster import KMeans

# -----------------------------
# ⚙️ Thông tin Supabase
# -----------------------------

SUPABASE_URL = os.getenv(
    "SUPABASE_URL",
    "https://ocateixuzulwmrtxseom.supabase.co"
)

SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jYXRlaXh1enVsd21ydHhzZW9tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMTYyMTQsImV4cCI6MjA3MTc5MjIxNH0.w7PLqjLGj4hNNGDh81NwDodEUCCqVSVm_PL0FpYWif8"

# -----------------------------
# 📡 Lấy dữ liệu từ Supabase
# -----------------------------

def fetch_supabase_data():

    if not SUPABASE_API_KEY:
        raise ValueError("Chưa cấu hình SUPABASE_API_KEY!")

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }

    def fetch_all(table, columns):
        url = f"{SUPABASE_URL}/rest/v1/{table}"

        all_data = []
        offset = 0
        limit = 1000

        while True:
            params = {
                "select": columns,
                "limit": limit,
                "offset": offset
            }

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()
            all_data.extend(data)

            if len(data) < limit:
                break

            offset += limit

        return pd.DataFrame(all_data)

    # Lấy bảng orders
    orders = fetch_all(
        "orders",
        "order_id,customer_id"
    )

    # Lấy bảng order_details
    details = fetch_all(
        "order_details",
        "order_id,quantity,unit_price"
    )

    return orders, details


# -----------------------------
# 🧮 Xử lý dữ liệu
# -----------------------------

def process_data(n_clusters):

    orders, details = fetch_supabase_data()

    if orders.empty or details.empty:
        raise ValueError("Không có dữ liệu từ Supabase!")

    # JOIN dữ liệu
    df = pd.merge(
        orders,
        details,
        on="order_id",
        how="inner"
    )

    # Tính doanh thu
    df["revenue"] = (
        df["quantity"] * df["unit_price"]
    )

    # Gom nhóm theo khách hàng
    agg_df = (
        df.groupby("customer_id")
        .agg(
            OrderCount=("order_id", "count"),
            TotalRevenue=("revenue", "sum")
        )
        .reset_index()
    )

    # Lọc doanh thu > 0
    agg_df = agg_df.dropna()

    agg_df = agg_df[
        agg_df["TotalRevenue"] > 0
    ].copy()

    agg_df["OrderCount"] = (
        agg_df["OrderCount"].astype(int)
    )

    agg_df["TotalRevenue"] = (
        agg_df["TotalRevenue"].astype(float)
    )

    if len(agg_df) < n_clusters:
        raise ValueError(
            f"Chỉ có {len(agg_df)} khách hàng hợp lệ, "
            f"không đủ để chia thành {n_clusters} cụm."
        )

    # -----------------------------
    # 🤖 K-Means
    # -----------------------------

    X = agg_df[
        ["OrderCount", "TotalRevenue"]
    ]

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    agg_df["Cluster"] = (
        kmeans.fit_predict(X)
    )

    agg_df["Cluster"] = (
        agg_df["Cluster"].astype(str)
    )

    # -----------------------------
    # 📊 Biểu đồ Plotly
    # -----------------------------

    fig = px.scatter(
        agg_df,
        x="OrderCount",
        y="TotalRevenue",
        color="Cluster",
        hover_data=["customer_id"],
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Phân nhóm khách hàng tiềm năng bằng K-Means",
        labels={
            "OrderCount": "Số lượng đơn hàng",
            "TotalRevenue": "Tổng doanh thu",
            "Cluster": "Nhóm khách hàng"
        }
    )

    fig.update_traces(
        marker=dict(size=11, opacity=0.8)
    )

    fig.update_layout(
        template="plotly_white",
        height=550
    )

    # -----------------------------
    # 📈 Thống kê cụm
    # -----------------------------

    summary = (
        agg_df.groupby("Cluster")
        .agg(
            CustomerCount=("customer_id", "count"),
            AvgOrders=("OrderCount", "mean"),
            AvgRevenue=("TotalRevenue", "mean")
        )
        .reset_index()
    )

    summary["AvgOrders"] = (
        summary["AvgOrders"].round(2)
    )

    summary["AvgRevenue"] = (
        summary["AvgRevenue"].round(2)
    )

    return agg_df, summary, fig


# -----------------------------
# 🚀 Hàm chạy Gradio
# -----------------------------

def run_clustering(n_clusters):

    try:
        agg_df, summary, fig = process_data(
            int(n_clusters)
        )

        total_customers = len(agg_df)

        total_revenue = agg_df[
            "TotalRevenue"
        ].sum()

        total_orders = agg_df[
            "OrderCount"
        ].sum()

        status = f"""
### Kết quả phân tích thành công!

- Tổng khách hàng: **{total_customers:,}**
- Tổng số đơn hàng: **{total_orders:,}**
- Tổng doanh thu: **{total_revenue:,.2f}**
- Số nhóm khách hàng: **{int(n_clusters)}**
"""

        return (
            status,
            agg_df,
            summary,
            fig
        )

    except Exception as e:
        return (
            f"❌ Lỗi: {str(e)}",
            pd.DataFrame(),
            pd.DataFrame(),
            None
        )


# -----------------------------
# 🎨 Giao diện Gradio
# -----------------------------

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="Customer Segmentation - KMeans"
) as demo:

    gr.Markdown("""
    # 📊 CUSTOMER SEGMENTATION DASHBOARD

    ### Phân nhóm khách hàng tiềm năng bằng thuật toán K-Means

    Dữ liệu được lấy trực tiếp từ Supabase Data API.
    """)

    with gr.Row():

        n_clusters = gr.Slider(
            minimum=2,
            maximum=10,
            value=3,
            step=1,
            label="Số cụm K-Means"
        )

        run_btn = gr.Button(
            "🚀 Phân tích khách hàng",
            variant="primary"
        )

    status = gr.Markdown(
        "Nhấn nút để bắt đầu phân tích dữ liệu."
    )

    gr.Markdown("## 📈 Biểu đồ phân nhóm khách hàng")

    plot = gr.Plot(
        label="Customer Segmentation"
    )

    gr.Markdown("## 👥 Danh sách khách hàng")

    customer_table = gr.Dataframe(
        label="Thông tin khách hàng theo cụm",
        interactive=False
    )

    gr.Markdown("## 📊 Thống kê các nhóm khách hàng")

    summary_table = gr.Dataframe(
        label="Cluster Summary",
        interactive=False
    )

    run_btn.click(
        fn=run_clustering,
        inputs=[n_clusters],
        outputs=[
            status,
            customer_table,
            summary_table,
            plot
        ]
    )

    gr.Markdown("""
    ---
    **Technology:** Python | Gradio | Supabase | Pandas | Scikit-learn | Plotly
    """)


# -----------------------------
# 🌐 Khởi chạy ứng dụng
# -----------------------------

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )
