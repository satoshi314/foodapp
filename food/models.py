from django.db import models
from django.contrib.auth.models import User


class State(models.Model):
    message  =   models.CharField(max_length=30)
    #imageField だとmedia ROOT が強制的に結合されるため、パスで保存する
    #symbol =   models.ImageField(blank=True,upload_to='system')  
    symbol =   models.CharField(max_length=100)
    def __str__(self):
        return self.message    #���̋L�q��邱�ƂŃI�u�W�F�N�g�̌Ăі����w�肵���v�f�ɂȂ�
    
class Shop(models.Model):    
    name = models.CharField(max_length=30)
    #evaluate = models.FloatField(blank=True)
    evaluate = models.FloatField(null=True) #数値型はblankではなくnull。（数値が入っていないときは自動的にnullに。文字列の場合は空白に 
    station = models.CharField(max_length=30,blank=True)
    genre = models.CharField(max_length=30,blank=True)
    kuchikomi = models.IntegerField(null=True)  #口コミの件数
    teikyu = models.CharField(max_length=20,blank=True)
    lunch_bud = models.CharField(max_length=20,blank=True)
    dinner_bud = models.CharField(max_length=20,blank=True)
    url = models.CharField(max_length=200,blank=True)
    comment = models.CharField(max_length=300,blank=True)
    #画像のアップロードはAWSなどと連携しないと不可なので一旦あきらめる
    #photo =models.ImageField(blank=True,upload_to='photos')
    # photo_binary=models.BinaryField(blank=True) #本番環境で動作させるために画像をバイナリとしてDBで保持
    coordinate = models.CharField(max_length=30,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name


