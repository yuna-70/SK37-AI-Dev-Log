"""TIL: Streamlit + PyMySQL 조건 검색 (대륙/인구수 필터링) (2026-09-17) — 개념 설명은 README.md 참고"""

import streamlit as st
import pymysql

st.title("대륙 및 인구수 조건별 도시 검색")
st.divider()

continent = st.sidebar.selectbox("대륙 선택", ['Asia', 'Europe', 'North America', 'Africa'])

with st.form("search_form"):
    min_pop = st.number_input("최소 인구수를 입력하세요", value=1000000, step=500000)
    submitted = st.form_submit_button("DB 검색 실행")

if submitted:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='world',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn.cursor() as cursor:
        sql = """
        SELECT C.Name AS 도시명, CO.Name AS 국가명, C.Population AS 인구수
        FROM city C
        INNER JOIN country CO ON C.CountryCode = CO.Code
        WHERE CO.Continent = %s AND C.Population >= %s
        ORDER BY C.Population DESC LIMIT 10;
        """
        cursor.execute(sql, (continent, min_pop))
        result = cursor.fetchall()

        st.success(f"{continent} 대륙 / {min_pop:,}명 이상 도시 검색 완료!")
        st.table(result)

    conn.close()