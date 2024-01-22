from django.db import models

class JWTToken(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=500, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.token