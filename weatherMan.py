import argparse
import calendar
import fnmatch
import os

parser=argparse.ArgumentParser(description="Weather man")
parser.add_argument("path",help="It's the path where data is placed")
parser.add_argument("-a",help="This is for the average month report")
parser.add_argument("-b",help="This is for bonus report")
parser.add_argument("-c",help="This is for the chart report")
parser.add_argument("-e",help="This is for the year report")
args = parser.parse_args()

def read_file(year_files):
    result = []
    temp = []
    headings = ""
    h = []
    for i in year_files:
        file = open(args.path + i,"r")
        file_data = file.read()
        headings = file_data.splitlines()[0]
        temp.append(file_data.splitlines()[1:])
    
    heading = dict()
    h = headings.split(sep = ",")
    
    for index, item in enumerate(h):
        heading[item] = index
    
    flattened = []
    for sublist in temp:
        for max in sublist:
            flattened.append(max)
            
    for item in flattened:
        result.append(item.split(","))
        
    return result,heading

def given_year(year):
    year_files = []
    
    min_temp_date = 0
    max_temp_date = 0
    max_humid_date = 0
    
    for file in os.listdir(args.path):
        if (fnmatch.fnmatch(file, '*' + year + '*.txt')):year_files.append(file)
    
    result,heading = read_file(year_files)
    
    max_temp = int(result[0][heading["Max TemperatureC"]])
    min_temp = int(result[0][heading["Min TemperatureC"]])
    max_humid = int(result[0][heading["Max Humidity"]])
    
    for item in result:
        if(item[heading["Max TemperatureC"]] == ""):
            continue
            
        high_temp = int(item[heading["Max TemperatureC"]])
        
        if (max_temp < high_temp):
            max_temp_date = item[heading["PKT"]]
            max_temp = high_temp
            
    for item in result:
        if(item[heading["Min TemperatureC"]] == ""):
            continue
        
        low_temp = int(item[heading["Min TemperatureC"]])
    
        if min_temp > low_temp:
            min_temp_date = item[heading["PKT"]]
            min_temp = low_temp
    
    for item in result:
        if(item[heading["Max Humidity"]] == ""):
            continue
        
        high_humid = int(item[heading["Max Humidity"]])
        
        if(max_humid < high_humid):
            max_humid_date = item[heading["PKT"]]
            max_humid = high_humid
        
    return [str(max_temp), max_temp_date, str(min_temp), min_temp_date, str(max_humid), max_humid_date]
    
def given_month(month,year):
    month_files = []
    sum_max_temp = 0
    sum_min_temp = 0
    sum_mean_humid = 0
    
    for file in os.listdir(args.path):
        if (fnmatch.fnmatch(file, "*" + year + '_' + month + '*.txt')):month_files.append(file)
    
    result,heading = read_file(month_files)
    
    for item in result:
        if(item[heading["Max TemperatureC"]] == ""):
            continue
        
        sum_max_temp = sum_max_temp + int(item[heading["Max TemperatureC"]])
    
    for item in result:
        if(item[heading["Min TemperatureC"]] == ""):
            continue
        
        sum_min_temp = sum_min_temp + int(item[heading["Min TemperatureC"]])

    for item in result:
        if(item[heading[" Mean Humidity"]] == ""):
            continue
        
        sum_mean_humid = sum_mean_humid + int(item[heading[" Mean Humidity"]])
    
    avg_max_temp = sum_max_temp / len(result)
    avg_min_temp = sum_min_temp / len(result)
    avg_mean_humid = sum_mean_humid / len(result)
    
    return [str(int(avg_max_temp)), str(int(avg_min_temp)), str(int(avg_mean_humid))]

def bar_chart_temp(month,year):
    month_files = []
    
    for file in os.listdir(args.path):
        if (fnmatch.fnmatch(file, "*" + year + '_' + month + '*.txt')):
            month_files.append(file)
            
    return read_file(month_files)

def bar_chart(month,year):
    result, heading = bar_chart_temp(month,year)
    count = 0

    for i in result:
        count = 0
        date = i[heading["PKT"]].split("-")[2]
        min_temp = i[heading["Min TemperatureC"]]
        max_temp = i[heading["Max TemperatureC"]]
        
        print(date, end="")

        if min_temp != "":
            min_temp = int(min_temp)
            while count < min_temp:
                output = "\33[49m\33[31m+\33[0m"
                print(output, end="")
                count += 1

            print(f" {min_temp}C")
        else:
            print("")

        count = 0
        print(date, end="")

        if max_temp != "":
            max_temp = int(max_temp)
            while count < max_temp:
                output = "\33[49m\33[96m+\33[0m"
                print(output, end="")
                count += 1

            print(f" {max_temp}C")
        else:
            print("")



def bar_chart_task5(month,year):
    result, heading = bar_chart_temp(month,year)
    count = 0
    
    for i in result:
        count = 0
        date = i[heading["PKT"]].split("-")[2]
        min_temp = i[heading["Min TemperatureC"]]
        max_temp = i[heading["Max TemperatureC"]]
        
        print(date, end="")
        
        # Print bar chart for Min TemperatureC
        while not min_temp == "" and count < int(min_temp):
            output = "\33[49m\33[96m+\33[0m"
            print(output, end="")
            count += 1

        count = 0
        # Print bar chart for Max TemperatureC
        while not max_temp == "" and count < int(max_temp):
            output = "\33[49m\33[31m+\33[0m"
            print(output, end="")
            count += 1
        
        # Print Max TempatureC
        if not max_temp == "":
            print(f" {max_temp}C", end="")
        else:
            print("", end="")
            
        # Print Min TempatureC
        if not min_temp == "":
            print(f" - {min_temp}C")
        else:
            print("")

def month_number_to_short_name(month_number):
    return calendar.month_abbr[month_number]

if(args.e):
    result = given_year(args.e)
    
    abbr = month_number_to_short_name(int(result[1].split(sep = "-")[1]))
    date = result[1].split(sep = "-")[2]
    print("Task 1")
    print(f"Highest: {result[0]}C on {abbr} {date}")
    abbr = month_number_to_short_name(int(result[3].split(sep = "-")[1]))
    date = result[3].split(sep = "-")[2]
    print(f"Lowest: {result[2]}C on {abbr} {date}")
    abbr = month_number_to_short_name(int(result[5].split(sep = "-")[1]))
    date = result[5].split(sep = "-")[2]
    print(f"Highest: {result[4]}% on {abbr} {date}")

if(args.a):
    month = args.a.split(sep = "/")[1]
    year = args.a.split(sep = "/")[0]
    
    result = given_month(month_number_to_short_name(int(month)), year)
    print("Task 2")
    print(f"Highest: {result[0]}C")
    print(f"Lowest: {result[1]}C")
    print(f"Highest: {result[2]}%")

if(args.c):
    month = args.c.split(sep = "/")[1]
    year = args.c.split(sep = "/")[0]
    
    print("Task 3")
    print(bar_chart(month_number_to_short_name(int(month)), year))

if(args.b):
    month = args.b.split(sep = "/")[1]
    year = args.b.split(sep = "/")[0]
    
    print("Task 4")
    print(bar_chart_task5(month_number_to_short_name(int(month)), year))