import logging
import asyncio
import random
from aiocoap import Context, Message, Code

# Configure logging to display debug information
logging.basicConfig(level=logging.INFO)

# Function to observe the state of a CoAP resource on the server using a GET request
async def observe_coap_get_request(uri):
    # Create a CoAP client context
    protocol = await Context.create_client_context()
    observe_value = 0

    while True:
        # Create a GET request with observe information
        request = Message(code=Code.GET, uri=uri, observe=observe_value)
        pr = protocol.request(request)

        # Send the request and receive the response from the server
        r = await pr.response

        # Display the response content
        print("Response from {}: {}".format(uri, r.payload.decode()))

        # Increase the observe value to send a new observe request
        observe_value += 1

        # Wait for 3 seconds before sending the next request
        await asyncio.sleep(3)

# Function to send random POST requests to control a CoAP resource
async def coap_post_request_client():
    while True:
        # Create a random payload (0 or 1)
        payload = str(random.choice([0, 1])).encode('utf-8')

        # Create a POST request with the created payload
        post_request = Message(code=Code.POST, payload=payload)
        post_request.set_request_uri("coap://192.168.243.75:5683/Control")

        # Create a CoAP client context
        context = await Context.create_client_context()

        try:
            # Send the request and receive the response from the server
            post_response = await context.request(post_request).response

            # Display the response content
            print(f"POST Response from server: {post_response.payload.decode('utf-8')}")
        except Exception as e:
            # Handle any errors that occur while sending the request
            print(f"POST Error: {e}")

        # Wait for 10 seconds before sending the next POST request
        await asyncio.sleep(10)

# Main function that initializes the tasks
async def main():
    # CoAP resource addresses on the server
    uri1 = 'coap://192.168.243.99:5683/Data'
    uri2 = 'coap://192.168.243.75:5683/Data'

    # Create a list of tasks to be executed
    tasks = [
        observe_coap_get_request(uri1),
        observe_coap_get_request(uri2),
        coap_post_request_client()
    ]

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

# Run the main function when the program is executed
if __name__ == "__main__":
    asyncio.run(main())
