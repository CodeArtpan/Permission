from django.db import models

class User(models.Model):
    '''
    用户表
    '''
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.username

class Role(models.Model):
    '''
    角色表
    '''
    name = models.CharField(max_length=32)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name

class Permission(models.Model):
    '''
    权限表
    '''
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    menu = models.ForeignKey('Menu',null=True,blank=True)

    def __str__(self):
        return self.title

class Menu(models.Model):
    '''
    菜单表
    '''
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self',null=True,blank=True)

    def __str__(self):
        caption_list = [self.caption,]
        p = self.parent
        while p:
            caption_list.insert(0,p.caption)
            p = p.parent
        return '----'.join(caption_list)