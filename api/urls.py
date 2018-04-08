from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from allauth.account.views import confirm_email
from . import views


class Router(routers.DefaultRouter):
    def get_api_root_view(self, api_urls=None, html=True):
        root_view = super(Router, self).get_api_root_view(api_urls=api_urls)
        root_view.cls.__doc__ = '''
[Registration](/api/auth/registration/)

[Login](/api/auth/login/)

[Login with Facebook](/api/auth/facebook/)

    From StackOverFlow:
    Only one of "Access Token" or "Code" field is required.
    (I have not tested the Code field but the Access Token field works,
    with the Code field left blank)

    To use Access Token, after the user performs the "Login to Facebook"
    step on the client side using Facebook javascript SDK, you will receive
    a response from Facebook
    which includes "accessToken" for accessing data on Facebook.
    Simply paste this accessToken into the "Access Token" field and
    it will automatically login and/or create the user's account from data
    retrieved from Facebook.

    Obviously you can then perform the same process by posting the access
    token to the form all in javascript.

[Login with Twitter](/api/auth/twitter/)

[Password reset](/api/auth/password/reset/)

[Password reset Confirm](/api/auth/password/reset/confirm/)

[Logout](/api/auth/logout/)

[User Details](/api/auth/user/)

[Password Change](/api/auth/password/change)

    Articles, Stories and all other models below accept ids of their models
    (article_id for articles, story_id for stories, id for facts)
    and links should look like
[/api/articles/1800](/api/articles/1800)

    comm_article Gives all comments for this article
    fact_article Gives all facts for this article

[*/api/stories/1800](/api/stories/1800)

[*/api/facts/1](/api/facts/1)

    Keywords accept \*keyword\* as an argument
[*/api/keywords/uk](/api/keywords/uk)

    Facts are upvoted with POST
[*/api/facts/1/upvote](/api/facts/1/upvote)

    and downvoted with POST
[*/api/facts/1/downvote](/api/facts/1/downvote)
    create a fact
[*/api/facts/create_fact/](/api/facts/create_fact/)
    To create a comment with POST
[*/api/comments/create_comment](/api/comments/create_comment)

    To upvote a comment with POST
[*/api/comments/1/upvote](/api/comments/1/upvote)

    and downvote it with POST</br>
[*/api/comments/1/downvote](/api/comments/1/downvote)

    To report a comment with POST
[*/api/comments/1/report](/api/comments/1/report)


    To create a citations with POST
[*/api/citations/create_citation](/api/citations/create_citation)

    To upvote a citation with POST
[*/api/citations/1/upvote](/api/citations/1/upvote)

    and downvote it with POST
[*/api/citations/1/downvote](/api/citations/1/downvote)

    To report a citation with POST
[*/api/citation/1/report](/api/citation/1/report)

    All topics (clusters) are in
[*/api/clusters](/api/clusters/)

    A call to a particular cluster will retrieve the list of all stories on
    this topic

[*/api/clusters/uk/](/api/clusters/uk)
'''
        return root_view


router = Router('{api}')

router.register(r'articles', views.ArticleApiViewSet, 'articles')
router.register(r'stories', views.StoryApiViewSet, 'stories')
router.register(r'keywords', views.KeywordViewSet, 'keywords')
router.register(r'facts', views.FactApiViewSet, 'facts')
router.register(r'comments', views.CommentApiViewSet, 'comments')
router.register(r'citations', views.CitationApiViewSet, 'citations')
router.register(r'citation_comments', views.CitationCommentApiViewSet,
                'citation_comments')
router.register(r'clusters', views.ClusterApiViewSet, 'clusters')
router.register(r'accounts', views.UserApiViewSet, 'users')


# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        confirm_email, name="account_confirm_email"),
    url(r'^articles.json$', views.ArticlesView.as_view(),
        name='articles-json'),
    url(r'^articles/(?P<pk>\d+).json$', views.ArticleDetailedView.as_view(),
        name='articles-detailed-json'),
    url(r'^stories/(?P<pk>\d+).json$', views.StoryDetailedView.as_view(),
        name='stories-detailed-json'),
    url(r'^stories.json$', views.StoriesView.as_view(), name='stories-json'),
    url(r'^$', views.StoriesView.as_view(), name='stories-redirect'),
    url(r'^keywords/(?P<slug>.+?).json$', views.KeywordView.as_view(),
        name='keywords-json'),
    url(r'^topic/(?P<slug>.+?)$', views.TopicView.as_view(),
        name='topics'),


    url(r'^keywords/(?P<slug>.+?)$', views.KeywordView.as_view(),
        name='keywords'),
    url(r'^stories$', views.StoriesView.as_view(), name='stories'),
    url(r'^articles$', views.ArticlesView.as_view(), name='articles'),
    url(r'^articles/(?P<pk>\d+)$', views.ArticleDetailedView.as_view(),
        name='articles-detailed'),
    url(r'^stories/(?P<pk>\d+)$', views.StoryDetailedView.as_view(),
        name='stories-detailed'),
    url(r'^rest-auth/registration/account-email-verification-sent/',
        views.null_view, name='account_email_verification_sent'),
    url(r'^rest-auth/registration/account-confirm-email/',
        views.null_view, name='account_confirm_email'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.null_view, name='password_reset_confirm'),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),

    url(r'^api/auth/password/reset/confirm/(?P<uid>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.null_view, name='password_reset_confirm'),

    url(r'^api/auth/', include('rest_auth.urls')),

    url(r'^api/auth/facebook/$', views.FacebookLogin.as_view(),
        name='fb_login'),
    url(r'^api/auth/twitter/$', views.TwitterLogin.as_view(),
        name='twitter_login')
    # url(r'^api/auth/', include('rest_framework_social_oauth2.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
