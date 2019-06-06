from django.db import models

# Create your models here.


class Score(models.Model):
    score = models.CharField(max_length=3)
    score_owner = models.CharField(max_length=128)
    score_checker = models.CharField(max_length=128)
    score_attribution = models.CharField(max_length=255)
    score_fp = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "实验章节：%s  |  得分：%s" % (self.score_attribution, self.score)
