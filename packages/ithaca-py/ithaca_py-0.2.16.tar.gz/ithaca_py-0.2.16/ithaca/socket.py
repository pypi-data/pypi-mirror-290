"""Socket Module."""

import ssl
from json import dumps, loads

import websocket


class Socket:
    """Socket Class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent
        self._ws_app = None

    def __on_open(self, ws):
        print("socket connection open...\n")
        params = {
            "action": "VALIDATE_AUTH_TOKEN",
            "payload": self.parent.user.get("authToken"),
        }
        ws.send(dumps(params))

    def __on_error(self, ws, error):
        print(error)

    def __on_close(self, wsapp, close_status_code, close_msg):
        print("on_close args:")
        if close_status_code or close_msg:
            print("close status code: " + str(close_status_code))
            print("close message: " + str(close_msg))

    def __on_message(self, ws, message):
        data = loads(message)
        if data.get("responseType") == "EXEC_REPORT":
            payload = data.get("payload")
            print(payload)
            # print("---" * 20)
            # print(f"{payload.get('orderStatus')} order for {payload.get('netPrice')}")
            # legs = payload.get("details")
            # if legs:
            #     for leg in legs:
            #         payoff = leg["contractDto"]["payoff"]
            #         expiry = leg["contractDto"]["economics"]["expiry"]
            #         strike = leg["contractDto"]["economics"]["strike"]
            #         side = leg["side"]
            #         quantity = leg["originalQty"]
            #         print(
            #             f"       {side} {quantity} {payoff} @ {strike} for {expiry}",
            #         )
        else:
            print(data)

    def connect(self, on_message = None):
        """Attempt to connect to the websocket endpoint."""
        print("connect: start: " + self.parent.ws_url)
        print("auth: " + self.parent.user.get("authToken"))

        if on_message is None:
            on_message = self.__on_message

        self._ws_app = websocket.WebSocketApp(
            url=self.parent.ws_url,
            on_message=on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
            on_open=self.__on_open,
        )
        sslopt = (
            {"cert_reqs": ssl.CERT_NONE}
            if "localhost" in self.parent.base_url
            else None
        )

        self._ws_app.run_forever(ping_interval=14, sslopt=sslopt, reconnect=10)

    def close(self):
        if self._ws_app:
            self._ws_app.close()
            print("WebSocket connection closed.")
