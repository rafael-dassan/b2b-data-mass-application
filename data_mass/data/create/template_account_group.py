from string import Template

# Create the template String
TEMPLATE_ACCOUNT_GROUP = Template("""
{
  "accountGroupId": "$accountGroupId",
  "accounts": "$accounts"
} """)
