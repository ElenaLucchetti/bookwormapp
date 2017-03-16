from django.db import models

class Book (models.Model):
	title = models.CharField(max_length=128, unique=True)
	isbn = models.IntegerField()
	authors = models.ManyToManyField(Author)
	genre = models.ForeignKey(Genre)
    releaseDate = models.DateField()
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(blank=True)
    slug = models.SlugField(unique = True)
	
class Author (models.Model):
	name = models.CharField(max_length = 50)

class Genre (models.Model):
	name = models.CharField(max_length = 50)
	
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username