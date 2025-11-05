from datetime import datetime


moscow_times_str = "Wednesday, October 2, 2002"
moscow_times_format = "%A, %B %d, %Y"
moscow_times_date = datetime.strptime(moscow_times_str, moscow_times_format)


guardian_str = "Friday, 11.10.13"
guardian_format = "%A, %d.%m.%y"
guardian_date = datetime.strptime(guardian_str, guardian_format)

daily_news_str = "Thursday, 18 August 1977"
daily_news_format = "%A, %d %B %Y"
daily_news_date = datetime.strptime(daily_news_str, daily_news_format)

print("The Moscow Times:")
print(f"Формат: {moscow_times_format}")
print(f"Результат: {moscow_times_date}")
print()

print("The Guardian:")
print(f"Формат: {guardian_format}")
print(f"Результат: {guardian_date}")
print()

print("Daily News:")
print(f"Формат: {daily_news_format}")
print(f"Результат: {daily_news_date}")

