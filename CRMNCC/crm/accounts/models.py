from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class thejobtitle(models.Model):

    jobtitle_name = models.CharField("Project Name",max_length=100,unique=True)

    def __str__(self):
        return str(self.jobtitle_name)






class Profile(models.Model):
    Region_CHOICES = [
                ('Central', 'Central'),
                ('Western', 'Western'),
                ('Eastern', 'Eastern'),

            ]


    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    phone = models.CharField("Phon No",max_length=100,null=True)
    jobtitle = models.CharField("Job Title",max_length=100,null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True,null=True)
    role = models.CharField("Role",max_length=200,null=True)
    supervisor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_supervisor',null=True)
    jobtitle_detail = models.ForeignKey(thejobtitle,on_delete=models.CASCADE,related_name='jobtitle_profile',null=True)
    region = models.CharField("Region",max_length=20,null=True,choices=Region_CHOICES)


    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
