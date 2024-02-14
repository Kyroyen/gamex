from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, HyperlinkedModelSerializer
from rest_framework import serializers
from .models import ApiUser, Blog, Comment


class ApiUserSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="logged-in-user-view:user-view", lookup_field="username", read_only=True)
    # url = serializers.IntegerField(source = "id")
    class Meta:
        model = ApiUser
        fields = [
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def is_valid(self, *, raise_exception=False):
        # print(self.data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class BlogSerializer(ModelSerializer):
    creator = ApiUserSerializer(required=False)
    url = HyperlinkedIdentityField(
        view_name="logged-in-user-view:blog-detail", lookup_field="id", read_only=True)

    class Meta:
        model = Blog
        fields = [
            "url",
            "title",
            "content",
            "creator",
            "date_created",
        ]
        extra_kwargs = {
            "creator": {
                "validators": ["validate_creator"],
            }
        }

    def validate_creator(self, value):
        return value

    def to_internal_value(self, data):
        creator = data.pop("creator")
        fin_data = super().to_internal_value(data)
        fin_data["creator"] = creator
        return fin_data


class CommentSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(view_name = "logged-in-user-view:comment-detail", lookup_field = "id", read_only = True)
    # user = ApiUserSerializer(source = "owner", read_only = True)
    owner = ApiUserSerializer(required=False)

    class Meta:
        model = Comment
        fields = [
            # "url",
            "content",
            "date_created",
            "owner",
            "blog",
        ]
        extra_kwargs = {
            "owner": {"validators": ["validate_owner"]},
            "blog": {"write_only": True},
        }

    def to_internal_value(self, data):
        owner = data.pop("owner")
        x = super().to_internal_value(data)
        x["owner"] = owner
        return x

    def validate_owner(self, value):
        return value

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
