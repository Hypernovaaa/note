import os, shutil, json, random, sys, logging, glob
from pprint import pprint
import pandas as pd 
from collections import defaultdict
import yaml 
from datetime import datetime 

def get_commission(income:float):
    '''计算业绩提成的系数 
    Arguments:
        income 总业绩
    Returns:
        ratio 系数
    '''
    for interval, ratio in config["commission"].items():
        start = float(interval.split(",")[0])
        end = float(interval.split(",")[1])
        if income > start and income <= end:
            return ratio
    raise ValueError("业绩系数没有找到！")

sale2income = defaultdict(list)  #  销售：[成交日期, 成交金额]
sale2ratio = defaultdict(float)  # 销售：销售提成系数
sale2final = defaultdict(lambda : [0] * 8)  # 销售: 成单业绩 退费 实际业绩	提成 周挑战激励	绩效 总计 本月提成奖金

data_path = "7月销售提成.xlsx"
config = yaml.safe_load(open("config.yaml"))

# 计算本月退费
df = pd.read_excel(data_path, sheet_name='业绩明细')
for idx, line in df.iterrows():
    saler = line["销售"]
    r_money = 0 if pd.isnull(line["退费金额"]) else line["退费金额"]
    sale2final[saler][1] += r_money

# 计算历史退费 
df = pd.read_excel(data_path, sheet_name='退费明细')
for idx, line in df.iterrows():
    saler = line["销售"]
    if not saler in sale2final:
        continue
    r_money = 0 if pd.isnull(line["退费金额"]) else line["退费金额"]
    sale2final[saler][1] += r_money

# 计算总业绩　
df = pd.read_excel(data_path, sheet_name='业绩明细')
for idx, line in df.iterrows():
    saler = line["销售"]
    income = 0 if pd.isnull(line["成交金额"]) else line["成交金额"]
    pay_date = line["成单时间"]
    sale2income[saler].append((pay_date, income))

# 计算销售提成系数
for saler, date_income in sale2income.items():
    all_income = sum(i[1] for i in date_income)
    sale2final[saler][0] = all_income
    ratio = get_commission(all_income)
    sale2ratio[saler] = ratio


# 计算实际业绩
for saler, final in sale2final.items():
    final[2] = final[0] - final[1]

# 计算绩效
for saler, final in sale2final.items():
    final[3] = final[2] * sale2ratio[saler]

# 计算激励
for saler, income in sale2income.items():
    # 计算每个星期
    for week_start, week_end, strategy_id in config["timeinterval"]:
        week_start = datetime.strptime(str(week_start), "%Y%m%d").date()
        week_end = datetime.strptime(str(week_end), "%Y%m%d").date()
        week_income = 0                   # 周收入总计
        
        for date, day_income in income:
            if date.date() < week_end and date.date() > week_start:
                week_income += day_income
        
        for reward_interal, reward in config["reward"][strategy_id].items():
            start = int(reward_interal.split(",")[0])
            end = int(reward_interal.split(",")[1])
            if week_income > start and week_income <= end:
                sale2final[saler][4] += reward
                print(saler, week_start, week_end, reward)
                break


pprint(sale2final)

df = pd.DataFrame.from_dict(sale2final, orient="index")
df.columns = ["成单业绩","退费","实际业绩","提成","周挑战激励","绩效","总计","本月提成奖金"]
# 重置索引，把名字放到一列
df.reset_index(inplace=True)
df.rename(columns={"index": "姓名"}, inplace=True)

df.to_excel("res.xlsx", index=False)
