#!/usr/bin/env python
from django.db import models
from django.contrib.auth.models import User
from ask_panichkina import settings

import os
import sys


uploads = "avatars"

class Tag(models.Model):
    text = models.CharField(max_length=15)
    def __unicode__(self):
        return self.text

class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=60)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    likes_num = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title

class Answer(models.Model):
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes_num = models.IntegerField(default=0)
    is_right = models.BooleanField(default=False)
    def __unicode__(self):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=uploads, default="/avatar.jpg")



class Rate_question(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)


class Rate_answer(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)


class Rate_profile(models.Model):
    user = models.ForeignKey(User)
    profile = models.ForeignKey(Profile)