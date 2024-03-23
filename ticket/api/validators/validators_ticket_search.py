from rest_framework import serializers

def validate_if_url_allowed(allowed_url, provided_url):
    if not allowed_url in provided_url:
        raise serializers.ValidationError("The url you have provided is incorrect.")
    else: pass