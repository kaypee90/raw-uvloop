import json


class App:
    @staticmethod
    async def read_body(receive):
        """
        Read and return the entire body from an incoming ASGI message.
        """
        body = b''
        more_body = True

        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        return json.loads(body)

    async def __call__(self, scope, receive, send):
        """
        Echo the request body back in an HTTP response.
        """
        body = {}
        if scope["method"] == "POST" or scope["method"] == "PUT":
            body = await self.read_body(receive)

        response = json.dumps({
            "message": "Request received successfully!!!!",
            "meta": {
                "served_by": "uv_loop"
            },
            "person": {
                "id": 1,
                **body
            }
        })

        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                (b'content-type', b'applicaton/json'),
                (b'content-length', str(len(response)).encode("utf-8"))
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': response.encode("utf-8"),
        })


app = App()