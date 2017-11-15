# from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import serializers
# from rest_framework.exceptions import ParseError
from taggit.models import Tag
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from api.models import (Article, Story, Fact, Comment,
                        Citation, Cluster, CitationComment, MyUser)


class CitationCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CitationComment
        fields = '__all__'

    def to_representation(self, obj):
        return super(CitationCommentSerializer, self).to_representation(obj)


class CitationSerializer(serializers.ModelSerializer):
    comm_citation = CitationCommentSerializer(many=True)

    class Meta:
        model = Citation
        fields = ('text', 'description', 'url', 'approval', 'fact_id',
                  'comm_citation')

    def to_representation(self, obj):
        return super(CitationSerializer, self).to_representation(obj)

    def __str__(self):
        return self.text


class FactSerializer(serializers.ModelSerializer):
    cit_fact = CitationSerializer(many=True)

    class Meta:
        model = Fact
        fields = ('id', 'article', 'upvoted', 'downvoted', 'sentence_id',
                  'text',
                  'upvoted_by', 'downvoted_by', 'cit_fact')
        lookup_field = 'id'

    def to_representation(self, obj):
        return super(FactSerializer, self).to_representation(obj)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, obj):
        return super(CommentSerializer, self).to_representation(obj)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    keywords = TagListSerializerField()
    fact_article = FactSerializer(many=True)
    comm_article = CommentSerializer(many=True)

    class Meta:
        model = Article
        fields = ('fact_article', 'comm_article', 'article_id', 'story_id',
                  'title',
                  'authors',
                  'image_url',
                  'url', 'videos', 'summary', 'text', 'pub_date', 'keywords',
                  'subjectivity', 'hotness', 'spelling', 'grammar',
                  'source_id')

    def to_representation(self, obj):
        return super(ArticleSerializer, self).to_representation(obj)


class ArticleSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('article_id',
                  'title',
                  'authors',
                  'image_url',
                  'url', 'videos', 'summary', 'text', 'pub_date',
                  'subjectivity', 'hotness', 'spelling', 'grammar',
                  'source_id')

    def to_representation(self, obj):
        return super(ArticleSerializerShort, self).to_representation(obj)


class StorySerializer(TaggitSerializer, serializers.ModelSerializer):
    keywords = TagListSerializerField()
    articles = ArticleSerializerShort(many=True)

    class Meta:
        model = Story
        fields = ('story_id', 'story_name', 'pub_date', 'rating_users',
                  'rating_subjectivity', 'hotness', 'keywords', 'image_url',
                  'articles')


class StorySerializerShort(serializers.ModelSerializer):
    articles = ArticleSerializerShort(many=True)

    class Meta:
        model = Story
        fields = ('story_id', 'story_name', 'pub_date', 'rating_users',
                  'rating_subjectivity', 'hotness', 'image_url',
                  'articles')


class KeywordSerializerField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list('name', flat=True)


class KeywordSerializer(serializers.ModelSerializer):
    stories = StorySerializerShort(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('name', 'stories')
        lookup_field = 'name'

    def to_representation(self, obj):
        stories = Story.objects.filter(keywords__name=obj)
        obj.stories = stories
        return super(KeywordSerializer, self).to_representation(obj)


class KeywordSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

    def to_representation(self, obj):
        return super(KeywordSerializerShort, self).to_representation(obj)


# first we define the serializers
'''class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'avatar')
'''


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class ClusterSerializer(serializers.ModelSerializer):
    article_cluster = ArticleSerializerShort(many=True)

    class Meta:
        model = Cluster
        fields = ('cluster_id', 'cluster_name', 'article_cluster')

    def to_representation(self, obj):
        return super(ClusterSerializer, self).to_representation(obj)


class ClusterSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = Cluster
        fields = ('cluster_id', 'cluster_name')

    def to_representation(self, obj):
        return super(ClusterSerializerShort, self).to_representation(obj)


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("last_login", 'id', "username", "first_name", "last_name",
                  "email",
                  "date_joined", "avatar", "clusters", "interests")

    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user
