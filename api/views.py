import json
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response, render
from django.views.generic import DetailView
# from django.contrib.auth.models import User
# from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.fields import CurrentUserDefault
from rest_framework.permissions import IsAuthenticated
from api.permissions import (POSTOnlyAuthentication, IsStaffOrTargetUser)

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter # noqa

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.views import LoginView
from rest_auth.social_serializers import TwitterLoginSerializer

from rest_framework.views import APIView
from allauth.account.views import ConfirmEmailView
from rest_framework.permissions import AllowAny

from rest_auth.registration.views import SocialLoginView
from taggit.models import Tag
from api.models import (Article, Story, Fact, Comment, Citation,
                        Cluster, CitationComment, Source, MyUser)
from api.serializers import (ArticleSerializer, StorySerializer,
                             KeywordSerializer, FactSerializer,
                             UserSerializer, CommentSerializer,
                             CitationSerializer, ClusterSerializer,
                             ClusterSerializerShort, ArticleSerializerShort,
                             KeywordSerializerShort, CitationCommentSerializer,
                             VerifyEmailSerializer)


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)



class ArticlesView(DetailView):
    def __init__(self):
        self.articles = Article.objects.all()[:20]
        self.keywords = []
        for s in self.articles:
            keywords_s = s.keywords.all()
            keywords_s = [k.name for k in keywords_s]
            self.keywords.append(keywords_s)
        self.articles = serializers.serialize("json", self.articles)
        self.articles = json.loads(self.articles)
        for i in range(len(self.articles)):
            self.articles[i]['keywords'] = self.keywords[i]

    def get(self, request):
        uri = request.build_absolute_uri()
        if '.json' in uri:
            self.articles = json.dumps(self.articles)
            return HttpResponse(self.articles, content_type='application/json')
        else:
            return render(request, 'articles.html',
                          {"articles": self.articles})


class StoriesView(DetailView):
    def __init__(self):
        self.stories = Story.objects.all()[:11]
        self.articles = []
        self.keywords = []
        self.clusters = []
        for story in self.stories:
            try:
                articles_s = Article.objects.filter(story_id=story.story_id)
                if type(articles_s) == Article:
                    articles_s = [articles_s]
                articles_s = [{'image_url': a.image_url,
                               'id': a.article_id, 'title': a.title,
                               'summary': a.summary, 'authors': a.authors,
                               'cluster':
                               Cluster.objects.get(
                                   cluster_id=a.article_cluster.cluster_id),
                               'source': Source.objects.get(id=a.source_id.id),
                               'subjectivity': a.subjectivity,
                               'spelling': 100 - a.spelling}
                              for a in articles_s]
                self.articles.append(articles_s[:5])
            except:
                self.articles.append([])

        for s in self.stories:
            self.clusters.append(
                Cluster.objects.get(cluster_id=s.story_cluster.cluster_id))
            keywords_s = s.keywords.all()
            keywords_s = [k.name for k in keywords_s]
            self.keywords.append(keywords_s)

        self.stories = serializers.serialize("json", self.stories)
        self.stories = json.loads(self.stories)
        for i in range(len(self.stories)):
            self.stories[i]['articles'] = self.articles[i]
            self.stories[i]['cluster'] = self.clusters[i]
            self.stories[i]['keywords'] = self.keywords[i][:10]

    def get(self, request):
        uri = request.build_absolute_uri()
        if '.json' in uri:
            self.stories = json.dumps(self.stories)
            return HttpResponse(self.stories, content_type='application/json')
        else:
            return render(request, 'stories.html',
                          {"stories": self.stories,
                           "keywords": self.keywords,
                           "articles": self.articles})


class KeywordView(DetailView):
    def get(self, request, slug, **kwargs):
        slug = slug.replace('%20', ' ')
        uri = request.build_absolute_uri()
        posts = Story.objects.filter(keywords__name=slug)
        if '.json' in uri:
            posts = serializers.serialize("json", posts)
            return HttpResponse(posts, content_type='application/json')
        else:
            return render_to_response('keywords.html', {"posts": posts,
                                                        "keyword": slug})


