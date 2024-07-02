def calculate_discomfort_index(temperature: float, humidity: float) -> tuple[float, str]:
    """
    温度と湿度から不快指数を計算し、それに基づいて体感を返します。

    :param temperature: 温度（摂氏）
    :param humidity: 相対湿度（パーセント）
    :return: 不快指数, 体感
    """
    discomfort_index = 0.81 * temperature + 0.01 * humidity * (0.99 * temperature - 14.3) + 46.3
    discomfort_index = round(discomfort_index, 2)

    if discomfort_index <= 55:
        feeling = "寒い"
    elif 55 < discomfort_index <= 60:
        feeling = "肌寒い"
    elif 60 < discomfort_index <= 65:
        feeling = "何も感じない"
    elif 65 < discomfort_index <= 70:
        feeling = "快い"
    elif 70 < discomfort_index <= 75:
        feeling = "暑くない"
    elif 75 < discomfort_index <= 80:
        feeling = "やや暑い"
    elif 80 < discomfort_index <= 85:
        feeling = "暑くて汗が出る"
    else:
        feeling = "暑くてたまらない"

    return discomfort_index, feeling
