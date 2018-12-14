*** Variables ***

# Screen elements
${TV_SPECIFIC_BEER}                 xpath=//android.widget.LinearLayout[@content-desc="Product list"][1]/android.widget.LinearLayout/android.widget.TextView
${ET_ADD_PRODUCT_QUANTITY}          xpath=//android.widget.EditText[@content-desc="Add edit"][1]
${ET_ADD_REMOVE_PRODUCT_TRUCK}      xpath=//android.widget.EditText[@content-desc="Your Order: edit"]
${IV_BRAND_IMAGE}                   id=brand_image
${IV_TRUCK}                         id=truck
${TV_TRUCK_EMPTY}                   id=empty_copy
${TV_ORDER_TITLE_LABEL}             id=order_title_label
${BTN_SUBMIT_ORDER}                 id=submitOrder
${TV_LOADING_TITLE}                 id=loading_title   
${TV_MINIMUM_ORDER}                 id=percentText  
${TV_ORDER_NUMBER}                  id=addPoNumber   
${TV_NO_DELIVERY_WINDOW}            id=noDeliveryWindowsText
${TV_ORDER_PLACED}                  id=orderPlaced
${TV_STATUS_ORDER}                  id=orderIdCell
${TV_RECENT_ORDERS_LINK}            id=recentTextLink
${ORDERS_TAB}                       xpath=//android.widget.TextView[@content-desc="Orders tab"]
${TV_TOTAL_ORDER}                   id=orderTotal
${TV_PRICE_INFO}                    xpath=//android.support.v7.widget.RecyclerView[@content-desc="Todos los Pedidos"]/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.TextView[3]
${TV_STATUS_SENT}                   xpath=//android.support.v7.widget.RecyclerView[@content-desc="Todos los Pedidos"]/android.widget.LinearLayout[2]/android.widget.TextView
${TABLE_ORDER_SUMMARY}              xpath=//android.widget.LinearLayout[@content-desc="Order Summary table"]/android.widget.LinearLayout[4]
${LAYOUT_DELIVERY_WINDOW}           id=deliveryWindowSelectionScreen

# Messages
${PRODUCT_TYPE}                     Cerveza Quilmes
${MY_TRUCK}                         Mi Camión
${TRUCK_EMPTY_MESSAGE}              No tenes nada en tu Camión. ¿Qué estás esperando?
${MINIMUM_ORDER_COMPLETED_MESSAGE}  Orden Mínima 100% Completa
${NO_DELIVERY_WINDOW_MESSAGE}       Disculpe, no hay fechas de entrega disponibles. Se enviará la orden en la próxima fecha de entrega disponible
${PRODUCT_QUANTITY}                 5
${PRODUCT_MINIMUM_QUANTITY}         2
${ZEROED_PRODUCT_QUANTITY}          0
${ORDER_NUMBER}                     12345 
${ORDER_STATUS_MESSAGE}             ¡Pedido enviado correctamente!
${ORDER_STATUS}                     Esperando confirmación
@{order_statuses}                   Enviado     Integrado       Esperando confirmación      Integrando