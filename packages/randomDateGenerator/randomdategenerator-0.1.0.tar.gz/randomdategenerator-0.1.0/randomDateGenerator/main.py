import random

months=["January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"]
dates = []

def datesFill():    #fill the dates list
  for x in range(1,32):
    dates.append(x)
datesFill()

month = random.choice(months) #variables for random momnth&dates
date = random.choice(dates)

def randomChoice(month):
  if month == "january" or "march" or "may" or "july" or "august" or "october" or "december":
    return f"{date}. {month}"                                        #31 days

  if month == "april" or "june" or "september" or "november":
    if date >= 31:
      return f"{date - 1}. {month}"     
    else:
      return f"{date}. {month}"                                      # 30 days
    
  else:
    if date >= 30:                                                   #29 days
      return f"{29}. {month}"     
    else:
      return f"{date}. {month}"
      


print(randomChoice(month))