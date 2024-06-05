import os
import fnmatch
import sys
import calendar

n = len(sys.argv)
all_files = []
script_name = sys.argv[0]
path = sys.argv[1]

def given_year(year):
    year_files = []
    result = []
    temp = []
    min_temp_date = 0
    max_temp_date = 0
    max_humid_date = 0
    
    for file in os.listdir(path):
        if (fnmatch.fnmatch(
            file, '*'+year+'*.txt')):
            year_files.append(file)
    
    for i in year_files:
        file = open(path+i,"r")
        file_data = file.read()
        temp.append(file_data.splitlines()[1:])
        
        
    flattened = []
    for sublist in temp:
        for max in sublist:
            flattened.append(max)
            
    for item in flattened:
        result.append(item.split(","))
    
    max_temp = int(result[0][1])
    min_temp = int(result[0][3])
    max_humid = int(result[0][7])
    
    for item in result:
        if(item[1] == ""):
            continue
            
        high_temp = int(item[1])
        
        if (max_temp < high_temp):
            max_temp_date = item[0]
            max_temp = high_temp
            
    for item in result:
        if(item[3] == ""):
            continue
        
        low_temp = int(item[3])
        
        if min_temp > low_temp:
            min_temp_date = item[0]
            min_temp = low_temp
    
    for item in result:
        if(item[7] == ""):
            continue
        
        high_humid = int(item[7])
        
        if(max_humid < high_humid):
            max_humid_date = item[0]
            max_humid = high_humid
        
    return [
        str(max_temp),
        max_temp_date,
        str(min_temp),
        min_temp_date,
        str(max_humid),
        max_humid_date
        ]
    
def given_month(month,year):
    month_files = []
    result = []
    temp = []
    sum_max_temp = int(0)
    sum_min_temp = int(0)
    sum_mean_humid = int(0)
    
    for file in os.listdir(path):
        if (fnmatch.fnmatch(
            file, "*"+year+'_'+month+'*.txt')):
            month_files.append(file)
    
    for i in month_files:
        file = open(path+i,"r")
        file_data = file.read()
        temp.append(file_data.splitlines()[1:])
        
        
    flattened = []
    for sublist in temp:
        for max in sublist:
            flattened.append(max)
            
    for item in flattened:
        result.append(item.split(","))
    
    for item in result:
        if(item[1] == ""):
            continue
        
        sum_max_temp = sum_max_temp+int(item[1])
    
    for item in result:
        if(item[1] == ""):
            continue
        
        sum_max_temp = sum_max_temp+int(item[1])
    
    for item in result:
        if(item[3] == ""):
            continue
        
        sum_min_temp = sum_min_temp+int(item[3])

    for item in result:
        if(item[8] == ""):
            continue
        
        sum_mean_humid = sum_mean_humid+int(item[8])
    
    avg_max_temp = sum_max_temp/len(result)
    avg_min_temp = sum_min_temp/len(result)
    avg_mean_humid = sum_mean_humid/len(result)
    
    return [
        str(int(avg_max_temp)),
        str(int(avg_min_temp)),
        str(int(avg_mean_humid))
        ]

def bar_chart_temp(month,year):
    month_files = []
    result = []
    temp = []
    
    for file in os.listdir(path):
        if (fnmatch.fnmatch(
            file, "*"+year+'_'+month+'*.txt')):
            month_files.append(file)
    
    for i in month_files:
        file = open(path+i,"r")
        file_data = file.read()
        temp.append(file_data.splitlines()[1:])
            
    flattened = []
    for sublist in temp:
        for max in sublist:
            flattened.append(max)
            
    for item in flattened:
        result.append(item.split(","))
        
    return result

def bar_chart(month,year):
    data = bar_chart_temp(month,year)
    count = 0
    
    for i in data:
        count = 0
        print(
            i[0].split(sep = "-")[2]
            ,end = ""
            )
        
        while not i[3] == "" and count < int(i[3]):
            output = "\33[{}m".format(49) + "\33[{}m".format(31) + "+" + "\33[{}m".format(0)
            print(output, end = "")
            count += 1

            
        if (not i[1] == ""):
            print(i[1]+"C")
        else:
            print("")
        count = 0
        
        print(i[0].split(sep = "-")[2],end = "")
        while not i[3] == "" and count < int(i[3]):
            output = "\33[{}m".format(49) + "\33[{}m".format(96) + "+" + "\33[{}m".format(0)
            print(output, end = "")
            count += 1
 
        if (not i[3] == ""):
            print(i[3]+"C")
        else:
            print("")

def bar_chart_task5(month,year):
    data = bar_chart_temp(month,year)
    count = 0
    
    for i in data:
        count = 0
        print(i[0].split(sep = "-")[2],end = "")
        
        while not i[3] == "" and count < int(i[3]):
            output = "\33[{}m".format(49) + "\33[{}m".format(96) + "+" + "\33[{}m".format(0)
            print(output, end = "")
            count += 1
    
        count = 0        
        while not i[3] == "" and count < int(i[3]):
            output = "\33[{}m".format(49) + "\33[{}m".format(31) + "+" + "\33[{}m".format(0)
            print(output, end = "")
            count += 1
         
        if (not i[3] == ""):
            print(" "+i[3],end = "C")
        else:
            print("",end = "")
            
        if (not i[1] == ""):
            print(" - "+i[1]+"C")
        else:
            print("")

def month_number_to_short_name(month_number):
    return calendar.month_abbr[month_number]


for i in range(2,n,2):
    
    flag = sys.argv[i]
    year_option = sys.argv[i+1]

    if(flag == "-e"):
        result = given_year(year_option)
        abbr = month_number_to_short_name(int(result[1].split(sep = "-")[1]))
        date = result[1].split(sep = "-")[2]
        print("Task 1")
        print(
            "Highest: "+result[0]
            + "C on "+abbr+" "+date
            )
        abbr = month_number_to_short_name(int(result[3].split(sep = "-")[1]))
        date = result[3].split(sep = "-")[2]
        print("Lowest: "+ result[2]
              +"C on "+ abbr+" "+date
            )
        abbr = month_number_to_short_name(int(result[5].split(sep = "-")[1]))
        date = result[5].split(sep = "-")[2]
        print("Highest: "+ result[4]
              +"%"+" on "+ abbr+" "+date
            )
        
    if(flag == "-a"):
        month = year_option.split(sep = "/")[1]
        year = year_option.split(sep = "/")[0]
        
        result = given_month(
            month_number_to_short_name
            (int(month)),year
            )
        print("Task 2")
        print("Highest: "+ result[0]+"C")
        print("Lowest: "+ result[1]+"C")
        print("Highest: "+ result[2]+"%")

    if(flag == "-c"):
        month = year_option.split(sep = "/")[1]
        year = year_option.split(sep = "/")[0]
        
        print("Task 3")
        print(bar_chart(
            month_number_to_short_name(int(month)),
            year
            ))

    if(flag == "-d"):
        month = year_option.split(sep = "/")[1]
        year = year_option.split(sep = "/")[0]
        
        print("Task 4")
        print(bar_chart_task5(
            month_number_to_short_name(int(month)),
            year
            ))



