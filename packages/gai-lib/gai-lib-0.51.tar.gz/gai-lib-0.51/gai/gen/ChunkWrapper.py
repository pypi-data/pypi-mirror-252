import json
class ChunkWrapper:

    # chunk is json in binary representation
    def __init__(self, chunk):
        self.chunk = chunk

    def __str__(self):
        return self.chunk.decode('utf-8')

    def decode(self):
        decoded_chunk = json.loads(self.chunk.decode('utf-8'))
        if "content" in decoded_chunk["choices"][0]["delta"] and decoded_chunk["choices"][0]["delta"]['content']:
            return decoded_chunk["choices"][0]["delta"]["content"], "text"
        if decoded_chunk["choices"][0]["delta"]['tool_calls'] and decoded_chunk["choices"][0]["delta"]['tool_calls'][0]['function']['name']:
            return {"name": decoded_chunk["choices"][0]["delta"]['tool_calls'][0]['function']['name']}, "tool_name"
        if decoded_chunk["choices"][0]["delta"]['tool_calls'] and decoded_chunk["choices"][0]["delta"]['tool_calls'][0]['function']['arguments']:
            return {"arguments": decoded_chunk["choices"][0]["delta"]['tool_calls'][0]['function']['arguments']}, "tool_arg"
        if decoded_chunk["choices"][0]["finish_reason"]:
            return {"finish_reason": decoded_chunk["choices"][0]["finish_reason"]}, "finish_reason"
    
    def __dict__(self):
        return json.loads(self.chunk.decode('utf-8'))

