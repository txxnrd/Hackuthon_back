import requests

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