class StoryDetailedView(DetailView):
    def get(self, request, pk):
        uri = request.build_absolute_uri()
        story = [Story.objects.get(pk=pk)]
        articles = Article.objects.filter(story_id=pk)
        articles = [{'id': a.article_id, 'title': a.title,
                     'summary': a.summary,
                     'image_url': a.image_url}
                    for a in articles]
        keywords = story[0].keywords.all()
        keywords = [k.name for k in keywords]
        story = serializers.serialize("json", story)
        story = json.loads(story)
        story[0]['articles'] = articles
        story[0]['keywords'] = keywords
        if '.json' in uri:
            story = json.dumps(story)
            return HttpResponse(story, content_type='application/json')
        else:
            return render_to_response('story-detailed.html',
                                      {"story": story,
                                       "keywords": keywords})


class ArticleDetailedView(DetailView):
    def get(self, request, pk):
        uri = request.build_absolute_uri()
        article = Article.objects.get(pk=pk)
        facts = Fact.objects.filter(article=article)
        keywords = article.keywords.all()
        keywords = [k.name for k in keywords]
        # article = serializers.serialize("json", article)
        # article = json.loads(article)
        # article = article[0]
        if '.json' in uri:
            article = serializers.serialize("json", [article])
            # article = json.loads(article)
            # article = json.dumps(article)
            return HttpResponse(article, content_type='application/json')
        else:
            return render_to_response('article-detailed.html',
                                      {"article": article,
                                       "keywords": keywords,
                                       "facts": facts})


class ArticleApiViewSet(viewsets.ModelViewSet):
    facts = Fact.objects.all()
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializerShort
        return ArticleSerializer

    @detail_route()
    def article(self, request, *args, **kwargs):
        article = self.get_object()
        return Response(article)


class StoryApiViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    @detail_route()
    def story(self, request, *args, **kwargs):
        story = self.get_object()
        return Response(story)

    @list_route()
    def recommended(self, request, *args, **kwargs):
        # user = request.user
        queryset = Story.objects.all()[11:20]
        serializer = StorySerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def featured(self, request, *args, **kwargs):
        # user = request.user
        queryset = Story.objects.all()[21:30]
        serializer = StorySerializer(queryset, many=True)
        return Response(serializer.data)


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return KeywordSerializerShort
        return KeywordSerializer
    lookup_field = 'name'


class TopicView(DetailView):
    def get(self, request, slug, **kwargs):
        uri = request.build_absolute_uri()
        posts = Story.objects.filter(story_cluster__cluster_name=slug)
        if '.json' in uri:
            posts = serializers.serialize("json", posts)
            return HttpResponse(posts, content_type='application/json')
        else:
            return render_to_response('topics.html', {"posts": posts,
                                                      "topic": slug})


