import pandas as pd
import datetime
import toml

from xtquant import xtdatacenter as xtdc, xtdata
from xtquant.xtdata import get_local_data, download_history_data, get_market_data_ex

from mason_tools import RpcServer


def init_xt(xt_token: str):
    xtdc.set_token(xt_token)
    xtdc.init()


def api(func_name, *args, **kwargs):
    return getattr(xtdata, func_name)(*args, **kwargs)


def get_history_data(stock_code, period, start_time="", end_time=""):
    download_history_data(
        stock_code, period, start_time=start_time, end_time=end_time, incrementally=None
    )
    data: dict = get_local_data(
        [], [stock_code], period, start_time, end_time, -1, "front_ratio", False
    )  # 默认等比前复权

    df: pd.DataFrame = data[stock_code]
    df["time"] = df["time"].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))
    df["stock_code"] = stock_code
    return df


def history_main_symbols(stock00_code: str, start_time: str = "", end_time: str = ""):
    """stock_code 为连续合约"""
    download_history_data(stock00_code, "historymaincontract", start_time, end_time)
    # 获取历史主力合约
    his_data = get_market_data_ex(
        [],
        [stock00_code],
        period="historymaincontract",
        start_time=start_time,
        end_time=end_time,
        count=-1,
        dividend_type="none",
        fill_data=False,
    )
    df: pd.DataFrame = his_data[stock00_code]
    if df.empty:
        return df
    df["time"] = df["time"].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))
    df["stock_code"] = df["合约在交易所的代码"] + "." + stock00_code.split(".")[-1]
    df = df[["time", "stock_code"]]
    return df


def test_xt(
    xt_token,
    start_date="20230110",
    end_date="20240112",
    period="1d",
    symbol="rb2405.SF",
):
    init_xt(xt_token)
    print(get_history_data(symbol, period, start_date, end_date))
    print(history_main_symbols("rb00.SF", start_date, end_date))


def XtDataServer(xt_token, rep_address, pub_address):
    init_xt(xt_token)
    xt_server = RpcServer()
    xt_server.start(rep_address, pub_address)
    xt_server.register(api)
    xt_server.register(get_history_data)
    xt_server.register(history_main_symbols)
    return xt_server


if __name__ == "__main__":
    xt_token = toml.load("secret.toml")["xt"]["xt_token"]
    rep_address = "tcp://*:2014"
    pub_address = "tcp://*:4102"
    s = XtDataServer(xt_token, rep_address, pub_address)
    # d = test_xt(xt_token)
