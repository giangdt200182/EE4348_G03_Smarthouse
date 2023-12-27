import logging
import asyncio
import random
from aiocoap import Context, Message, Code, error

# Configure logging to display debug information
logging.basicConfig(level=logging.INFO)

# Function to observe the state of a CoAP resource on the server using a GET request
async def observe_coap_get_request(uri):
    while True:
        try:
            # Create a CoAP client context
            protocol = await Context.create_client_context()

            # Create a GET request with observe information
            request = Message(code=Code.GET, uri=uri, observe=0)
            pr = protocol.request(request)

            # Send the request and receive the response from the server
            r = await pr.response

            # Display the response content
            print("Response from {}: {}".format(uri, r.payload.decode()))

        except error.RequestTimedOut:
            # Handle the case where the request times out (no connection)
            print("Timeout while requesting {}, trying again...".format(uri))

        except Exception as e:
            # Handle any other exceptions that may occur
            print("Error: {}".format(e))

        # Wait for 2 seconds before sending the next request
        await asyncio.sleep(2)

# Function to send random POST requests to control a CoAP resource
async def coap_post_request_client():
    while True:
        try:
            # Create a random payload (0 or 1)
            payload = str(random.choice([0, 1])).encode('utf-8')

            # Create a POST request with the created payload
            post_request = Message(code=Code.POST, payload=payload)
            post_request.set_request_uri("coap://192.168.243.99:5683/Control")

            # Create a CoAP client context
            context = await Context.create_client_context()

            # Send the request and receive the response from the server
            post_response = await context.request(post_request).response

            # Display the response content
            print(f"POST Response from server: {post_response.payload.decode('utf-8')}")

        except error.RequestTimedOut:
            # Handle the case where the request times out (no connection)
            print("Timeout while sending POST request, trying again...")

        except Exception as e:
            # Handle any other exceptions that may occur
            print(f"POST Error: {e}")

        # Wait for 5 seconds before sending the next POST request
        await asyncio.sleep(5)

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
