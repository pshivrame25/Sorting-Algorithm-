import random
from datetime import datetime
import time
import os
import glob
import xlsxwriter

def partition(arr, low, high):
	i = low - 1
	pivot = arr[random.randint(low, high)]

	for j in range(low, high):
		if arr[j] <= pivot:
			i = i+1
			arr[i],arr[j] = arr[j],arr[i]
	arr[i+1],arr[high] = arr[high],arr[i+1]
	return i+1

def quickSort(arr, low, high):
	if low < high:
		pi = partition(arr, low, high)
		quickSort(arr, low, pi-1)
		quickSort(arr, pi+1, high)


workbook = xlsxwriter.Workbook('quick.xlsx')
worksheet = workbook.add_worksheet('My Quick')
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
        quickSort(arr, 0, len(arr) - 1)
        sort_end = time.perf_counter()
        sort.append((sort_end - sort_start)*1000000)
        total.append(sort[count] + data[count])
        if(count == 0):
            f = open(filename+"_quicksort.log", "w+")
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