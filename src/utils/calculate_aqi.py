def calculate_air_quality_index(gas_resistance: float, temperature: float, humidity: float) -> tuple[float, str]:
    """
    ガス抵抗値、温度、湿度から空気質指数（AQI）を計算し、その評価を返します。

    :param gas_resistance: ガス抵抗値（オーム）
    :param temperature: 温度（摂氏）
    :param humidity: 相対湿度（パーセント）
    :return: AQI, AQIの評価
    """
    # ガス抵抗値による基本的なAQI計算
    if gas_resistance > 20000:
        aqi = 50  # 良好
    elif gas_resistance > 15000:
        aqi = 100  # 普通
    elif gas_resistance > 10000:
        aqi = 150  # やや悪い
    elif gas_resistance > 5000:
        aqi = 200  # 悪い
    elif gas_resistance > 1000:
        aqi = 300  # 非常に悪い
    else:
        aqi = 400  # 危険

    # 温度と湿度を考慮して補正（例として簡単な補正）
    if humidity > 70 or humidity < 30:
        aqi += 10  # 湿度が高すぎるか低すぎると補正
    if temperature > 30 or temperature < 10:
        aqi += 10  # 温度が高すぎるか低すぎると補正

    # AQIは0から500の範囲に制限
    aqi = min(max(aqi, 0), 500)

    # AQIに基づく評価
    if aqi <= 50:
        aqi_feeling = "良好"
    elif aqi <= 100:
        aqi_feeling = "普通"
    elif aqi <= 150:
        aqi_feeling = "やや悪い"
    elif aqi <= 200:
        aqi_feeling = "悪い"
    elif aqi <= 300:
        aqi_feeling = "非常に悪い"
    else:
        aqi_feeling = "危険"

    return aqi, aqi_feeling
