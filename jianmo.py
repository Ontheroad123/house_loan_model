#目前国家规定房贷最多抵扣个税240个月
#本研究只考虑等额本息的情况（本人就是等额本息50w贷款方式,300个月）
#假如手里50w现金，现在考虑是否需要提前还款
#保留房贷，对个税有极大好处

import math 
import matplotlib.pyplot as plt
cash = 500000
week = 300
lilv = 0.031
# 提前还款金额与月供关系
def gongjijin(x, week, lilv):
    x = cash-x
    y = x*lilv/12*(1+lilv/12)**week
    y1 = (1+lilv/12)**week-1
    y = y/y1
    return y
print(gongjijin(0, week, lilv))
#print((40264+26768)/gongjijin(0, week, lilv))
a = []
b = []
for i in range(500):
    a.append(i*1000)
    b.append(float(gongjijin(i*1000, week, lilv)))
    print(i*1000, float(gongjijin(i*1000, week, lilv)))
plt.scatter(a,b)
plt.yticks(range(0,3000,300))
plt.xlabel('Early repay')
plt.ylabel('Monthly payment')
plt.savefig('公积金提前还款与月供关系.png')
plt.cla()
# 假设目前有50w现金, 提前还款从0-50w，剩下现金按照目前2.5%的复利计算
def zichan(cash, x, y=2000, o=14000):
    #x 提前还款金额
    #y 公积金账户每月入的钱
    #o 目前公积金账户余额
    q1 = (cash-x)*(1+0.025)**25 #剩余现金的利息
    geshui = 0
    if cash-x>0:
        geshui =1200*20
    q2 = (y-gongjijin(x, week, lilv))*300+o #公积金账户的钱
    
    total = q1 + q2 + geshui
    #print(x, q1, q2, geshui, total)
    return q1, q2, geshui, total
res = zichan(500000,100000)
print(res)
res = zichan(500000,0)
print(res)
a = []
b = []
c = []
d = []
e = []
for i in range(51):
    a.append(i*10000)
    b.append(float(zichan(500000, i*10000)[0]))
    c.append(float(zichan(500000, i*10000)[1]))
    d.append(float(zichan(500000, i*10000)[2]))
    e.append(float(zichan(500000, i*10000)[3]))

plt.plot(a,b, 'b*--', alpha=1, markersize='3',linewidth=0.5, label='cash interest')
plt.plot(a,c, 'rs--', alpha=1, markersize='3',linewidth=0.5, label='Housing fund')
plt.plot(a,d, 'go--', alpha=1, markersize='3',linewidth=0.5, label='Tax savings')
plt.plot(a,e, 'y^--', alpha=1, markersize='3',linewidth=0.5, label='Total')
plt.legend()
plt.savefig('公积金提前还款与总资产关系.png')
plt.cla()
# a = []
# b = []
# c = []
# for i in range(10):
#     for j in range(i):
#         a.append(i*10000)
#         b.append(j*10000)
#         c.append(float(zichan(i*10000, j*10000)[3]))

# import matplotlib.pyplot as plt1
# plt1.plot(a,c, label='cash total')
# plt1.legend()
# plt1.savefig('现金与提前还款的关系.png')

#个税计算
def shui(x, zhuanxiang, fujia, qita, flag):
    #zhuanxiang 专项扣除五险一金这些
    #fujia 专项附加扣除（除房贷外的，比如小孩，老人等）
    #qita 依法确定的其他扣除
    #flag 是否有房贷
    nashui = 0
    jiesheng = 0
    y = x-60000-zhuanxiang-fujia-qita-12000
    if not flag:
        y = x + 12000
    if y<0:
        nashui = 0
    elif y<36000:
        nashui = y*0.03
        jiesheng = 12000*0.03
    elif y<144000:
        nashui = 36000*0.03 + (y-36000)*0.1
        jiesheng = 12000*0.1
    elif y<300000:
        y = y-2520
        nashui = 36000*0.2 + (144000-36000)*0.1 + (y-144000)*0.2
        jiesheng = 12000*0.2
    elif y<420000:
        y = y-16920
        nashui = 36000*0.03 + (144000-36000)*0.1 + (300000-144000)*0.2+(y-300000)*0.25
        jiesheng = 12000*0.25
    elif y<660000:
        y = y-31920
        nashui = 36000*0.03 + (144000-36000)*0.1 + (300000-144000)*0.2+(420000-300000)*0.25+(y-420000)*0.3
        jiesheng = 12000*0.3
    elif y<960000:
        y = y-52920
        nashui = 36000*0.03 + (144000-36000)*0.1 + (300000-144000)*0.2+(420000-300000)*0.25+(660000-420000)*0.3+(y-660000)*0.35
        jiesheng = 12000*0.35
    else:
        y = y-85920
        nashui = 36000*0.03 + (144000-36000)*0.1 + (300000-144000)*0.2+(420000-300000)*0.25+(660000-420000)*0.3+(960000-660000)*0.35+(y-960000)*0.45
        jiesheng = 12000*0.45
    #print('应纳税所得额：{},  应纳税额：{}'.format(y, nashui))
    return nashui, jiesheng

