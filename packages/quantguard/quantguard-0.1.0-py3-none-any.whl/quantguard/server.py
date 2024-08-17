"""server"""

import asyncio

from quantguard.config.account import init_account
from quantguard.log.log import init_log
from quantguard.worker.bill_worker import BillWorker
from quantguard.config.account import accounts

import logging

logger = logging.getLogger(__name__)


class Server:

    def __init__(self):
        init_log()
        init_account()

    def run_bill_worker(self):
        loop = asyncio.new_event_loop()

        for account in accounts:
            loop.create_task(BillWorker(account=account).run())
            print(f"create task {account.name}")

        # SyncBillWork(loop=loop, config=config).run()
        loop.run_forever()
