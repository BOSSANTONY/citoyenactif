from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from .models import Signalement, Profile
from .forms import SignalementForm, RegisterForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

@user_passes_test(lambda u: u.is_authenticated and u.is_superuser)
@require_POST
def supprimer_utilisateur(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, "Utilisateur supprimé.")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
    return redirect('dashboard')


@login_required
def supprimer_signalement(request, signalement_id):
    signalement = get_object_or_404(Signalement, id=signalement_id)

    # Vérifie si l’utilisateur est propriétaire OU admin
    if signalement.profil.user == request.user or request.user.is_superuser:
        signalement.delete()
        messages.success(request, "Signalement supprimé avec succès.")
    else:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce signalement.")

    return redirect('mes_signalements')  # Redirige vers les signalements perso

def login_view(request):
    photo_url = None

    if request.user.is_authenticated:
        return redirect('home')  # Empêche un utilisateur connecté d'aller à la page login

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    # Ne PAS charger d'utilisateur ou de photo si personne n’est connecté
    return render(request, "login.html", {
        "photo_url": photo_url,
    })




def logout_view(request):
    logout(request)
    return redirect("home")


from django.contrib.auth.models import User
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            role = form.cleaned_data['role']

            # Vérifier s'il existe déjà un admin
            if role == 'admin':
                existing_admin = Profile.objects.filter(role='admin').exists()
                if existing_admin:
                    messages.error(request, "Un administrateur existe déjà. Impossible d'en créer un autre.")
                    return render(request, 'register.html', {'form': form})

            # Création du compte utilisateur
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user.set_password(password)  # Hash du mot de passe

            if role in ['admin', 'agent']:
                user.is_staff = True

            user.save()

            # Création du profil
            photo = form.cleaned_data['photo']
            Profile.objects.create(user=user, photo=photo, role=role)

            # Authentification et connexion
            user_auth = authenticate(username=user.username, password=password)
            if user_auth:
                login(request, user_auth)
                messages.success(request, "Inscription réussie !")
                return redirect('login')
            else:
                messages.error(request, "Erreur lors de l'authentification automatique.")
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def signalement_create(request):
    if request.method == 'POST':
        form = SignalementForm(request.POST, request.FILES)
        if form.is_valid():
            signalement = form.save(commit=False)
            signalement.profil = request.user.profile
            signalement.save()
            return redirect('mes_signalements')  # ✅ C’est le nom correct défini dans urls.py
    else:
        form = SignalementForm()
    return render(request, 'signalements/form_signalement.html', {'form': form})


@login_required
def carte(request):
    signalements = Signalement.objects.all()
    return render(request, 'signalements/carte.html', {"signalements": signalements})

@login_required
@user_passes_test(lambda u: u.profile.role == "utilisateur")
def ma_carte(request):
    signalements = Signalement.objects.filter(profil__user=request.user)
    context = {
        'signalements': signalements,
        'google_maps_api_key': 'AIzaSyBYKtlqDygyn8Vg0ehWdzdoZdsyer3Czls',
    }
    return render(request, 'signalements/ma_carte.html', context)


@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def carte_utilisateur(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        signalements = Signalement.objects.filter(profil__user=user)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('dashboard')

    context = {
        'utilisateur': user,
        'signalements': signalements,
        'google_maps_api_key': 'AIzaSyBYKtlqDygyn8Vg0ehWdzdoZdsyer3Czls',
    }
    return render(request, 'signalements/carte_utilisateur.html', context)


# 🌍 Accueil
def home(request):
    context = {}
    if request.user.is_authenticated:
        # Crée le profil s’il n’existe pas
        profile, created = Profile.objects.get_or_create(user=request.user)
        context['profile'] = profile
    return render(request, 'signalements/home.html', context)



# ➕ Créer un nouveau signalement
@login_required
def signalement_nouveau(request):
    if request.method == 'POST':
        form = SignalementForm(request.POST, request.FILES)
        if form.is_valid():
            signalement = form.save(commit=False)
            signalement.utilisateur = request.user
            signalement.save()
            messages.success(request, "Merci ! Votre signalement a bien été enregistré.")
            return redirect('mes_signalements')
    else:
        form = SignalementForm()
    return render(request, 'signalements/form_signalement.html', {'form': form})

# 📋 Liste des signalements personnels
@login_required
def mes_signalements(request):
    signalements=Signalement.objects.filter(profil__user=request.user)
    return render(request, 'signalements/mes_signalements.html', {'signalements': signalements})

# 📍 Carte interactive (vue avec tous les signalements)
def carte(request):
    signalements = Signalement.objects.all()
    context = {
        'signalements': signalements,
        'google_maps_api_key': 'AIzaSyBYKtlqDygyn8Vg0ehWdzdoZdsyer3Czls',  # ta clé Google Maps ici
    }
    return render(request, 'signalements/carte.html', context)


@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def dashboard(request):
    total = Signalement.objects.count()
    resolus = Signalement.objects.filter(statut='resolu').count()
    en_cours = Signalement.objects.filter(statut='en_cours').count()
    par_categorie = Signalement.objects.values('categorie').annotate(count=Count('id'))

    users = User.objects.all().select_related('profile')
    agents = User.objects.filter(profile__role='agent')

    return render(request, 'signalements/dashboard.html', {
        'total': total,
        'resolus': resolus,
        'en_cours': en_cours,
        'par_categorie': par_categorie,
        'users': users,
        'agents': agents,
        'now': timezone.now(),
    })