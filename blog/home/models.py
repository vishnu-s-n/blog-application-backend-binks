from django.db import models
from django.contrib.auth.models import User



class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="blog")
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to="blogs")
    likes = models.IntegerField(default=0)

    def __str__(self) :
        return self.title
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blogs")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bloguser")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="userblog")
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)