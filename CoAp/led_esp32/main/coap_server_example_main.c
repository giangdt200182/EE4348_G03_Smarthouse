#include <string.h>
#include <sys/socket.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "protocol_examples_common.h"
#include "coap3/coap.h"
#include "driver/adc.h"
#include "driver/gpio.h"

#define EXAMPLE_COAP_PSK_KEY CONFIG_EXAMPLE_COAP_PSK_KEY
#define EXAMPLE_COAP_LOG_DEFAULT_LEVEL CONFIG_COAP_LOG_DEFAULT_LEVEL

const static char *TAG = "CoAP_server";

// GPIO pin for controlling the switch
#define SWITCH_GPIO_PIN GPIO_NUM_2

// Global variable to store LED state
static int led_state = 0;

/* Counter variable */
static int i = 0;

/* The resource handler for "Data" path */
static void hnd_data_get(coap_resource_t *resource,
                         coap_session_t *session,
                         const coap_pdu_t *request,
                         const coap_string_t *query,
                         coap_pdu_t *response)
{
    // Update the counter value
    if (led_state == 1) {
        i++;
    } else if (led_state == 0) {
        i = 0;
    }
    // Send the current state of the LED
    ESP_LOGI(TAG, "Sending LED state in response to GET request: %d,%d", led_state,i);

    char led_state_response[10];  // Adjust the size based on your requirements
    snprintf(led_state_response, sizeof(led_state_response), "%d,%d", led_state, i);

    //char led_state_response[2];
    //snprintf(led_state_response, sizeof(led_state_response), "%d", led_state);
    coap_pdu_set_code(response, COAP_RESPONSE_CODE_CONTENT);
    coap_add_data_large_response(resource, session, request, response,
                                 query, COAP_MEDIATYPE_TEXT_PLAIN, 60, 0,
                                 strlen(led_state_response),
                                 (const u_char *)led_state_response,
                                 NULL, NULL);
}

/* The resource handler for "Control" path */
static void hnd_control_post(coap_resource_t *resource,
                             coap_session_t *session,
                             const coap_pdu_t *request,
                             const coap_string_t *query,
                             coap_pdu_t *response)
{
    // Extract the payload from the POST request
    const uint8_t *payload;
    size_t payload_len;
    coap_get_data(request, &payload_len, &payload);

    // Convert the payload to an integer (assuming payload is a valid integer)
    int control_value = atoi((const char *)payload);

    // Now, you can use control_value to control the LED
    gpio_set_level(SWITCH_GPIO_PIN, control_value);

    // Update the global LED state
    led_state = control_value;

    // Print a message to the command window
    ESP_LOGI(TAG, "LED state set to: %d", control_value);

    // Send a response indicating success (you can customize the response)
    coap_pdu_set_code(response, COAP_RESPONSE_CODE_CHANGED);
}

/* CoAP server task */
static void coap_example_server(void *p)
{
    coap_context_t *ctx = NULL;
    coap_address_t serv_addr;
    coap_resource_t *resource = NULL;

    coap_set_log_level(EXAMPLE_COAP_LOG_DEFAULT_LEVEL);

    while (1) {
        coap_endpoint_t *ep = NULL;
        unsigned wait_ms;

        /* Prepare the CoAP server socket */
        coap_address_init(&serv_addr);
        serv_addr.addr.sin6.sin6_family = AF_INET6;
        serv_addr.addr.sin6.sin6_port   = htons(COAP_DEFAULT_PORT);

        ctx = coap_new_context(NULL);
        if (!ctx) {
            ESP_LOGE(TAG, "coap_new_context() failed");
            continue;
        }
        coap_context_set_block_mode(ctx, COAP_BLOCK_USE_LIBCOAP | COAP_BLOCK_SINGLE_BODY);

        ep = coap_new_endpoint(ctx, &serv_addr, COAP_PROTO_UDP);
        if (!ep) {
            ESP_LOGE(TAG, "udp: coap_new_endpoint() failed");
            goto clean_up;
        }
        ep = coap_new_endpoint(ctx, &serv_addr, COAP_PROTO_TCP);
        if (!ep) {
            ESP_LOGE(TAG, "tcp: coap_new_endpoint() failed");
            goto clean_up;
        }

        // Resource for "Data" path
        resource = coap_resource_init(coap_make_str_const("Data"), 0);
        if (!resource) {
            ESP_LOGE(TAG, "coap_resource_init() failed for Data");
            goto clean_up;
        }
        coap_register_handler(resource, COAP_REQUEST_GET, hnd_data_get);
        coap_resource_set_get_observable(resource, 1);
        coap_add_resource(ctx, resource);

        // Resource for "Control" path
        resource = coap_resource_init(coap_make_str_const("Control"), 0);
        if (!resource) {
            ESP_LOGE(TAG, "coap_resource_init() failed for Control");
            goto clean_up;
        }
        coap_register_handler(resource, COAP_REQUEST_POST, hnd_control_post);
        coap_add_resource(ctx, resource);

        wait_ms = COAP_RESOURCE_CHECK_TIME * 1000;

        while (1) {
            int result = coap_io_process(ctx, wait_ms);
            if (result < 0) {
                break;
            } else if (result && (unsigned)result < wait_ms) {
                /* decrement if there is a result wait time returned */
                wait_ms -= result;
            }
            if (result) {
                /* result must have been >= wait_ms, so reset wait_ms */
                wait_ms = COAP_RESOURCE_CHECK_TIME * 1000;
            }
        }
    }

clean_up:
    coap_free_context(ctx);
    coap_cleanup();

    vTaskDelete(NULL);
}

void app_main(void)
{
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
     * Read "Establishing Wi-Fi or Ethernet Connection" section in
     * examples/protocols/README.md for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());

    // Configure GPIO for controlling the switch
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << SWITCH_GPIO_PIN),
        .mode = GPIO_MODE_OUTPUT,
    };
    ESP_ERROR_CHECK(gpio_config(&io_conf));

    xTaskCreate(coap_example_server, "coap", 8 * 1024, NULL, 5, NULL);
}