class FactApiViewSet(viewsets.ModelViewSet):
    queryset = Fact.objects.all()
    serializer_class = FactSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (POSTOnlyAuthentication,)
    user_serializer = UserSerializer

    @detail_route(methods=['get'])
    def fact(self, request, format=None):
        if request.method == 'GET':
            fact = self.get_object()
            return Response(fact)

    @detail_route(methods=['post'])
    def upvote(self, request, format=None, *args, **kwargs):
        # user = CurrentUserDefault() 
        user = request.user
        fact = self.get_object()
        if not Fact.objects.filter(upvoted_by=user):
            fact.upvote()
            fact.upvoted_by.add(user)
            fact.save()
            return Response('Upvoted')
        else:
            return Response('You have already voted')

    @detail_route(methods=['post'])
    def downvote(self, request, format=None, *args, **kwargs):
        user = request.user
        fact = self.get_object()
        if not Fact.objects.filter(downvoted_by=user):
            fact.downvote()
            fact.downvoted_by.add(user)
            fact.save()
            return Response('Downvoted')
        else:
            return Response('You have already voted')

    @list_route(methods=['post'])
    def create_fact(self, request, format=None, *args, **kwargs):
        article = request.data['article']
        text = request.data['text']
        print(article)
        sentence = int(request.data['sentence_id'].strip())
        print(sentence)
        user = request.user
        if not article:
            return (Response('Article is not provided'))
        if not sentence:
            return (Response('Sentence is not provided'))

        article = Article.objects.get(pk=article)
        if user and article and sentence:
            fact = Fact(article=article, text=text,
                        user=user, sentence_id=sentence)
            fact.save()
            str_to_replace = r'fact="0" sent_id="{}"'.format(sentence)
            replacement_str = r'fact="1" sent_id="{}"'.format(sentence)
            article.text = article.text.replace(str_to_replace,
                                                replacement_str)
            article.save()
            return(Response('Fact added'))
        else:
            return(Response('Not provided all fields'))


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(LoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class CommentApiViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (POSTOnlyAuthentication,)
    user_serializer = UserSerializer

    @detail_route(methods=['get'])
    def comment(self, request, format=None):
        if request.method == 'GET':
            comment = self.get_object()
            return Response(comment)

    @list_route(methods=['post'])
    def create_comment(self, request, format=None, *args, **kwargs):

        user = request.user
        article = request.data['article_id']
        article = Article.objects.get(article_id=article)
        recipient = None
        if request.data['recipient']:
            recipient = request.data['recipient']
            recipient = MyUser.objects.get(id=recipient)
        if user:
            comment = Comment(article_id=article, title=request.data['title'],
                              text=request.data['text'], user=user,
                              recipient=recipient)
            comment.save()
        return(Response('Comment added'))

    @detail_route(methods=['post'])
    def upvote(self, request, format=None, *args, **kwargs):
        user = request.user
        comment = self.get_object()
        if not Comment.objects.filter(upvoted_by=user):
            comment.upvoted = comment.upvoted + 1
            comment.upvoted_by.add(user)
            comment.save()
            return Response('Upvoted')
        else:
            return Response('You have already voted')

    @detail_route(methods=['post'])
    def downvote(self, request, format=None, *args, **kwargs):
        user = request.user
        comment = self.get_object()
        if not Comment.objects.filter(upvoted_by=user):
            comment.downvoted = comment.downvoted + 1
            comment.downvoted_by.add(user)
            comment.save()
            return Response('Downvoted')
        else:
            return Response('You have already voted')

    @detail_route(methods=['post'])
    def report(self, request, format=None, *args, **kwargs):
        user = request.user
        comment = self.get_object()
        if not Comment.objects.filter(reported_by=user):
            comment.reported_by.add(user)
            comment.save()
            return Response('Reported')
        else:
            return Response('You have reported this comment')


class CitationApiViewSet(viewsets.ModelViewSet):
    queryset = Citation.objects.all()
    serializer_class = CitationSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (POSTOnlyAuthentication,)
    user_serializer = UserSerializer

    @detail_route(methods=['get'])
    def comment(self, request, format=None):
        if request.method == 'GET':
            citation = self.get_object()
            return Response(citation)

    @list_route(methods=['post'])
    def create_citation(self, request, format=None, *args, **kwargs):
        user = request.user
        fact = request.data['fact_id']
        if not fact:
            return (Response('Fact is not provided'))

        fact = Fact.objects.get(pk=fact)
        text = request.data['text']
        url = request.data['url']
        approval = True
        if 'approval' not in request.data:
            approval = False

        if user and text and type(approval) == bool:
            citation = Citation(fact_id=fact, text=text,
                                url=url, user=user,
                                approval=approval)
            citation.save()
            return(Response('Citation added'))
        else:
            return(Response('Not provided all fields'))

    @detail_route(methods=['post'])
    def upvote(self, request, format=None, *args, **kwargs):
        user = request.user
        citation = self.get_object()
        if not Citation.objects.filter(upvoted_by=user):
            citation.upvoted = citation.upvoted + 1
            citation.upvoted_by.add(user)
            citation.save()
            return Response('Upvoted')
        else:
            return Response('You have already voted')

    @detail_route(methods=['post'])
    def downvote(self, request, format=None, *args, **kwargs):
        user = request.user
        citation = self.get_object()
        if not Citation.objects.filter(upvoted_by=user):
            citation.downvoted = citation.downvoted + 1
            citation.downvoted_by.add(user)
            citation.save()
            return Response('Downvoted')
        else:
            return Response('You have already voted')

    @detail_route(methods=['post'])
    def report(self, request, format=None, *args, **kwargs):
        user = request.user
        citation = self.get_object()
        if not Citation.objects.filter(reported_by=user):
            citation.reported_by.add(user)
            citation.save()
            return Response('Reported')
        else:
            return Response('You have reported this comment')


class ClusterApiViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return ClusterSerializerShort
        return ClusterSerializer

    queryset = Cluster.objects.all()
    # serializer_class = ClusterSerializerShort
    lookup_field = 'cluster_name'

    @detail_route()
    def cluster(self, request, pk, *args, **kwargs):
        self.serializer_class = ClusterSerializer
        cluster = self.get_object()
        return Response(cluster)
    @detail_route()
    def combined_view(self, request, *args, **kwargs):
        pk = kwargs['cluster_name']
        if pk == "Science_&_technology":
            clusters = ['technology', 'nature', 'cars']
        elif pk == 'Global':
            clusters = ['global', 'USA', "UK", "EU", 'Asia', 'Africa',
                        'Australia', 'Latin', 'NZ', 'Ireland', 'Canada',
                        'weather', 'disasters', 'crime', 'accidents']
        elif pk == 'Sports':
            clusters = ['sports', ]
        elif pk == 'Politics':
            clusters = ['politics', 'education', 'war', 'finance']
        elif pk == 'Business':
            clusters = ['business', 'finance']
        elif pk == 'Health':
            clusters = ['health', ]
        elif pk == 'Society':
            clusters = ['society', 'culture', 'travel', 'food']
        elif pk == 'Entertainment':
            clusters = ['music', 'videogames', 'TV', 'movies', 'festivals',
                        'entertainment']
        queryset = Article.objects.filter(
            article_cluster__cluster_name__in=clusters)
        serializer = ArticleSerializerShort(queryset, many=True)
        # lol = serializers.serialize("json", queryset)
        return Response(serializer.data)
    @list_route()
    def combined(self, request, *args, **kwargs):
        clusters = ['Global', 'Politics', 'Business', 'Health', 'Society',
                    'Entertainment', 'Sport', 'Travel',
                    'Science_&_technology']
        cl_numbers = [i for i in range(len(clusters))]
        output = {"count": len(clusters),
                  "results": [{"cluster_id": i,
                               "cluster_name": clusters[i]}
                              for i in cl_numbers]}
        return Response(output)


class CitationCommentApiViewSet(viewsets.ModelViewSet):
    queryset = CitationComment.objects.all()
    serializer_class = CitationCommentSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (POSTOnlyAuthentication,)
    user_serializer = UserSerializer

    @detail_route(methods=['get'])
    def comment(self, request, format=None):
        if request.method == 'GET':
            comment = self.get_object()
            return Response(comment)

    @list_route(methods=['post'])
    def create_comment(self, request, format=None, *args, **kwargs):
        user = request.user
        citation = request.data['citation_id']
        citation = Citation.objects.get(id=citation)

        recipient = None
        if request.data['recipient']:
            recipient = request.data['recipient']
            recipient = MyUser.objects.get(id=recipient)
        if user:
            comment = CitationComment(citation_id=citation,
                                      title=request.data['title'],
                                      text=request.data['text'], user=user,
                                      recipient=recipient)
            comment.save()
        return(Response('Comment added'))

    @detail_route(methods=['post'])
    def upvote(self, request, format=None, *args, **kwargs):
        user = request.user
        comment = self.get_object()
        if not CitationComment.objects.filter(upvoted_by=user):
            comment.upvoted = comment.upvoted + 1
            comment.upvoted_by.add(user)
            comment.save()
            return Response('Upvoted')
        else:
            return Response('You have already voted')

    @detail_route(methods=['post'])
    def downvote(self, request, format=None, *args, **kwargs):
        user = request.user
        comment = self.get_object()
        if not CitationComment.objects.filter(upvoted_by=user):
            comment.downvoted = comment.downvoted + 1
            comment.downvoted_by.add(user)
            comment.save()
            return Response('Downvoted')
        else:
            return Response('You have already voted')


class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['get'])
    def user(self, request, format=None):
        if request.method == 'GET':
            user = self.get_object()
            return Response(user)