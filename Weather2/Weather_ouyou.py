import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# タイトルと説明
st.title("天気アプリ")
st.write("調べたい地域を選んでください。")

# 地域の選択肢（都道府県名：cityコード）
city_code_list = {
    "東京都": "130010",
    "大阪府": "270000",
    "北海道": "016010",
    "福岡県": "400010"
}

# セレクトボックスで選択
city_code_index = st.selectbox("地域を選んでください。", city_code_list.keys())
city_code = city_code_list[city_code_index]

# 選択中の地域表示
st.write("選択中の地域:", city_code_index)

# 天気APIにリクエスト
url = "https://weather.tsukumijima.net/api/forecast/city/" + city_code
response = requests.get(url)
weather_json = response.json()

# 現在の時間取得
now_hour = datetime.now().hour

# 時間帯ごとの降水確率を取得
if 0 <= now_hour < 6:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T00_06']
elif 6 <= now_hour < 12:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T06_12']
elif 12 <= now_hour < 18:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T12_18']
else:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T18_24']

# 現在の降水確率を表示
weather_now_text = "現在の降水確率 : " + weather_now
st.write(weather_now_text)

# 日別の降水確率をDataFrame化
df1 = pd.DataFrame(weather_json['forecasts'][0]['chanceOfRain'], index=["今日"])
df2 = pd.DataFrame(weather_json['forecasts'][1]['chanceOfRain'], index=["明日"])
df3 = pd.DataFrame(weather_json['forecasts'][2]['chanceOfRain'], index=["明後日"])

# 結合して全体表示
df_all = pd.concat([df1, df2, df3])
st.write("3日間の降水確率一覧")
st.dataframe(df_all)
