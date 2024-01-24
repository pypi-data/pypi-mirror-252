# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime

import demjson
import numpy as np
import pandas as pd
import requests
from frame import (
    data_center,  # frame 软连接到trade模块的frame
    stock_func,
)
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Scatter
from pyecharts.commons.utils import JsCode
from sqlalchemy import text

from tradeTools import Decorator, helpers


class Mgr():
    def __init__(self):
        self.oldDc = data_center.use()

    # @Decorator.loadData(path="data")
    def getST(self, dateTime=20210101, is_real_time=False, **kwargs):
        _dirPath = (os.path.dirname(__file__))
        fileName = os.sep.join(
            [_dirPath, r"data", "SThistory", "SThistory.conf"])
        with open(fileName) as f:
            total = json.load(f)

        stSymbols = {}
        for _symbol, data in total.items():
            _data = data.copy()
            if "delist" in _data:
                del _data["delist"]
            df = pd.DataFrame(_data).T
            df.index = pd.to_datetime(df.index)
            df = df[df.index <= str(dateTime)]
            if df.empty:
                continue
            df.sort_index(ascending=False, inplace=True)
            opt = df.iloc[0]["opt"]
            newName = df.iloc[0]["newName"]
            if opt in ["*ST", "ST"] or re.search("ST|退", newName):
                __symbol = _symbol.split(".")[1]+"."+_symbol.split(".")[0]
                stSymbols[__symbol] = {"newName": newName, "opt": opt}
        return pd.DataFrame(stSymbols).T

    # 获取上市满1年的股票
    # 过滤st股
    def getSymbols(self, dateTime=20210101, years=-1, isFilterSt=True, is_real_time=False) -> list:
        """_summary_

        Args:
            dateTime (int, optional): _description_. Defaults to 20210101.
            years (int, optional): 上市时间约束，默认满一年. Defaults to -1.
            isFilterSt (bool, optional): 是否过滤st股,注意如果dateTime 大于5月会取最新年报期 Defaults to True.
            is_real_time (bool, optional): _description_. Defaults to False.

        Returns:
            list: _description_
        """
        if not hasattr(self, 'listDf') or is_real_time:
            self.listDf = helpers.getSymbolsInfo(is_real_time=is_real_time)
            listDf = self.listDf
        else:
            listDf = self.listDf
        start = datetime.strptime(
            str(dateTime), '%Y%m%d') + pd.tseries.offsets.DateOffset(years=years)
        symbols = listDf[listDf.listingDate <= str(start)].index.tolist()
        if isFilterSt:
            symbols = list(
                set(symbols) - set(self.getST(dateTime=dateTime).index.tolist()))
        return listDf.loc[symbols]

    @Decorator.firstLoad
    @Decorator.loadData(path="data")
    def gen_idx_data(self, index_symbol, is_real_time=False, **kwargs):
        if not hasattr(self, "oldDc"):
            self.oldDc = data_center.use()
        maxDate = 0
        fileName = kwargs["fileName"]
        if os.path.exists(fileName):
            oldDf = pd.read_csv(fileName, index_col=0,)
            maxDate = oldDf["time"].max()
        sql = "SELECT code,time,close from `index_day_data` "
        sql += f"WHERE code = '{index_symbol}'"
        if maxDate:
            sql += f" and time>{maxDate}"
        df = pd.read_sql(sql, self.oldDc.database.conn)
        if df.empty:
            return oldDf
        df['date'] = pd.to_datetime(df['time'], format='%Y%m%d')
        df.set_index('date', inplace=True)

        if maxDate:
            df = pd.concat([oldDf, df])
        df[index_symbol] = df.close / df.close.shift(1) - 1
        return df

    @Decorator.firstLoad
    @Decorator.loadData(path="data")
    def genSymbolRateData(self, symbol, is_real_time=True, **kwargs):
        # 生成间隔数据收益率数据
        if not hasattr(self, "oldDc"):
            self.oldDc = data_center.use()
        maxDate = 0
        fileName = kwargs["fileName"]
        if os.path.exists(fileName):  # 读取已有数据文件
            if os.stat(fileName).st_size == 0:
                oldDf = pd.DataFrame()
            else:
                oldDf = pd.read_csv(fileName, index_col=0,)
            # if not oldDf.empty:
                maxDate = oldDf["time"].max()
        # 多取一条历史数据为了算当日收益率
        sql = "SELECT code,time,close,volume "
        if symbol[-6:].startswith("1"):
            sql += f"from `bond_day_data` WHERE code = '{symbol}'"
        else:
            sql += f"from `tdx_day_data` WHERE code = '{symbol}'"
        if maxDate:
            sql += f" and time >={maxDate}"
        # 使用text函数将SQL语句包装为一个可执行对象
        sql = text(sql)
        df = pd.read_sql(sql, self.oldDc.database.conn)
        if df.empty:
            if maxDate:
                return oldDf
            return pd.DataFrame()

        df['date'] = pd.to_datetime(df['time'], format='%Y%m%d')
        df.set_index('date', inplace=True)

        df["lastTime"] = df.time.shift()
        df["lastClose"] = df.close.shift()

        def _getRehabilitationClose(hang):  # 复权
            begTime = hang.lastTime
            endTime = hang.time
            symbol = hang.code
            dividends = self.oldDc.query_dividends(stock_id=symbol,
                                                begtime=begTime,
                                                endtime=endTime)
            pre_close = hang.lastClose
            if dividends[symbol]:
                for dividend in dividends[symbol]:
                    pre_close = stock_func.get_dividend_pre_price(
                        pre_close, dividend[1])  # 前复权
            return (hang.close / pre_close) - 1

        df["rate"] = df.apply(_getRehabilitationClose, axis=1)
        if maxDate:
            df = df[df.time > maxDate]
            df = pd.concat([oldDf, df])
            df['date'] = pd.to_datetime(df['time'], format='%Y%m%d')
            df.set_index('date', inplace=True)
        return df

    @Decorator.loadData(path="data")
    def genSymbolTScore(self, symbol, frequency, windows,):  # 滚动z分数
        allData = self.genSymbolRateData(symbol=symbol, frequency=frequency)
        if allData.empty:
            return pd.DataFrame()
        allData['mRate'].fillna(0, inplace=True)  # 停牌的日期。收益率为设为0
        allData['mean'] = allData['mRate'].rolling(windows).mean()
        allData['std'] = allData['mRate'].rolling(windows).std(ddof=1)
        allData["ZScore"] = (allData['mRate'] - allData['mean'])/allData['std']
        allData["TScore"] = 50+10*allData["ZScore"]
        return allData[['mRate', 'mean', 'std', 'ZScore', 'TScore']]

    def genTradeDays(self, begTime: int, frequency: int = 20, is_real_time=False):
        # todo resample
        # 根据换仓频率生成交易日列表
        # frequency 交易日间隔
        df = self.genIDXData(indexSymbol="SH.000001",
                             is_real_time=is_real_time)
        df = df[df.index >= str(begTime)]

        return df.iloc[0::frequency]

    def getSymbolRateData(self, symbol, is_real_time=False):
        if not hasattr(self, 'symbolRateData'):
            self.symbolRateData = {}
        if symbol not in self.symbolRateData:
            symbolRateData = self.genSymbolRateData(symbol=symbol,
                                                    is_real_time=is_real_time)
            if symbolRateData.empty:
                print(f"{symbol}无历史行情数据")
            self.symbolRateData[symbol] = symbolRateData
        return self.symbolRateData.get(symbol)

    def getSymbolsData(self, symbols, endDate):
        rates = []
        marketValues = []
        for symbol in symbols:
            rateDf = self.genSymbolRateData(symbol=symbol)
            star = endDate.replace(endDate.year - 2)
            df = rateDf[(star <= rateDf.index) & (rateDf.index <= endDate)]
            rate = df["mRate"]
            marketValue = df["MarketV"]
            rate.name = symbol
            marketValue.name = symbol
            rates.append(pd.DataFrame(rate))
            marketValues.append(pd.DataFrame(marketValue))
        symbolsReturn = pd.concat(rates, axis=1)
        marketValue = pd.concat(marketValues, axis=1)
        marketValue["TOTAL"] = marketValue.sum(axis=1)
        marketValue = (marketValue.T / marketValue.TOTAL).T  # 求权重
        marketValue = marketValue.iloc[-1]
        marketValue = marketValue.drop("TOTAL")
        return symbolsReturn, marketValue

    def genReturn(self, beg, end, symbols, weight=[]):
        rate = []
        for symbol in symbols:
            df = self.genSymbolRateData(symbol=symbol, is_real_time=True)
            # 计算累计收益率
            s = df.loc[(str(beg) < df.index) & (df.index <= str(end))]["rate"]

            s.name = symbol
            rate.append(s)
        if not rate:
            return 0
        rateDf = pd.concat(rate, axis=1)
        rateDf = rateDf.fillna(0)  # 停牌股。当日的收益率为0
        # 如果多个交易日。由初始交易日的权重和前一日的净值。得出前一日的权重比例。再和当日的收益率点积
        if rateDf.shape[0] <= 1:
            rate = np.dot(rateDf.iloc[-1], weight)
        else:
            cumprodDf = (1 + rateDf).cumprod()
            last = cumprodDf.iloc[-1]
            # 考虑如果总仓位累加不为1
            _p = 1 - np.sum(weight)  # 初始留存的净值
            rate = _p+np.dot(cumprodDf.iloc[-1], weight)  # 当前净值
            rate /= _p + np.dot(cumprodDf.iloc[-2], weight)  # 上一日净值
            rate -= 1
        return rate

    # 计算symbols组合的收益率
    def genReturnMonthlys(self, dateTime, symbols, frequency, ):
        seriseMonthRate = []
        for symbol in symbols:
            if not hasattr(self, 'symbolRateData'):
                self.symbolRateData = {}

            if symbol not in self.symbolRateData:
                symbolRateData = self.genSymbolRateData(symbol=symbol, frequency=frequency,
                                                        is_real_time=False)
                if symbolRateData.empty:
                    continue
                symbolRateData["lastMarketV"] = symbolRateData["MarketV"].shift()
                symbolRateData['lastMarketV'].fillna(
                    method='ffill', inplace=True)  # ’ffill’，向前填充，或是向下填充
                self.symbolRateData[symbol] = symbolRateData
            df = self.symbolRateData.get(symbol)

            if dateTime not in df.index:
                print(f"{symbol} {dateTime}的数据为空 ")
                continue
            s = df.loc[dateTime]
            seriseMonthRate.append(s)
        monthDf = pd.DataFrame(seriseMonthRate)
        if monthDf.empty:
            return monthDf
        monthDf["市值权重"] = monthDf.lastMarketV / monthDf.lastMarketV.sum()
        monthDf["wRate"] = monthDf.mRate * monthDf["市值权重"]  # 加权收益率
        print(monthDf)
        sumWRate = monthDf.wRate.sum()
        meanRate = monthDf.mRate.mean()
        returnMonthlyDf = pd.DataFrame([[sumWRate, meanRate]], index=[
                                       dateTime], columns=['sumWRate', "meanRate"])
        return returnMonthlyDf

    @Decorator.loadData()
    def get_report(self, df: pd.DataFrame, index_symbol="", **kwargs) -> pd.DataFrame:
        # df 每一列为每日收益率序列
        # index_symbol 基准指数
        # 生成净值图。夏普率等信息
        beg_time = df.iloc[0].name  # 策略开始时间
        end_time = df.iloc[-1].name  # 策略开始时间
        print(f"beg{beg_time} ,end{end_time}")
        if index_symbol:

            idx = self.gen_idx_data(index_symbol=index_symbol)
            idx = idx[(idx.index >= str(beg_time)) & (
                idx.index <= str(end_time))]
            idx = idx.loc[:, [index_symbol]]
            #  df中每个列减去指数日收益
            alpha = df.sub(idx[index_symbol], axis=0)
            # 给每列列名加上后缀 '_alpha'
            alpha = alpha.add_suffix('_alpha')
            # 每日收益率 加指数 加alpha
            df = pd.concat([df, idx, alpha], axis=1, join='outer', )
        tradays = df.shape[0]
        cumprod = (1+df).cumprod()
        # 最新累计净值
        last_net_value = pd.Series(cumprod.iloc[-1], name="last_net_value")
        # 年化收益率
        annual_return = pow(cumprod.iloc[-1], 252/tradays)-1
        annual_return = pd.Series(annual_return*100, name="annual_return(%)")
        # 最大回撤
        maximum_drawdown = 1-cumprod/np.maximum.accumulate(cumprod)
        report = pd.DataFrame(columns=cumprod.columns)
        report.loc["last_net_value"] = last_net_value
        report.loc["annual_return(%)"] = annual_return
        report.loc["maximum_drawdown"] = maximum_drawdown.max()
        std = df.std()
        year_std = std * pow(252, 0.5)
        # 夏普率
        sharp = annual_return/100/year_std
        report.loc["year_std"] = year_std
        report.loc["sharp"] = sharp

        # 生成净值图
        xaxis = [i.strftime("%Y%m%d") for i in cumprod.index.tolist()]
        line = Line().add_xaxis(xaxis)

        for col in cumprod.columns:
            line.add_yaxis(series_name=f"{col}",
                           y_axis=cumprod[col].tolist(),
                           )
            line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        min_val = cumprod.min().min()*0.9
        max_val = cumprod.max().max()*1.1
        line.set_global_opts(yaxis_opts=opts.AxisOpts(
            min_=min_val, max_=max_val))
        line.set_global_opts(
            legend_opts=opts.LegendOpts(pos_top='1%'),
        )
        line.set_series_opts(z=100)  # 线性图在柱形图之上

        bar = Bar().add_xaxis(xaxis)

        # bar.extend_axis(
        #     yaxis=opts.AxisOpts(
        #         name='最大回撤',
        #         type_='value',
        #         position='right'
        #     )
        # )
        # for col in maximum_drawdown.columns:
        #     bar.add_yaxis(series_name=f"{col}_mdd",
        #                   y_axis=maximum_drawdown[col].tolist(),
        #                   yaxis_index=1,
        #                   )
        #     bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
        #                         # itemstyle_opts={"margin_bottom":"30%"}
        #                         )
        # bar.set_global_opts(legend_opts=opts.LegendOpts(pos_top='bottom'))
        # bar.set_global_opts(legend_opts=opts.LegendOpts(pos_left="left"))
        # bar.set_global_opts(
        #     legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=10)),
        #     )
        bar.overlap(line)
        # bar.render()
        # todo grid 方式可以调整图例和表的相对位置防止重叠。但是次坐标轴不显示
        # 用于显示多个线性图
        grid = Grid()
        if index_symbol:
            grid.add(bar, grid_opts=opts.GridOpts(pos_top="20%"))
        else:
            grid.add(line, grid_opts=opts.GridOpts(pos_top="20%"))

        grid.render()
        return report

    def draw_scatter(self, dfs):
        # 散点图x轴要先排序
        # 刻画散点图。df的前两行为xy轴。列名为散点名称
        js_code_str = '''
            function(params){
            return params.data[2];
            }
            '''
        # df = df.T
        # df = df.sort_values(by=df.columns[0])
        # df = df.T
        # print(df)

        # 创建散点图
        scatter = Scatter()
        import matplotlib.pyplot as plt
        import numpy as np

        def generate_colors(n: int):
            cmap = plt.get_cmap("hsv")
            colors = cmap(np.linspace(0, 1, n))
            return colors

        colors = generate_colors(len(dfs))

        # colors = ["blue", "red"]
        for i, df in enumerate(dfs):
            x_data = df.iloc[0].tolist()
            y_data = df.iloc[1].tolist()
            name_data = df.columns.tolist()
            print(x_data)
            print(y_data)
            data = [list(z) for z in zip(y_data, name_data)]
            print(df.name)
            scatter.add_xaxis(x_data)
            scatter.add_yaxis(df.name,
                              data,
                              label_opts=opts.LabelOpts(is_show=False),
                              itemstyle_opts=opts.ItemStyleOpts(
                                  color=colors[i])
                              )

        # 设置全局配置项
        scatter.set_global_opts(
            # title_opts=opts.TitleOpts(title="Scatter Example"),
            xaxis_opts=opts.AxisOpts(
                name=df.iloc[0].name,
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                name=df.iloc[1].name,
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(formatter=JsCode(js_code_str)),
        )
        # 渲染图表
        scatter.render("scatter.html")

    def calc_rtn_by_year(self, df, rule="Y",):
        total = []
        for i, _df in df.resample(rule):
            _s = (1+_df).cumprod()
            if rule == "Y":
                colname = i.year
            else:
                colname = f"{i.year}{i.month:0>2d}"
            s = _s.iloc[-1] - 1  # 每年收益率
            s.name = colname
            total.append(s)
            # total=total.append(pd.DataFrame(s))
        total = pd.DataFrame(total)
        return total

    def calcSharpRatio(self, df):
        # 无风险年化收益率为2%
        # 除非无风险利率波动较大（如在新兴市场中一样），否则超额收益和原始收益的标准差将相似

        r = round(df['return'].mean()/df['return'].std()*np.sqrt(252), 3)
        print("夏普率", r)
        # 减去无风险利率
        df["rtn"] = df["return"] - 0.02/252
        # 由日频率转化为年化夏普
        # https://www.zhihu.com/question/27264526 不同周期选择参考优劣参考
        r = round(df['rtn'].mean()/df['rtn'].std()*np.sqrt(252), 3)
        print("夏普率扣除无风险收益后", r)

    @Decorator.loadData(path="data")
    def qryShiborData(self, **kawgrs):
        if "year" not in kawgrs:
            # 汇总
            total = pd.DataFrame(
                columns=["曲线名称", "日期", "3月", "6月",
                         "1年", "3年", "5年", "7年", "10年", "30年"])
            for year in range(2006, 2023):
                _df = self.qryShiborData(year=year)
                _df['date'] = pd.to_datetime(_df["日期"], format='%Y-%m-%d')
                _df.set_index('date', inplace=True)
                total = total.append(_df)
            return total

        import akshare as ak
        year = kawgrs["year"]
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        bond_china_yield_df = ak.bond_china_yield(
            start_date=start_date, end_date=end_date)
        return bond_china_yield_df

    # def get_minute_data(self, symbol,
    #                     date_time,
    #                     minute=931):
    #     url = "http://192.168.1.100:5000/stock"
    #     params = {}
    #     params["code"] = symbol[:2]+"SE"+symbol[2:]
    #     params["begin"] = date_time
    #     params["end"] = date_time
    #     params["minute"] = minute
    #     rsp = requests.get(url=url, params=params)
    #     data_json = demjson.decode(rsp.text)
    #     print(data_json)

    # @Decorator.firstLoad
    @Decorator.loadData(path="data")
    def get_minutes_data(self, symbol, date_time, **kwargs):
        # 分钟线数据 只保留01到10分的时间戳
        # http://192.168.1.100:5000/stock?code=SHSE.600000&begin=20220104&end=20221231&minute=0931,1400,1430
        # 开高低收
        # 定义交易日起始时间和结束时间
        start_time = pd.Timestamp('09:30:00')
        end_time = pd.Timestamp('15:00:00')
        df = pd.DataFrame(columns=['date_time', "hour_minute", 'open',
                                   'high', 'low', 'close', 'volume'])
        # 定义时间间隔
        interval = pd.Timedelta(minutes=5)

        # 生成时间戳列表
        timestamps = []
        for timestamp in pd.date_range(start=start_time,
                                       end=end_time,
                                       freq=interval):
            timestamps.append(timestamp.time().strftime("%H%M"))

        url = "http://192.168.1.100:5000/stock"
        params = {}
        params["code"] = symbol[:2]+"SE"+symbol[2:]
        params["begin"] = date_time
        params["end"] = date_time
        params["minute"] = ",".join(timestamps)
        rsp = requests.get(url=url, params=params)
        print(demjson.decode(rsp.text))
        data_json = demjson.decode(rsp.text)["info"]
        for date, values in data_json.items():
            for value in values:
                hour_minute = int(value[0])
                open_price = value[1]
                high_price = value[2]
                low_price = value[3]
                close_price = value[4]
                volume = value[5]
                #  只保留日期
                date_time = pd.to_datetime(date, format='%Y-%m-%d').date()
                # hour_minute = pd.to_datetime(hour_minute,
                #                              format='%H%M%S').time()
                df = df.append({'date_time': date_time,
                                'hour_minute': hour_minute,
                                'open': open_price,
                                'high': high_price,
                                'low': low_price,
                                'close': close_price,
                                'volume': volume}, ignore_index=True)
        df.set_index('date_time', inplace=True)
        return df


if __name__ == '__main__':
    m = Mgr()
    m.genSymbolRateData(symbol="SH.600057", is_real_time=True)
