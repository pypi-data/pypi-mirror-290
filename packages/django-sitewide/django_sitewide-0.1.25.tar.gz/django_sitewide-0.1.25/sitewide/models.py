from django.db import models

# Create your models here.


class Phrase(models.Model):
    """Terminology used by a certain Group"""

    group = models.CharField(max_length=255)
    phrase = models.CharField(max_length=255)
    rephrase = models.CharField(max_length=255)

    def __str__(self):
        """Return the Rephrased version of Phrase as per specified Group"""

        return self.rephrase

    class Meta:
        """Meta for the Modes of Entry"""

        managed = True
        db_table = "phrase"
        constraints = [
            models.UniqueConstraint(fields=["group", "phrase"], name="unique_phrase"),
        ]
