from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver
from .models import Profile

@receiver(social_account_added)
@receiver(social_account_updated)
def populate_profile_from_social_account(request, sociallogin, **kwargs):
    user = sociallogin.user

    # Créer ou récupérer le profil
    profile, created = Profile.objects.get_or_create(user=user)

    # Mettre à jour la photo depuis le compte Google
    avatar_url = sociallogin.account.get_avatar_url()
    if avatar_url:
        profile.photo = avatar_url
        profile.save()
