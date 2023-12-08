import math 
print('本计算方式适用等额本息计算方式,详细计算过程可参考:')
print('https://zhuanlan.zhihu.com/p/670993980?')



# 提前还款金额与月供关系
def gongjijin(x, week, lilv):
    #x 还款金额
    #贷款总月数
    #lilv 贷款利率
    x = cash-x
    y = x*lilv/12*(1+lilv/12)**week
    y1 = (1+lilv/12)**week-1
    y = y/y1
    return y

#贷款金额与月供关系
def gongjijin1(x, week, lilv, yihuanbenjin=0, yihuanlixi=0):
    #x 贷款总额
    #week 贷款月数
    #贷款利率
    #yihuanbenjin 已经还得本金
    #yihuanlixi 已还利息
    has_week = week-math.floor((yihuanbenjin+yihuanlixi)/gongjijin(0, week, lilv))
    y = (x-yihuanbenjin)*lilv/12*(1+lilv/12)**has_week
    y1 = (1+lilv/12)**has_week-1
    y = y/y1
    return y

#现金收益与房贷持平的关系
def daikuan(cash, has_week):
    qq = (1+0.025)**math.ceil(has_week/12)
    xuyao = math.ceil(gongjijin1(cash, week, lilv)*has_week/qq)
    return xuyao

#精确计算提前还多少，刚好在剩下贷款年限内以公积金完全抵房贷,适合房贷大于公积金每月入账的
def tiqianhuan(cash, week, yihuanbenjin, yihuanlixi, gongjijins,gongjijin_shengyu):
    #cash 贷款总额
    #week 贷款总月数，
    #yihuanbenjin 已还本金，
    #yihuanlixi 已还利息，
    #gongjijins 公积金每月入账，
    #gongjijin_shengyu 目前公积金账户剩余，
    has_week = week-math.floor((yihuanbenjin+yihuanlixi)/gongjijin1(500000, week, lilv))
    yue_lilv = lilv/12
    gong_yue = gongjijin_shengyu/has_week
    yuegong = gong_yue+gongjijins
    next_yuegong = cash-yihuanbenjin-yuegong*((1+yue_lilv)**has_week-1)/((1+yue_lilv)**has_week*yue_lilv)
    print('您只需提前还款{}即可保证接下来的{}月靠公积金覆盖房贷。'.format(next_yuegong, has_week))
    xianjin = daikuan(cash, has_week)
    print('根据您目前贷款信息(包括贷款,已还本金等信息),按银行复利{}利率，在接下来{}年存{}元即可覆盖房贷。'.format(rank_lilv, math.ceil(has_week/12), xianjin))
    #return next_yuegong
while(True):
    cash = int(input('请输入贷款总额(例如500000):'))
    week = int(input('请输入贷款总月数(例如300):'))
    lilv = float(input('请输入贷款利率(例如0.031):'))
    rank_lilv = float(input('请输入银行存款利率(例如0.025):'))
    yihuanbenjin = float(input('已还本金(例如20000):'))
    yihuanlixi = float(input('已还利息(例如40000):'))
    gongjijins = float(input('公积金每月入账(例如2000):'))
    gongjijin_shengyu = float(input('公积金账户剩余(例如10000):'))
    next_yuegong = tiqianhuan(cash, week, yihuanbenjin, yihuanlixi, gongjijins,gongjijin_shengyu)
    flag = input('继续计算请输入Y,结束请输入E:')
    if flag == 'E':
        break
