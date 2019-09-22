import sys
import win32com.client
 
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("Connection lost. ")
    exit()

################################################
# PLUS 공통 OBJECT
g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
 

# 코스피 200 종목 가져와 추가
codelist = g_objCodeMgr.GetGroupCodeList(180)
for code in codelist :
    print(code, g_objCodeMgr.CodeToName(code))

print(len(codelist))
