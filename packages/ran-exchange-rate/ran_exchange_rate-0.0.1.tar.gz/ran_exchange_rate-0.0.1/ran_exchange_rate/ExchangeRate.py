# -*- coding: utf-8 -*-
"""
*------------------------------
｜@Project   : phonebus_crm_backend
｜@ Author   : ran <|-<
｜@ Time     : 2024/8/13 1:23
｜@ File     : excharge_rate_test.py
｜@ Software : PyCharm
*------------------------------
"""
import asyncio
import logging
import traceback

import aiohttp
from decimal import Decimal
from http import HTTPStatus
from typing import Dict, List

__alphavantage_api_key: str = "MVJZFQONDELOAVOU"
__exchangerate_api_key: str = "02bd6077c183ac96b5f88e20"


class ExchangeRateOpt:
    """
    This exchangerate operation supports the latest exchangerate acquisition from both api providers
    (exchangerate-api: https://www.exchangerate-api.com, alphavantage: https://www.alphavantage.co),
    the specific API limit please refer to the API providers help documentation.

    The preferred pattern is 2, which means that we will request https://www.exchangerate-api.com to
    get the latest exchangerate.

    Remember, please go to the official website to apply for the supplier to open api_key before the
    follow-up process!!
    """
    def __init__(self, __alphavantage_api_key: str = None, exchangerate_api_key: str = None):
        self.__alphavantage_api_key = __alphavantage_api_key
        self.__alphavantage_base_url = "https://www.alphavantage.co/query"
        self.__exchangerate_api_key = exchangerate_api_key
        self.__exchangerate_base_url = "https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"
        self.__model = 2

    async def _model_1_currency_rate_base_usd(
            self,
            from_currency: str,
            to_currency: str = "USD"
    ) -> Dict[str, Decimal]:
        """
        :param from_currency: currency which want to trans.
        :param to_currency: currency which trans to.
        :return: dict, {currency_str: currency_rate_decimal}
        """
        try:
            params: dict = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_currency,
                "to_currency": to_currency,
                "apikey": self.__alphavantage_api_key
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url=self.__alphavantage_base_url, params=params) as response:
                    if response.status != HTTPStatus.OK:
                        raise Exception(str(await response.text()))
                    currency_rate = await response.json()
                    rate_decimal: dict = currency_rate.get("Realtime Currency Exchange Rate", None)
                    if not rate_decimal:
                        raise Exception(str(await response.text()))
                    rate_decimal: Decimal = rate_decimal["5. Exchange Rate"]
                    return {from_currency: rate_decimal}
        except aiohttp.ClientError as e:
            raise Exception(str(e))
        except Exception:
            err_info = traceback.format_exc()
            logging.error(err_info)
            raise Exception(err_info)

    async def _model_2_currency_rate_base_usd(
            self,
            from_currency: str,
            to_currency: str = "USD"
    ) -> Dict[str, Decimal]:
        """
        base currency is USD
        :param from_currency: currency which trans.
        :return: dict, {currency_str: currency_rate_decimal}
        """
        try:
            request_url = self.__exchangerate_base_url.format(
                api_key=self.__exchangerate_api_key,
                currency=from_currency
            )
            async with aiohttp.ClientSession() as session:
                async with session.get(url=request_url) as response:
                    if response.status != HTTPStatus.OK:
                        raise Exception(str(await response.text()))
                    currency_rate = await response.json()
                    if currency_rate.get("result") != "success":
                        raise Exception(str(await response.text()))
                    rate_decimal: Decimal = currency_rate["conversion_rates"].get(to_currency)
                    return {from_currency: rate_decimal}
        except aiohttp.ClientError as e:
            raise Exception(str(e))
        except Exception:
            err_info = traceback.format_exc()
            logging.error(err_info)
            raise Exception(err_info)

    async def get_currency_rate_base_usd(
            self,
            from_currency_list: list,
            to_currency: str = "USD"
    ) -> Dict[str, Decimal]:
        """
        :param from_currency_list: currency list which you want to trans.
        :param to_currency: currency which trans to.
        return currency_map: {currency_str: currency_decimal}
        """
        result_map: dict = {}
        try:
            task_list: list = [self._model_2_currency_rate_base_usd(currency) for currency in from_currency_list]
            currency_list: List[dict] = list(await asyncio.gather(*task_list))
            result_map: dict = {k: v for x in currency_list for k, v in x.items()}
        except Exception as e:
            logging.error(f"Model 2 Error: {e} \n, Model Change TO 1, Retry...")
            try:
                task_list = [self._model_1_currency_rate_base_usd(currency) for currency in from_currency_list]
                currency_list: List[dict] = list(await asyncio.gather(*task_list))
                result_map: dict = {k: v for x in currency_list for k, v in x.items()}
            except Exception as e:
                logging.error(f"Model 1 Error: {e} \n.")
        return result_map
