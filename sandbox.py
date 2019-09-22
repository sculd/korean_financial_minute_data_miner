import time
import win32com.client

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("Connection lost. ")
    exit()

stock_code = 'A' + '006980'
objStockChart.SetInputValue(0, stock_code)

objStockChart.SetInputValue(1, ord('1'))  # 요청 구분 '1': 기간, '2': 개수
objStockChart.SetInputValue(2, 20190920)
objStockChart.SetInputValue(3, 20190920)

count = 10
#objStockChart.SetInputValue(1, 2)  # 개수로 받기
#objStockChart.SetInputValue(4, count)  # 조회 개수
objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
#objStockChart.SetInputValue(6, 'm')  # 'M', 'W', 'D', 'm', 'T'


objStockChart.SetInputValue(6, ord('m'))  # 'M', 'W', 'D', 'm', 'T'
objStockChart.SetInputValue(7, 1)  # period        
objStockChart.SetInputValue(9, ord('1'))  # 수정주가


objStockChart.BlockRequest()
rqStatus = objStockChart.GetDibStatus()

# -1: error, 0: normal, 1: pending
if rqStatus != 0:
    print("GetDibStatus {}".format(rqStatus))
    exit()
else:
    print("normal request response {rqStatus}".format(rqStatus=rqStatus))

# 0: stock code, 1: number of fields, ..., 3: received count
print(objStockChart.GetHeaderValue(0))
print(objStockChart.GetHeaderValue(1))
print(objStockChart.GetHeaderValue(2))
print(objStockChart.GetHeaderValue(3))

count_received = objStockChart.GetHeaderValue(3)
print('count_received: {count_received}'.format(count_received=count_received))

for r in range(count_received):
    data = []
    data.append(objStockChart.GetDataValue(0, r))
    data.append(objStockChart.GetDataValue(1, r))
    data.append(objStockChart.GetDataValue(2, r))
    data.append(objStockChart.GetDataValue(3, r))
    data.append(objStockChart.GetDataValue(4, r))
    data.append(objStockChart.GetDataValue(5, r))
    data.append(objStockChart.GetDataValue(6, r))
    print(data)
