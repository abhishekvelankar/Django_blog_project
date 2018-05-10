from django.db import models
from django.utils import timezone
#reverse is added to redirect user to some page after posting a blog or a comment.
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    #connect author to each user
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True,null=True)
    #if published date is not set by user then it will be automatically set to default current date
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    #after hitting post go to that post detail page where the primary key of that post you just created
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    #connects each comment to its post
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete = models.CASCADE)
    author = models.CharField(max_length=250)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    #after commenting on the post go back to the list of comments of the original post
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
