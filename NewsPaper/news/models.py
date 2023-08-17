from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
#from datetime import datetime
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_post_raiting = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']*3
        author_comment_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        under_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']

        self.rating = author_post_raiting + author_comment_rating + under_post_comment_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=80, unique=True)

    def __str__(self) -> str:
        return self.category_name
    

class Post(models.Model):
    ARTICLES = 'AT'
    NEWS = 'NW'
    post_type_list = [
        (ARTICLES, 'Статья'), 
        (NEWS, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length = 2, choices = post_type_list, default = NEWS)
    create_time = models.DateTimeField(auto_now_add = True)
    post_title = models.CharField(max_length=80)
    post_text = models.TextField(default='место для вашей рекламы')
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.post_text) < 124:
            return self.post_text
        else:
            return self.post_text[:124] + '...'

   
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default='место для вашей рекламы')
    create_time = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()