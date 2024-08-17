from .exchange import Exchange
from quantguard.model.balance import Balance
from quantguard.model.position import Position
from quantguard.model.order import Order, DimensionEnum
from quantguard.model.ledger import Ledger, LedgerType
import time
import logging
from ccxt import gate

logger = logging.getLogger(__name__)


# TODO 只实现了合约的定义，spot和合约应该单独提供类
class GATE(Exchange):
    def __init__(self, account_name: str, config: dict):
        super().__init__("gate", account_name, config)
        self.exchange: gate = self.exchange

    def fetch_balance(self) -> Balance:
        ccxt_balance = super().fetch_balance(({"type": "swap"}))
        # print(f"account {self.account_name} balance: {ccxt_balance}")

        balance = Balance(
            name=self.account_name,
            exchange=self.exchange_id,
            asset="USDT",
            total=ccxt_balance["USDT"]["total"],
            available=ccxt_balance["USDT"]["free"],
            frozen=ccxt_balance["USDT"]["used"],
            borrowed=0,  # TODO
            ts=ccxt_balance["info"][0]["update_time"],
            unrealized_pnl=ccxt_balance["info"][0]["unrealised_pnl"],
            created_at=int(time.time() * 1000),
        )
        return balance

    def fetch_positions(self) -> list[Position]:
        ccxt_position = super().fetch_positions()
        # print(f"account {self.account_name} position: {ccxt_position}")
        positions = []
        for pos in ccxt_position:
            # "DOGE/USDT:USDT"
            base_asset = pos["symbol"].split("/")[0]
            quote_asset = pos["symbol"].split("/")[1].split(":")[0]
            position = Position(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type="UFUTURES",
                base_asset=base_asset,
                quote_asset=quote_asset,
                ts=pos["timestamp"] if pos["timestamp"] else 0,
                # dimension=pos["side"] if pos["side"] else "",
                dimension=DimensionEnum.QUANTITY.value,
                quantity=float(pos["info"]["size"]) * float(pos["contractSize"]),
                average_price=pos["entryPrice"],
                unrealized_pnl=pos["unrealizedPnl"],
                liquidation_price=pos["liquidationPrice"],
                contract_size=pos["contractSize"],
                created_at=int(time.time() * 1000),
            )
            positions.append(position)
        return positions

    def fetch_orders_T(self, fetch_orders_T=1):
        since = super().get_yesterday_timestamps(fetch_orders_T)
        open_orders = self.loop_fetch_open_orders(since=since)
        closed_orders = self.loop_fetch_closed_orders(since=since)
        all_orders = open_orders + closed_orders
        my_trades = self.loop_fetch_my_trades(since=since)
        map_my_trades = {}
        for trade in my_trades:
            map_my_trades[trade["info"]["order_id"]] = trade
        orders = []
        for order in all_orders:
            # 'symbol': 'DOGE/USDT:USDT'
            base_asset = order["symbol"].split("/")[0]
            quote_asset = order["symbol"].split("/")[1].split(":")[0]

            market_type = "UFUTURES"
            contract_size = self.fetch_symbol_contract_size(order["symbol"])

            # 自定义id去除t-开头 t-1629782400000
            cId = order["clientOrderId"]
            if cId.startswith("t-"):
                cId = cId[2:]
            my_trade = map_my_trades.get(order["id"])
            if my_trade is None:
                result = self.exchange.privateFuturesGetSettleMyTrades(
                    {"settle": "usdt", "type": "swap", "order": order["id"]}
                )
                if result:
                    my_trade = result[0]
            item = Order(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type=market_type,
                base_asset=base_asset,
                quote_asset=quote_asset,
                market_order_id=order["id"],
                custom_order_id=cId,
                ts=order["timestamp"],
                origin_price=order["price"],
                origin_quantity=float(order["amount"]) * contract_size,  # 委托数量 > 0
                total_average_price=(
                    order["average"] if order["average"] else 0
                ),  # 总成交均价
                total_filled_quantity=float(order["filled"])
                * contract_size,  # 成交数量 > 0
                last_average_price=order["info"]["fill_price"],  # 最新成交价格
                last_filled_quantity=float(order["info"]["size"])
                * contract_size,  # 最新成交数量, sell为-1
                order_side=order["side"],
                order_time_in_force=order["timeInForce"],
                reduce_only=order["info"]["is_reduce_only"],
                order_type=order["type"],
                order_state=order["status"],
                dimension=DimensionEnum.QUANTITY.value,
                trade_list=order["trades"],
                commission=my_trade["info"]["fee"] if my_trade else 0,
                contract_size=contract_size,
                created_at=int(time.time() * 1000),
            )
            orders.append(item)
        return orders

    def loop_fetch_open_orders(self, since=None, offset=0):
        open_orders = self.exchange.fetch_open_orders(
            since=since, params={"type": "swap"}
        )
        if len(open_orders) == 0:
            return open_orders
        last_time = open_orders[-1]["timestamp"]
        print(
            f"length: {len(open_orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
        )
        if last_time < since:
            return open_orders
        offset += len(open_orders)
        return open_orders + self.loop_fetch_open_orders(since, offset)

    def loop_fetch_closed_orders(self, since=None, offset=0):
        closed_orders = self.exchange.fetch_closed_orders(
            since=since, params={"type": "swap", "offset": offset}
        )

        if len(closed_orders) == 0:
            return closed_orders
        last_time = closed_orders[-1]["timestamp"]
        logger.info(
            f"length: {len(closed_orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
        )
        if last_time < since:
            return closed_orders
        offset += len(closed_orders)
        return closed_orders + self.loop_fetch_closed_orders(since, offset)

    def loop_fetch_my_trades(self, since=None, offset=0):
        my_trades = self.exchange.fetch_my_trades(
            since=since, params={"type": "swap", "offset": offset}
        )

        if len(my_trades) == 0:
            return my_trades
        last_time = my_trades[-1]["timestamp"]
        logger.info(
            f"length: {len(my_trades)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
        )
        if last_time < since:
            return my_trades
        offset += len(my_trades)
        return my_trades + self.loop_fetch_my_trades(since, offset)

    def fetch_ledgers_T(self, fetch_orders_T=1, since=None, offset=0):
        # 只能获取到最近30天的数据
        if since is None:
            since = int(super().get_yesterday_timestamps(fetch_orders_T))
        ccxt_ledgers = self.exchange.fetch_ledger(
            params={"type": "swap", "offset": offset}
        )
        ledgers = []
        for ledger in ccxt_ledgers:
            item = self.count_ledger_fee(ledger)
            if not item:
                continue
            ledgers.append(item)

        if len(ccxt_ledgers) == 0:
            return ledgers

        last_time = ccxt_ledgers[-1]["timestamp"]
        logger.info(
            f"length: {len(ccxt_ledgers)}, fee length: {len(ledgers)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
        )
        if last_time < since:
            return ledgers

        offset += len(ccxt_ledgers)
        return ledgers + self.fetch_ledgers_T(
            fetch_orders_T, since=since, offset=offset
        )

    def count_ledger_fee(self, ledger) -> Ledger:
        # 交易手续费
        if ledger["type"] == "fee" and ledger["info"]["type"] == "fund":
            item = Ledger(
                name=self.account_name,
                exchange=self.exchange_id,
                asset=ledger["info"]["contract"].split("_")[1],
                symbol=ledger["info"]["contract"].replace("_", "-"),
                ts=ledger["timestamp"],
                market_type="UFUTURES",
                market_id="%s_%s" % (ledger["timestamp"], ledger["info"]["balance"]),
                ledger_type=LedgerType.FUNDING_FEE.value,
                amount=float(ledger["info"]["change"]),
                created_at=int(time.time() * 1000),
            )
            return item

        # ledger_type = ledger["type"]
        # if ledger["type"] == "fee":
        #     ledger_type = LedgerType.FUNDING_FEE.value
        # else:
        #     continue
        # print(f"ledger: {ledger}")

        # # {'id': '83503268060', 'direction': 'in', 'account': None, 'referenceAccount': None, 'referenceId': None, 'type': 'c2c_om', 'currency': 'USDT', 'amount': 20.0, 'timestamp': 1722737188820, 'datetime': '2024-08-04T02:06:28.820Z', 'before': 0.0, 'after': 20.0, 'status': None, 'fee': None, 'info': {'id': '83503268060', 'time': '1722737188820', 'currency': 'USDT', 'change': '20', 'balance': '20', 'type': 'c2c_om', 'text': '26021689'}}
        # item = Ledger(
        #     name=self.account_name,
        #     exchange=self.exchange_id,
        #     asset=ledger["currency"],
        #     symbol="",  # TODO 没有交易对
        #     ts=ledger["timestamp"],
        #     update_ts=int(time.time() * 1000),
        #     market_type="UFUTURES",
        #     market_id=ledger["id"],
        #     ledger_type=ledger_type,
        #     amount=ledger["amount"],
        #     created_at=int(time.time() * 1000),
        # )
        return None
