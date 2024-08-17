from .exchange import Exchange
from quantguard.model.balance import Balance
from quantguard.model.position import Position
from quantguard.model.order import Order, DimensionEnum
from quantguard.model.ledger import Ledger, LedgerType
from ccxt import okx
import time


class OKX(Exchange):
    def __init__(self, account_name: str, config: dict):
        super().__init__("okx", account_name, config)
        self.exchange: okx = self.exchange

    def fetch_balance(self) -> Balance:
        ccxt_balance = super().fetch_balance()
        # print(f"account {self.account_name} balance: {ccxt_balance}")
        balance = Balance(
            name=self.account_name,
            exchange=self.exchange_id,
            asset="USDT",
            total=ccxt_balance["USDT"]["total"],
            available=ccxt_balance["USDT"]["free"],
            frozen=ccxt_balance["USDT"]["used"],
            borrowed=ccxt_balance["info"]["data"][0]["borrowFroz"],
            ts=ccxt_balance["timestamp"],
            unrealized_pnl=ccxt_balance["info"]["data"][0]["details"][0]["upl"],
            created_at=int(time.time() * 1000),
        )
        return balance

    def fetch_positions(self) -> list[Position]:
        ccxt_position = super().fetch_positions()
        positions = []
        for pos in ccxt_position:
            # 'symbol': 'DOGE/USDT:USDT'
            base_asset = pos["symbol"].split("/")[0]
            quote_asset = pos["symbol"].split("/")[1].split(":")[0]
            if pos["info"]["instType"] == "SWAP":
                market_type = "UFUTURES"
            else:
                market_type = "SPOT"
            position = Position(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type=market_type,
                base_asset=base_asset,
                quote_asset=quote_asset,
                ts=pos["info"]["cTime"],
                # dimension=pos["side"],
                dimension=DimensionEnum.QUANTITY.value,
                quantity=float(pos["info"]["pos"]) * pos["contractSize"],
                average_price=pos["info"]["avgPx"],
                unrealized_pnl=pos["unrealizedPnl"],
                liquidation_price=(
                    pos["liquidationPrice"] if pos["liquidationPrice"] else ""
                ),
                contract_size=pos["contractSize"],
                created_at=int(time.time() * 1000),
            )
            positions.append(position)
        return positions

    def fetch_orders_T(self, fetch_orders_T=1):
        since = super().get_yesterday_timestamps(fetch_orders_T)
        open_orders = self.loop_fetch_open_orders(orignal_since=since, since=since)
        closed_orders = self.loop_fetch_closed_orders(orignal_since=since, since=since)
        all_orders = open_orders + closed_orders
        orders = []
        # 一个订单可能对应多个trade, 订单1715876098503593985
        for order in all_orders:
            base_asset = order["symbol"].split("/")[0]
            quote_asset = order["symbol"].split("/")[1].split(":")[0]
            if order["info"]["instType"] == "SWAP":
                market_type = "UFUTURES"
            else:
                market_type = "SPOT"

            contract_size = self.fetch_symbol_contract_size(order["symbol"])
            item = Order(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type=market_type,
                base_asset=base_asset,
                quote_asset=quote_asset,
                market_order_id=order["id"],
                custom_order_id=(
                    order["clientOrderId"] if order["clientOrderId"] is not None else ""
                ),
                ts=order["timestamp"],
                # update_ts=order["lastUpdateTimestamp"],
                origin_price=order["price"],
                origin_quantity=float(order["amount"])
                * contract_size,  # 委托数量, 合约为张数
                total_average_price=order["average"],
                total_filled_quantity=float(order["filled"])
                * contract_size,  # 成交数量，合约为张数
                last_average_price=order["info"]["fillPx"],  # 最新成交价格
                last_filled_quantity=float(order["info"]["fillSz"])
                * contract_size,  # 最新成交数量，合约为张数
                order_side=order["side"],
                order_time_in_force=(
                    order["timeInForce"] if order["timeInForce"] else ""
                ),
                reduce_only=True if order["reduceOnly"] else False,
                order_type=order["info"]["ordType"],
                # leverage=order["info"]["lever"],
                order_state=order["status"],
                dimension=DimensionEnum.QUANTITY.value,
                trade_list=order["trades"],
                commission=order["fee"]["cost"],
                contract_size=contract_size,
                created_at=int(time.time() * 1000),
            )
            orders.append(item)
        return orders

    def loop_fetch_open_orders(self, orignal_since=None, since=None):
        open_orders = self.exchange.fetch_open_orders(
            since=since, params={"instType": "SWAP"}
        )
        if len(open_orders) == 0:
            return open_orders

        last_time = open_orders[-1]["timestamp"]
        if last_time < orignal_since:
            return open_orders
        return open_orders + self.loop_fetch_open_orders(orignal_since, last_time)

    def loop_fetch_closed_orders(self, orignal_since=None, since=None):
        closed_orders = self.exchange.fetch_closed_orders(
            since=since, params={"instType": "SWAP"}
        )

        if len(closed_orders) == 0:
            return closed_orders

        last_time = closed_orders[-1]["timestamp"]
        if last_time < orignal_since:
            return closed_orders

        return closed_orders + self.loop_fetch_closed_orders(orignal_since, last_time)

    def fetch_ledgers_T(
        self, fetch_orders_T=1, orignal_since=None, since=None, id=None
    ):
        if since is None:
            since = super().get_yesterday_timestamps(fetch_orders_T)
        print(
            f"since yyyy-mm-dd: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
        )
        params = {"instType": "SWAP"}
        # , "method": "privateGetAccountBillsArchive" 请求3个月数据
        # 先通过时间获取到最后一条数据的id, 后续再通过id获取数据
        if id:
            params["before"] = id
        else:
            params["end"] = since
        # print(f"params: {params}")
        ccxt_ledgers = self.exchange.fetch_ledger(params=params)
        ledgers = []
        for ledger in ccxt_ledgers:
            ledger_type = ledger["info"]["type"]
            if ledger["info"]["type"] == "8":
                ledger_type = LedgerType.FUNDING_FEE.value
            else:
                continue

            symbol = ledger["symbol"] if ledger["symbol"] else ""
            # DOGE/USDT:USDT -> DOGE-USDT
            if symbol:
                symbol = symbol.replace("/", "-").split(":")[0]
            item = Ledger(
                name=self.account_name,
                exchange=self.exchange_id,
                asset=ledger["currency"],
                symbol=symbol,
                ts=ledger["timestamp"],
                market_type="UFUTURES",
                market_id=ledger["id"],
                ledger_type=ledger_type,
                amount=ledger["amount"],
                created_at=int(time.time() * 1000),
            )
            ledgers.append(item)
        # print(f"length: {len(ccxt_ledgers)}, fee length: {len(ledgers)}")
        # since 和 当前时间相差小于1天
        # print(f"since: {since}, last timestamp: {ccxt_ledgers[-1]['timestamp']}")
        if len(ccxt_ledgers) == 0:
            return ledgers
        last_time = ccxt_ledgers[-1]["timestamp"]
        if last_time < orignal_since:
            return last_time

        time.sleep(0.4)  # 当前接口 5次/2s
        return ledgers + self.fetch_ledgers_T(
            fetch_orders_T, orignal_since, last_time, ccxt_ledgers[-1]["id"]
        )
