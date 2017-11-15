from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Cluster(models.Model):
    cluster_id = models.AutoField(primary_key=True)
    cluster_name = models.CharField(max_length=200)

    def __str__(self):
        return self.cluster_name


class Interest(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    clusters = models.ManyToManyField(Cluster,
                                      related_name='user_cluster')
    interests = models.ManyToManyField(Interest,
                                       related_name='user_interest')
    avatar = models.ImageField(blank=True, null=True)


class Story(models.Model):
    story_id = models.AutoField(primary_key=True)
    story_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    rating_users = models.IntegerField(blank=True, null=True)
    rating_subjectivity = models.IntegerField(blank=True, null=True)
    hotness = models.IntegerField(default=0)
    keywords = TaggableManager()
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    story_cluster = models.ForeignKey(Cluster, blank=True,
                                      null=True, related_name='story_cluster')

    def __str__(self):
        return self.story_name

    class Meta:
        ordering = [u'-date', u'-hotness']


class Party(models.Model):
    name = models.TextField(max_length=100)
    country = models.TextField(max_length=100, blank=True)
    subjectivity = models.IntegerField()
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.TextField(max_length=100)
    url = models.URLField(max_length=500)
    country = models.TextField(max_length=100)
    source_subjectivity = models.IntegerField(blank=True, null=True)
    affiliations = models.ManyToManyField(Party, blank=True,
                                          related_name='affiliation')
    bias = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    story_id = models.ForeignKey(Story, blank=True,
                                 null=True, related_name='articles')
    title = models.CharField(max_length=200, null=True)
    authors = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    url = models.URLField(max_length=500)
    videos = models.URLField(blank=True, null=True)
    summary = models.CharField(max_length=5000)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    keywords = TaggableManager()
    subjectivity = models.IntegerField(blank=True, null=True)
    hotness = models.IntegerField(blank=True, null=True, default=0)
    spelling = models.IntegerField(blank=True, null=True)
    grammar = models.IntegerField(blank=True, null=True)
    party_id = models.ForeignKey(Party, blank=True, null=True)
    party_subjectivity_article = models.IntegerField(blank=True, null=True)
    source_id = models.ForeignKey(Source)
    article_cluster = models.ForeignKey(Cluster, blank=True,
                                        null=True,
                                        related_name='article_cluster')
    wrong_cluster = models.ManyToManyField(MyUser,
                                           related_name='wrong_cluster')
    wrong_story = models.ManyToManyField(MyUser,
                                         related_name='wrong_story')

    def __str__(self):
        return self.title

    class Meta:
        ordering = [u'-pub_date']


class Fact(models.Model):
    article = models.ForeignKey(Article, related_name='fact_article')
    sentence_id = models.IntegerField()
    text = models.CharField(max_length=5000, null=True)
    upvoted = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(MyUser, related_name='fact_upv_by')
    downvoted = models.IntegerField(default=0)
    downvoted_by = models.ManyToManyField(MyUser, related_name='fact_downv_by')
    user = models.ForeignKey(MyUser, related_name='fact_user', null=True,
                             blank=True)
    'fact="{}" sent_id="{}"'
    def __str__(self):
        return self.text

    def upvote(self):
        self.upvoted += 1

    def downvote(self):
        self.downvoted += 1

    class Meta:
        ordering = [u'id']


class Comment(models.Model):
    article_id = models.ForeignKey(Article, blank=True,
                                   null=True, related_name='comm_article')
    title = models.CharField(max_length=200, null=True)
    text = models.TextField()
    user = models.ForeignKey(MyUser, related_name='comm_user')
    recipient = models.ForeignKey(MyUser, null=True, blank=True,
                                  related_name='comm_recipient')
    pub_date = models.DateTimeField(auto_now_add=True)
    upvoted = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(MyUser, related_name='com_upv_by')
    downvoted = models.IntegerField(default=0)
    downvoted_by = models.ManyToManyField(MyUser, related_name='com_downv_by')
    reported_by = models.ManyToManyField(MyUser, related_name='com_report_by')

    def __str__(self):
        return self.text


class Citation(models.Model):
    fact_id = models.ForeignKey(Fact, blank=True,
                                null=True, related_name='cit_fact')
    text = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(MyUser, related_name='cit_user')
    pub_date = models.DateTimeField(auto_now_add=True)
    upvoted = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(MyUser, related_name='cit_upv_by')
    downvoted = models.IntegerField(default=0)
    downvoted_by = models.ManyToManyField(MyUser, related_name='cit_downv_by')
    approval = models.BooleanField(default=True)
    reported_by = models.ManyToManyField(MyUser, related_name='cit_report_by')

    def __str__(self):
        return self.text


class CitationComment(models.Model):
    citation_id = models.ForeignKey(Citation, blank=True,
                                    null=True, related_name='comm_citation')
    title = models.CharField(max_length=200, null=True)
    text = models.TextField()
    user = models.ForeignKey(MyUser, related_name='cit_comm_user')
    recipient = models.ForeignKey(MyUser, null=True, blank=True,
                                  related_name='cit_comm_recipient')
    pub_date = models.DateTimeField(auto_now_add=True)
    upvoted = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(MyUser, related_name='cit_com_upv_by')
    downvoted = models.IntegerField(default=0)
    downvoted_by = models.ManyToManyField(MyUser,
                                          related_name='cit_com_downv_by')

    def __str__(self):
        return self.text
