from django.db import models

class CompanyHealthScore(models.Model):
    company_id = models.CharField(primary_key=True, max_length=50)
    company_name = models.TextField()
    sector = models.TextField(null=True)
    health_score = models.FloatField(null=True)
    health_label = models.TextField(null=True)

    class Meta:
        db_table = 'company_health_scores'
        managed = False