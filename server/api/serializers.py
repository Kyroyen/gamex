from rest_framework.serializers import ModelSerializer

from .models import ApiUser,Blog,Comment

class ApiUserSerializer(ModelSerializer):
    class Meta:
        model = ApiUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            ]
        extra_kwargs = {
            "password" : {"write_only" : True},
            }
        
    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop("password",None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "creator",
            "date_created",
            ]

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
            "date_created",
            "owner",
            ]