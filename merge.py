from datetime import datetime
import time
import os
import glob
import xlsxwriter

def mergeSort(arr): 
    if len(arr) >1: 
        middle = len(arr)//2
        left = arr[:middle]
        right = arr[middle:]
  
        mergeSort(left) 
        mergeSort(right)
  
        left_index = right_index = index = 0
          
        while left_index < len(left) and right_index < len(right): 
            if left[left_index] < right[right_index]: 
                arr[index] = left[left_index]
                left_index+=1
            else: 
                arr[index] = right[right_index] 
                right_index+=1
            index+=1
          
        while left_index < len(left): 
            arr[index] = left[left_index] 
            left_index+=1
            index+=1
          
        while right_index < len(right): 
            arr[index] = right[right_index] 
            right_index+=1
            index+=1



workbook = xlsxwriter.Workbook('merge.xlsx')
worksheet = workbook.add_worksheet('My merge')
cell_format = workbook.add_format()
cell_format.set_num_format('#,##0.0000')

row = 0
for filename in glob.glob('*.log'):
    data = []
    sort = []
    total = []
    count = 0
    for count in range(8):
        data_start = time.perf_counter()
        time_dict = {}
        f = open(filename, "r+")
        for line in f:
            date_obj = datetime.fromisoformat(line.split(" ")[0])
            int_obj = int(datetime.timestamp(date_obj))
            if int_obj in time_dict:
                time_dict[int_obj].append(line)
            else:
                time_dict[int_obj] = [line]
        arr = list(time_dict.keys())
        data_end = time.perf_counter()
        data.append((data_end - data_start)*1000000)
        sort_start = time.perf_counter()
        mergeSort(arr)
        sort_end = time.perf_counter()
        sort.append((sort_end - sort_start)*1000000)
        total.append(sort[count] + data[count])
        if(count == 0):
            f = open(filename+"_mergesort.log", "w+")
            for a in arr:
                for line in time_dict[a]:
                    f.write(line)
        count+=1
    for i in range(3, len(data)):
        worksheet.write(row + i - 3, 0, filename)
        worksheet.write(row + i - 3, 1, data[i], cell_format)
        worksheet.write(row + i - 3, 2, sort[i], cell_format)
        worksheet.write(row + i - 3, 3, total[i], cell_format)
    row += 5
workbook.close()

# print(data)
# print(sort)
# print(total)