hq = shui(500000, 0, 0, 0, True)
print(hq)
a = []
b = []
c = []
for i in range(100):
    a.append(i*10000)
    b.append(shui(i*10000, 0, 0, 0, True)[0])
    c.append(shui(i*10000, 0, 0, 0, True)[1])
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(a,b, 'b')
ax1.text(72000,0,(72000,0),color='r')
ax1.set_xlabel('Annual income')
ax1.set_ylabel('Ratepaying',labelpad=-1,color='b')

ax2 = ax1.twinx()
ax2.plot(a,c, 'y')
ax2.set_ylabel('Saving',labelpad=-1, color='y')
fig.savefig('年收入与纳税.png')
plt.cla()
#贷款金额与月供关系
def gongjijin1(x, week, lilv, yihuanbenjin=0, yihuanlixi=0):
    #x 贷款总额
    #week 贷款月数
    #贷款利率
    #yihuanbenjin 已经还得本金
    #yihuanlixi 已还利息
    print(gongjijin(0, week, lilv))
    has_week = week-math.floor((yihuanbenjin+yihuanlixi)/gongjijin(0, week, lilv))
    y = (x-yihuanbenjin)*lilv/12*(1+lilv/12)**has_week
    y1 = (1+lilv/12)**has_week-1
    y = y/y1
    return y
#现金收益与房贷持平的关系
def daikuan(qq):
    qq = qq*(1+0.025)**25
    mu = float((1+0.031/12)**300-1)
    zi = float(0.031/12*(1+0.031/12)**300)
    dai = qq*mu/zi/300
    return dai
#print(100000/daikuan(100000))
a = []
b = []
c = []
for i in range(51):
    x = i*10000
    fangdai = gongjijin1(x, week, lilv, 0, 0)*week
    xianjin = x*(1+0.025)**25
    #print(x, fangdai, xianjin)
    a.append(x)
    b.append(fangdai)
    c.append(xianjin)

fig,ax = plt.subplots(1,2,sharey = "row")
fig.subplots_adjust(wspace = 0)
ax1 = ax[0]
ax1.plot(a,b, 'b*--', alpha=1, markersize='3',linewidth=0.5, label='Total amount of loan')
ax1.plot(a,c, 'rs--', alpha=1, markersize='3',linewidth=0.5, label='Compound interest')
ax1.annotate('394281,730974', 
             xy=(394281,730974),#箭头末端位置
             
             xytext=(20000,800000),#文本起始位置
             
             #箭头属性设置
            arrowprops=dict(facecolor='#74C476', 
                            # shrink=1,#箭头的收缩比
                            # alpha=0.6,
                            # width=7,#箭身宽
                            # headwidth=30,#箭头宽
                            # hatch='--',#填充形状
                            # headlength=0.1,#身与头比
                            #其它参考matplotlib.patches.Polygon中任何参数
                           ),
            )
ax1.set_xlabel('Cash',{'size':10})
ax1.set_ylabel('Total',{'size':10},labelpad=-5)

#房贷与复利时间的关系
def fulitime(x, year):
    fuli = x*(1+0.025)**year
    print(year, fuli)
    return fuli
a = []
b = []
for i in range(30):
    a.append(i)
    b.append(fulitime(500000, i))
ax2 = ax[1]
ax2.plot(a,b)
ax2.set_xlabel('Year')
ax2.annotate('16,742253', 
             xy=(16,730974),#箭头末端位置
             
             xytext=(1,900000),#文本起始位置
             
             #箭头属性设置
            arrowprops=dict(facecolor='#74C476', 
                            # shrink=1,#箭头的收缩比
                            # alpha=0.6,
                            # width=7,#箭身宽
                            # headwidth=40,#箭头宽
                            # hatch='--',#填充形状
                            # headlength=0.8,#身与头比
                            # #其它参考matplotlib.patches.Polygon中任何参数
                           ),
            )
plt.savefig('房贷与复利时间的关系.png')

#根据贷款总额，贷款总月数，已还本金，已还利息，公积金每月入账，目前公积金账户剩余，精确计算提前还多少，刚好在剩下贷款年限内以公积金完全抵房贷
def tiqianhuan(x, week, yihuanbenjin, yihuanlixi, gongjijins,gongjijin_shengyu):
    has_week = week-math.floor((yihuanbenjin+yihuanlixi)/gongjijin1(500000, week, lilv))
    yue_lilv = lilv/12
    gong_yue = gongjijin_shengyu/has_week
    yuegong = gong_yue+gongjijins
    next_yuegong = x-yihuanbenjin-yuegong*((1+yue_lilv)**has_week-1)/((1+yue_lilv)**has_week*yue_lilv)
    return next_yuegong
next_yuegong = tiqianhuan(500000, 360, 26768, 40264, 1700, 0)
#print(next_yuegong)