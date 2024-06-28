from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.forms import UserUpdateForm, ProfileUpdateForm
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max, Count
from elections.models import Election, Candidate, Vote


@login_required()
def dashboard(request):
    if (request.user.is_staff):
        return redirect('admin-dashboard')

    ongoing_elections = Election.objects.filter(is_active=True, start_date__lte=timezone.now())
    ongoing_elections = sorted(ongoing_elections, key=lambda x: x.start_date, reverse=True)

    candidates_with_votes = Candidate.objects.filter(election__in=ongoing_elections).annotate(total_votes=Count('vote'))
    top_candidates = []

    for election in ongoing_elections:
        top_candidate = candidates_with_votes.filter(election=election).order_by('-total_votes').first()
        # top_candidate = candidates.annotate(max_votes=Max('vote__votes')).order_by('-max_votes').first()
        if top_candidate:
            top_candidate_votes = Vote.objects.filter(candidate=top_candidate).count()
            top_candidate.total_votes = top_candidate_votes
            top_candidates.append(top_candidate)

    context = {
        'page_title': 'Dashboard',
        'ongoing_elections': ongoing_elections,
        'top_candidates': top_candidates,
        }
    return render(request, 'dashboard/dashboard.html', context=context)

@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'page_title': 'Profile', 
        'u_form': u_form, 
        'p_form': p_form
    }
    return render(request, 'dashboard/profile.html', context=context)