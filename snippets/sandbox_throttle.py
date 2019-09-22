import time
import win32com.client

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

remainTime = objCpCybos.LimitRequestRemainTime / 1000.
print('remainTime: {remainTime}'.format(remainTime=remainTime))

LT_TRADE_REQUEST = 0  # 주문, 계좌 관련 통신
LT_NONTRADE_REQUEST = 1   # 시세 관련 통신
LT_SUBSCRIBE = 2  # 실시간 통신 관련

remainCount = objCpCybos.GetLimitRemainCount(LT_NONTRADE_REQUEST)    
print('remainCount: {remainCount}'.format(remainCount=remainCount))
