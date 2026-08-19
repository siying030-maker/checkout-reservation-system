import streamlit as st
from datetime import date, datetime

from core.google_api import (
    open_sheet,
    get_worksheet,
    append_row,
)


# ==================================================
# 頁面設定
# ==================================================

st.set_page_config(
    page_title="宿舍離宿預約",
    page_icon="🏠",
    layout="centered",
)


# ==================================================
# Google Sheet
# ==================================================

CHECKOUT_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1H0mwVCby43p8UGT8BiNT9ZQTvMH2LFD58Cf9OarxZtE/edit"
)


# ==================================================
# 宿舍 → Sheet
# ==================================================

SHEET_MAPPING = {
    "女一宿": "女一",
    "女二宿": "女二",
    "女三宿(涵青館)": "女三",
    "男一宿": "男一",
    "男三宿(涵青館)": "男三",
}


# ==================================================
# 儲存預約
# ==================================================

def save_checkout_reservation(
    dorm,
    room,
    name,
    checkout_date,
    checkout_time,
):

    # 找到宿舍對應的工作表
    sheet_name = SHEET_MAPPING.get(
        dorm
    )

    if not sheet_name:
        raise ValueError(
            "找不到對應宿舍工作表"
        )

    # 開啟 Google Sheet
    ss = open_sheet(
        CHECKOUT_URL
    )

    # 開啟對應工作表
    ws = get_worksheet(
        ss,
        sheet_name
    )

    # 日期
    date_text = checkout_date.strftime(
        "%Y/%m/%d"
    )

    # 時間
    time_text = checkout_time.strftime(
        "%H:%M"
    )

    # 寫入
    append_row(
        ws,
        [
            room,
            name,
            date_text,
            time_text,
        ]
    )


# ==================================================
# 標題
# ==================================================

st.title(
    "🏠 宿舍離宿預約系統"
)

st.info(
    "請填寫離宿資料，送出後即完成預約。"
)

st.divider()


# ==================================================
# 表單
# ==================================================

with st.form(
    "checkout_form",
    clear_on_submit=True,
):

    dorm = st.selectbox(
        "宿別",
        options=list(
            SHEET_MAPPING.keys()
        ),
        index=None,
        placeholder="請選擇宿舍",
    )

    room = st.text_input(
        "房號",
        placeholder="例如：81701",
    )

    name = st.text_input(
        "姓名",
        placeholder="請輸入姓名",
    )

    checkout_date = st.date_input(
        "離宿日期",
        value=None,
        min_value=date.today(),
        format="YYYY/MM/DD",
    )

    checkout_time = st.time_input(
        "離宿時間",
        value=None,
        step=1800,
    )

    submitted = st.form_submit_button(
        "送出離宿預約",
        type="primary",
        use_container_width=True,
    )


# ==================================================
# 送出處理
# ==================================================

if submitted:

    room = str(
        room
    ).strip()

    name = str(
        name
    ).strip()

    # ----------------------------------------------
    # 驗證
    # ----------------------------------------------

    if not dorm:

        st.error(
            "請選擇宿別"
        )

    elif not room:

        st.error(
            "請輸入房號"
        )

    elif not name:

        st.error(
            "請輸入姓名"
        )

    elif checkout_date is None:

        st.error(
            "請選擇離宿日期"
        )

    elif checkout_time is None:

        st.error(
            "請選擇離宿時間"
        )

    else:

        try:

            save_checkout_reservation(
                dorm=dorm,
                room=room,
                name=name,
                checkout_date=checkout_date,
                checkout_time=checkout_time,
            )

            st.success(
                "✅ 離宿預約完成"
            )

            st.write(
                f"宿別：{dorm}"
            )

            st.write(
                f"房號：{room}"
            )

            st.write(
                f"姓名：{name}"
            )

            st.write(
                "離宿時間："
                f"{checkout_date.strftime('%Y/%m/%d')} "
                f"{checkout_time.strftime('%H:%M')}"
            )

        except Exception as error:

            st.error(
                f"❌ 預約失敗：{error}"
            )