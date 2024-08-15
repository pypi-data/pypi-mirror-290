class RPCClient:
    def __init__(self, rpc_url):
        self.rpc = rpc_url

    def rpc_call(self, method, params):
        """
        Makes an RPC call using the provided method and parameters.
        """
        # Check if the response already exists in the database
        cached_response = fetch_response_data(method, params)
        if cached_response:
            return cached_response

        # If no cached response exists, proceed with the RPC call
        headers = {"Content-Type": "application/json"}
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }
        response = getPostRequest(self.rpc, request_data, headers)

        # Save the response to the database for future use
        session = dbConfig().session
        new_entry = ResponseData(signature=request_data['id'], method=method, params=json.dumps(params), response=json.dumps(response))
        session.add(new_entry)
        session.commit()

        return response
