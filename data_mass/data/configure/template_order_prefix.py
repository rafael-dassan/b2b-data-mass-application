from string import Template

# Create the template String
TEMPLATE_ORDER_PREFIX = Template("""
{
  "orderNumberSize": $orderNumberSize,
  "prefix": "$prefix"
} """)
