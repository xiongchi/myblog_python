# coding=utf-8
from matplotlib import pylab, ticker
from pylab import *
import matplotlib.finance as mpf
import matplotlib.ticker as tk

from config import Config
from web.stock.k.select_stock_data import SelectStockData


class KPhoto(object):
    def __init__(self, secucode, days):
        ssd = SelectStockData()
        self.days = days
        self.secucode = secucode
        self.k_day_data = ssd.sel_k_by_code(secucode, days)
        self.secuname = ssd.sel_secuname(secucode)
        self.timeData = self.k_day_data[:, 0]
        self.flag_data = [i for i in range(len(self.timeData))]
        self.bg_color = 'black'
        self.title_color = 'gold'
        self.gird_color = 'red'
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 设置绘图尺寸
        pylab.rcParams['figure.figsize'] = (8, 5)
        plt.figure(facecolor=(0, 0, 0))

    # 画图
    def k_photo(self):
        path = Config.get_conf().get('photo', 'path')
        data_list = np.array(self.k_day_data[:, [2, 3, 5, 4, 6]], dtype=float)
        data_list = np.c_[self.flag_data, data_list]
        self.draw_k(data_list, self.flag_data)
        self.drawCount(data_list, self.flag_data)
        self.save(path + str(self.secucode) + '_' + str(self.days) + '.png')

    # 均线
    def avg_k(self, ax):
        ma_5 = self.k_day_data[:, 9]
        ma_10 = self.k_day_data[:, 10]
        ma_20 = self.k_day_data[:, 11]
        flag_data = [i for i in range(len(self.timeData))]
        ax.plot(flag_data, ma_5, color='yellow', label='m5')
        ax.annotate(s='m5', xy=(self.flag_data[-2], ma_5[-2]), xytext=(+10, -10), color='white', textcoords='offset points', arrowprops=dict(arrowstyle='-'))
        ax.plot(flag_data, ma_10, color='purple', label='m10')
        ax.plot(flag_data, ma_20, color='green', label='m20')

    # 画K线
    def draw_k(self, data_list, flag_data):
        left, width = 0, 1.0
        bottom, heght = 0.05, 0.2
        r1 = [left, bottom + heght + 0.05, width, 0.65]
        k_ax = plt.axes(r1)
        plt.title(self.secucode + "                      " + self.secuname, color=self.title_color)
        distance = flag_data[-1] / 50 * 0.26 if flag_data[-1] / 50 * 0.26 >= 0.26 else 0.26
        mpf.candlestick_ohlc(k_ax, data_list, width=0.8, colorup='r', colordown='g')
        k_ax.set_xlim(flag_data[0] - distance, flag_data[-1] + distance)
        k_ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date))
        k_ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.k_format_date))
        self.avg_k(k_ax)
        self._back_ground(k_ax)

    # 画成交量
    def drawCount(self, data_list, flag_data):
        left, width = 0, 1.0
        bottom, heght = 0.05, 0.2
        r1 = [left, bottom, width, heght]
        count_ax = plt.axes(r1)
        subPrice = [open - close for d, open, high, low, close, volume in data_list]
        _colors = []
        # 上涨为red  下跌为green
        for i in subPrice:
            if i <= 0.0:
                _colors.append('red')
            else:
                _colors.append('green')
        volumes = [volume for d, open, high, low, close, volume in data_list]
        # 图的头和尾的蜡烛图处理
        distance = flag_data[-1] / 50 * 0.3 if flag_data[-1] / 50 * 0.3 >= 0.3 else 0.3
        count_ax.set_xlim(flag_data[0] - distance, flag_data[-1] + distance)
        count_ax.yaxis.set_major_locator(tk.MultipleLocator(np.max(volumes) / 3))
        count_ax.bar(range(len(flag_data)), volumes, width=0.8, color=_colors)
        count_ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.y_format_count))
        self._back_ground(count_ax)
        self.del_axix(count_ax)

    # k线 y轴图显示格式
    def k_format_date(self, x, pos=None):
        return '{:.2f}'.format(x)

    # 成交量显示格式
    def format_date(self, x, pos=None):
        if x < 0 or x > len(self.timeData) - 1:
            return ''
        else:
            return self.timeData[int(x)]
        # 成交量x轴显示格式

    # 背景
    def _back_ground(self, ax):
        plt.rcParams['savefig.facecolor'] = 'black'
        ax.set_facecolor('black')
        ax.spines['right'].set_color('#FF3232')
        ax.spines['right'].set_linewidth(0.3)
        ax.spines['left'].set_color('r')
        ax.spines['left'].set_linewidth(0.3)
        ax.spines['top'].set_color('r')
        ax.spines['top'].set_linewidth(0.3)
        ax.spines['bottom'].set_color('r')
        ax.spines['bottom'].set_linewidth(0.3)
        ax.tick_params(axis='x', bottom=False, left=False, colors='w', width=0.3)
        ax.tick_params(axis='y', bottom=False, left=False, colors='#FF3232', width=0.3)

    # y轴线
    def y_format_count(self, y, pos=None):
        if y == 0:
            return 0
        else:
            y_str = str(y)
            count_num = int(y_str.split('.')[0])
            if count_num >= 100000:
                return '{:.2f}'.format(count_num / 10000.0) + '万'
            else:
                return count_num

    # 隐藏刻度线
    def del_axix(self, x_axis):
        x_axis.set_xticks([])

    def save(self, k_path=''):
        plt.savefig(k_path, dpi=100, format='png', bbox_inches='tight')
        plt.close()

