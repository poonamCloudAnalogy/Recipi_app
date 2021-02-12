from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer for user object"""
    class Meta:
        model = get_user_model()
        '''  call user model that return user model \
            class fields we want to include in our serializer '''
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):  # create function create a new object
        ''' create a new ueser with encrypted password and return it '''
        return get_user_model().object.create_user(**validated_data)

    def update(self, instance, validated_data):
        ''' update a user, setting the password correctly and return it '''
        ''' firstly it remove old password '''
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        ''' super call modelserializer update function '''
        if password:
            user.set_password(password)
            user.save()
        return user


''' serializer to authenticating our request '''


class AuthTokenSerializer(serializers.Serializer):
    ''' serializer for the user authentication object '''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        ''' validate and authenticate the user/ '''
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
