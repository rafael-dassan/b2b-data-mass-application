# Adding a new region on data_mass

## Add REDIRECT_URL and CLIENT_ID Parameters to the Functions that uses regions:
``` python
def get_iam_b2c_country_params_uat(country):     
def get_iam_b2c_country_params_sit(country):
def get_iam_b2c_country_params_qa(country):
```
## Also add the new region to the validations functions as:
``` python
def valid_country(country):
def validate_country_menu_in_user_create_iam(zone):
def validate_zone_for_interactive_combos_ms(zone):
def validate_zone_for_ms(zone):

```
## UAT functions for recommendations:
```python
def get_header_request_recommender(zone, environment):
```
## Get the mockup for adresses:
```python
def get_account_delivery_address(zone):
```
## Other functions that might be changed according to business rules:
```python
def create_quick_order_payload(account_id, zone, product_list):
def get_order_prefix_params(zone):
def create_forgotten_items_payload(account_id, zone, product_list):
def create_upsell_payload(account_id, zone, product_list):
```
## Add magento credentials on DT, QA, SIT, UAT:
```python
def get_magento_base_url(environment, country):
def get_magento_user_registration_access_token(environment, country):
```
# Set the information terms for the new region according to business rules
```python
def generate_terms_information(zone):
```

# Test functions
```python
def get_email_param(country):
def get_account_params(country):

```
-------------------------------------------------

# Business rules questions:

TO REMMBER = Add info for populator