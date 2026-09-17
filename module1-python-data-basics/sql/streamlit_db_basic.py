"""TIL: Streamlit + PyMySQL 기본 연동 (2026-09-17) — 개념 설명은 README.md 참고"""

import streamlit as st
import pymysql

st.title("world DB 한국 주요 도시 현황")

def get_korea_cities():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='world',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn.cursor() as cursor:
        sql = "SELECT Name AS 도시명, District AS 시도, Population AS 인구수 FROM city WHERE CountryCode = 'KOR' LIMIT 10;"
        cursor.execute(sql)
        result = cursor.fetchall()

    conn.close()
    return result

data = get_korea_cities()

st.subheader("한국 상위 10개 도시 목록")
st.divider()
st.table(data)