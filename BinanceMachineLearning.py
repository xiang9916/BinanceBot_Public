from BinanceClient import Client
from BinanceIndicators import VWAP
from BinanceTools import candles_decimal, proxy

import numpy as np
import threading
import time
import torch
from decimal import *
from math import floor

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_EVEN
proxy()
Client = Client()


def set_device():
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
    return device


class LstmModel(torch.nn.Module): # 继承自 torch.nn.Module
    def __init__(self, input_dims, input_seq_length, output_dims, output_seq_length, h_dims, lstm_num_layers) -> None:
        super().__init__()
        self.input_dims = input_dims
        self.input_seq_length = input_seq_length
        self.output_dims = output_dims
        self.output_seq_length = output_seq_length
        self.h_dims = h_dims
        self.lstm_num_layers = lstm_num_layers

        self.hidden_cell = (
            torch.zeros(self.lstm_num_layers, self.h_dims).to(device),
            torch.zeros(self.lstm_num_layers, self.h_dims).to(device)
        )

        # 神经网络包括5个层
        self.lstm1 = torch.nn.LSTM(
            input_size = self.input_dims,
            hidden_size = self.h_dims,
            num_layers = self.lstm_num_layers
        )
        self.linear1 = torch.nn.Linear(
            in_features = self.input_seq_length,
            out_features = self.output_seq_length
        )
        self.linear2 = torch.nn.Linear(
            in_features = self.h_dims,
            out_features = self.h_dims
        )
        self.relu = torch.nn.ReLU()
        self.linear3 = torch.nn.Linear(
            in_features = self.h_dims,
            out_features = self.output_dims
        )

    def forward(self, x):
        y1, self.hidden_cell = self.lstm1(x, self.hidden_cell)
        # y2 = torch.t(self.linear1(torch.t(y1.view(self.input_dims, self.h_dims))))
        y2 = y1[-self.output_seq_length:, :]
        y3 = self.linear2(y2)
        y4 = self.relu(y3)
        y5 = self.linear3(y4)
        return y5

    def init_hidden_cell(self):
        self.hidden_cell = (
            torch.zeros(self.lstm_num_layers, self.h_dims).to(device),
            torch.zeros(self.lstm_num_layers, self.h_dims).to(device)
        )


def source():
    source = []
    # 将收盘价时间序列数据添加进 source
    for asset in assets:
        k_lines = Client.getKlines(symbol = asset+'USDT', interval = '1d', limit = 371)
        closes = []
        for candle in k_lines:
            closes.append(float(candle[4]))
        closes = np.array(closes)
        print(closes.size)
        source.append(closes)
    source = np.array(source).T
    return source



def train(data):
    def sourcer(data):

    return


def test():
    return


def predict():
    return


if __name__ == "__main__":
    assets = ['BTC', 'ETH', 'BNB']
    device = set_device()
    data = source()
    
    model = LstmModel(
        input_dims = 3,
        input_seq_length = 360,
        output_dims = 3,
        output_seq_length = 5,
        h_dims = 16,
        lstm_num_layers = 1
    )
    