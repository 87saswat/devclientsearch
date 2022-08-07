

from multiprocessing.sharedctypes import Value
from pyexpat import model
from django.db import models
import uuid

from users.models import Profile

# Create your models here.


class Projects(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    demmo_link = models.CharField(max_length=1000, blank=True, null=True)
    source_link = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def reviewers(self):
        # getting all the reviewers and their id through owner__id (owner-->Profile-->id), value_list..flat=true(will convert it to a True list) means it is a list of values instead of object
        queryset = self.review_set.all().value_list(
            'owner__id', flat=True)  # it gives us the id of all the reviewer
        return queryset

    @property
    def getVotecount(self):
        reviews = self.review_set.all()
        up_vote = reviews.filter(value='up').count()
        # down_vote = reviews.filter(value='down').count()
        total_vote = reviews.count()
        ratio = (up_vote/total_vote) * 100

        self.vote_total = total_vote  # update the vote_total and vote_ration
        self.vote_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')

    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        # owner and project have to be unique. no owner can add more than one review in a project i.e. an owner can only add ne review on a project
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
