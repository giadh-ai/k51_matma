import gradio as gr
import pyodbc
import hashlib
import base64

# pip install pymssql
# sudo apt install msodbcsql18

# ==========================
# CẤU HÌNH SQL SERVER
# ==========================
SERVER = "127.0.0.1"      # sửa lại nếu khác
DATABASE = "northwind"         # tên database
DB_USER = "sa"
DB_PASSWORD = "Vietnam@123"

# ==========================
# HÀM MÃ HÓA MẬT KHẨU
# Base64(SHA256(password))
# ==========================
def encode_password(password):
    sha256_hash = hashlib.sha256(
        password.encode("utf-8")
    ).digest()

    return base64.b64encode(
        sha256_hash
    ).decode("utf-8")


# ==========================
# KẾT NỐI SQL SERVER
# ==========================
def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    return conn


# ==========================
# ĐĂNG NHẬP
# ==========================
def login(username, password):

    if not username or not password:
        return "Vui lòng nhập tên đăng nhập và mật khẩu"

    try:

        encrypted_password = encode_password(password)

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT TOP 1 id, username
        FROM tbl_user
        WHERE username = ?
          AND password = ?
        """

        cursor.execute(
            sql,
            (username, encrypted_password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return f"Đăng nhập thành công. Xin chào {user.username}"
        else:
            return "Sai tên đăng nhập hoặc mật khẩu"

    except Exception as ex:
        return f"Lỗi kết nối SQL Server: {str(ex)}"


# ==========================
# GIAO DIỆN GRADIO
# ==========================
with gr.Blocks(title="Login System") as demo:

    gr.Markdown("# HỆ THỐNG ĐĂNG NHẬP")

    username = gr.Textbox(
        label="Tên đăng nhập",
        placeholder="Nhập username"
    )

    password = gr.Textbox(
        label="Mật khẩu",
        type="password"
    )

    btn_login = gr.Button("Đăng nhập")

    result = gr.Textbox(
        label="Kết quả",
        interactive=False
    )

    btn_login.click(
        fn=login,
        inputs=[username, password],
        outputs=result
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )