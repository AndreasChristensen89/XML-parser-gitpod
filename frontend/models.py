from django.db import models


class Samples(models.Model):
    """
    Model to keep records of samples
    """
    
    sample_uid = models.CharField(max_length=50, default="")
    sample_name = models.CharField(max_length=50, default="")


class Publications(models.Model):
    """
    Model to keep records of publications
    """

    publications_uid = models.CharField(max_length=50, default="")
    publication_title = models.CharField(max_length=50, default="")
