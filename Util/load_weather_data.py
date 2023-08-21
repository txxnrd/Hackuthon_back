import requests
end_point = {
    "여의도": "/1156054000/37.52638860108943/126.93512931714196/서울%20영등포구%20여의도동/SCH/여의도한강공원",
    "반포": "/1165057000/37.5097007912995/126.994629809971/%EC%84%9C%EC%9A%B8%20%EC%84%9C%EC%B4%88%EA%B5%AC%20%EB%B0%98%ED%8F%AC2%EB%8F%99/SCH/%EB%B0%98%ED%8F%AC%ED%95%9C%EA%B0%95%EA%B3%B5%EC%9B%90"
}

def get_weather_data(place, day_after_today, is_PM):
    response = requests.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="+place+"한강공원+날씨")
    res = response.text.split("week_list")[1]
    res = res.split("\\ul")[0]
    res = res.split('blind">')[1:-1]
    
    if day_after_today < 0 or day_after_today > 9:
        return "fail..."
    
    weather = res[day_after_today*4+is_PM].split("<")[0]
    high_temp = res[day_after_today*4+2].split("span>")[1].split("°")[0]
    low_temp = res[day_after_today*4+3].split("span>")[1].split("°")[0]
    
    return [weather, high_temp, low_temp]

#print(get_weather_data("여의도", 0, True))