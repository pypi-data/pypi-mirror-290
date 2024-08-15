from email import header
import hmac
import base64
import hashlib
import json
import time
import urllib.parse
import requests
from urllib.parse import urlencode
from ttxt.utils import general
from ttxt.base import baseSpotExchange
from ttxt.types import baseTypes
import uuid

class blofin(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, password, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.password = password
        self.domain_url = "https://api.blofin.com"
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "-")
    
    def _getUserSymbol(self, symbol):
        return symbol.replace("-", "/")
    
    def get_uuid(self):
        return str(uuid.uuid4())
    
    def get_timstamp(self):
        return str(int(time.time()*1000))

    ## Auth 
    def parse_params_to_str(self, params):
        params = [(key, val) for key, val in params.items()]
        params.sort(key=lambda x:x[0])
        url = "?" + urlencode(params)
        if url == '?':
            return ''
        return url

    def create_signature_blofin(self, nonce, method, timestamp, path, body=None):
        # If it is a GET request, the body must be "".
        if body:
            prehash_string = f"{timestamp}{method}{path}{body or ''}{nonce}"
        else:
            prehash_string = f"{path}{method}{timestamp}{nonce}"
        encoded_string = prehash_string.encode()
        signature = hmac.new(self.secret.encode(), encoded_string, hashlib.sha256)
        #The implementation here differs slightly from the signature used by other exchanges. It needs to be converted to a hexadecimal string and then converted to bytes. Please note that it is not hex2bytes, but rather string2bytes.
        hexdigest = signature.hexdigest() #Convert the signature result into a hexadecimal string.
        hexdigest_to_bytes = hexdigest.encode() #Convert this string into bytes.
        base64_encoded = base64.b64encode(hexdigest_to_bytes).decode() #Base64 encoding
        return base64_encoded

    def _signedRequest(self, method, request_path, queryString, body=None):
        ts = self.get_timstamp()
        nonce = self.get_uuid()
        if queryString and queryString != '':
            request_path += self.parse_params_to_str(queryString)
        headers = {
            "ACCESS-KEY": self.key,
            "ACCESS-SIGN": self.create_signature_blofin(nonce, method, ts, request_path, body),
            "ACCESS-TIMESTAMP": ts,
            "ACCESS-NONCE": nonce,
            "ACCESS-PASSPHRASE": self.password
        }
        url = self.domain_url + request_path
        if method == "POST":
            try:
                response = requests.post(url, headers=headers, json=body)
                return response.json()
            except Exception as e:
                raise e
        if method == "GET":
            try:
                response = requests.get(url, headers=headers)
                return response.json()
            except Exception as e:
                raise e
    
    def _unsignedRequest(self, method, apiUrl, params):
        url = self.domain_url + apiUrl
        if method == 'GET':
            try:
                response = requests.request('get', url, params=params)
                return response.json()
            except Exception as e:
                raise e
        else:
            raise Exception(f"{method} Method not supported for unsigned calls")
    
    ## parsers
    def _parseBalance(self, balData):
        parsedBal = {"free": {}, "total": {}}
        if balData["code"] != '0':
            raise Exception(balData['msg'])
        data = balData.get("data", [])
        for d in data:
            parsedBal["free"][d["currency"]] = d["available"]
            parsedBal["total"][d["currency"]] = d["balance"]
        return parsedBal
    
    def _parseCreateorder(self, order):
        if order["code"] != '0':
            raise Exception(order['msg'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        if "data" in order and order["data"] != {}:
            parsedOrder['id'] = order['data'][0]['orderId']
            parsedOrder["orderJson"] = json.dumps(order)
        return parsedOrder
    
    def _parseOpenOrders(self, orders):
        if orders["code"] != '0':
            raise Exception(orders['msg'])
        parsedOrderList = []    
        if "data" in orders and orders['data'] != {}:
            for orderJson in orders["data"]:
                currentOrder = {} 
                currentOrder["id"] = orderJson["orderId"]
                currentOrder["symbol"] = self._getUserSymbol(orderJson["instId"])
                currentOrder["price"] = float(orderJson["price"])
                currentOrder["amount"] = float(orderJson["size"])
                currentOrder["side"] = orderJson["side"]
                currentOrder["timestamp"] = orderJson["createTime"]
                currentOrder["status"] = orderJson["state"]
                currentOrder["orderJson"] = json.dumps(orderJson)
                parsedOrderList.append(currentOrder)
        return parsedOrderList
    
    def _parseFetchOrder(self, data):
        parsedOrder = {"id": None, "symbol": None, "price": None, "amount": None, "takerOrMaker": None, "datetime": None, "fee": None, "fee_currency": None,
                       "side": None, "timestamp": None, "status": None}
        if data != {}:
            order = data
            parsedOrder["id"] = order["orderId"]
            parsedOrder["tradeId"] = order["tradeId"]
            parsedOrder["symbol"] = self._getUserSymbol(order["instId"])
            parsedOrder["price"] = float(order["fillPrice"])
            parsedOrder['takerOrMaker'] = "maker"  # this info is not given in the api response
            parsedOrder["amount"] = float(order["fillSize"])
            parsedOrder["side"] = order["side"]
            parsedOrder["timestamp"] = int(order["ts"])  # ms epoch
            parsedOrder["datetime"] = general.ts_to_datetime(parsedOrder["timestamp"])
            parsedOrder["status"] = "closed"
            parsedOrder['fee'] = order.get("fee", None)
            parsedOrder["fee_currency"] = "quoteCurrency"  # not possible to split pair to get correct quote currency 
        return parsedOrder
    
    def _parseFetchTrades(self, orders):
        if orders["code"] != '0':
            raise Exception(orders['msg'])
        parsedTradesList = []
        for orderJson in orders["data"]:
            parsedTradesList.append(self._parseFetchOrder({'data': orderJson}))
        return parsedTradesList
    
    def _parseCancelOrder(self, order):
        if order["code"] != '0':
            raise Exception(order['msg'])
        parsedOrder = {'id': None, "symbol": None, "amount": None, "side": None, "timestamp": None, "status": None, "orderJson": None}
        parsedOrder['id'] = order["data"]["orderId"]
        parsedOrder["orderJson"] = json.dumps(order["data"])
        return parsedOrder
    
    ## Exchange functions 
    def fetch_ticker(self, symbol):
        raise NotImplementedError("method not implemented")
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = "/uapi/v1/account/balance" #"/api/v1/asset/balances"
        params.update({'accountType': 'spot', 'asset_type': 'BALANCE'})
        try:
            resp = self._signedRequest('GET', apiUrl, params)
            return self._parseBalance(resp)
        except Exception as e:
            raise e
        
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}): 
        apiUrl = "/api/v1/trade/fills-history"
        try:
            if since:
                params["begin"] = int(since)
            if 'endTime' in params and params['endTime']:
                params['end'] = params['endTime']
            response = self._signedRequest('POST', request_path=apiUrl, queryString=params)
            return self._parseFetchTrades(response)
        except Exception as e:
            raise e
    
    def create_order(self, symbol, side, amount, order_type, price=None, params={}): 
        if order_type == "limit":
            return self.create_limit_order(symbol, side, amount, price, params)
        elif order_type == "market":
            return self.create_market_order(symbol, side, amount, params)
        else: raise Exception("wrong order type, only supports market and limit")
    
    def create_market_order(self, symbol, side, amount, params={}):
        apiUrl = "/0/private/AddOrder"
        body = {
            "instId":self._getSymbol(symbol),
            "orderType":"market",
            "side":side,
            "size":str(amount),
            "marginMode":"cross"
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, body=body, queryString='')
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def create_limit_order(self, symbol, side, amount, price, params={}):
        apiUrl = "/api/v1/trade/order"
        body = {
            "instId":self._getSymbol(symbol),
            "orderType":"limit",
            "side":side,
            "price":str(price),
            "size":str(amount)
        }
        try:
            body.update(params) 
            response = self._signedRequest('POST', request_path=apiUrl, queryString='', body=body)
            return self._parseCreateorder(response)
        except Exception as e:
            raise e
    
    def cancel_order(self, id=None, symbol=None, params={}):
        apiUrl = "/api/v1/trade/cancel-order"
        ticker = self._getSymbol(symbol)
        try:
            params={}
            if id is not None:
                params['orderId'] = id
            if symbol is not None:
                params['instId'] = ticker
            params.update(params)
            response = self._signedRequest('POST', request_path=apiUrl, queryString='',body=params)
            return self._parseCancelOrder(response)
        except Exception as e:
            raise e
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        apiUrl = "/api/v1/trade/orders-pending"
        try:
            response = self._signedRequest('GET', request_path=apiUrl, queryString={}, body=None)
            return self._parseOpenOrders(response)
        except Exception as e:
            raise e
    
    def fetch_order(self, id, symbol = None, params={}):
        raise NotImplementedError("method not supported")