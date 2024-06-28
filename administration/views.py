from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from elections.models import Election, Candidate, Vote, Result
from django.contrib.auth.models import User
from .forms import ElectionCreateForm, ElectionUpdateForm, CandidateCreateForm


@staff_member_required()
def dashboard(request):
    total_elections = Election.objects.count()
    active_elections = Election.objects.filter(is_active=True)
    past_elections = Election.objects.filter(is_active=False)
    candidates = Candidate.objects.filter(election__is_active=True)
    candidates_running = Candidate.objects.filter(election__is_active=True)
    voters = User.objects.exclude(pk=request.user.pk)
    admins = User.objects.filter(is_staff=True).count()

    # barchart
    election_titles =[]
    candidate_count = []
    for election in active_elections:
        election_titles.append(election.title)
        candidate_count.append(Candidate.objects.filter(election=election).count())

    # doughnut chart
    male_candidates = Candidate.objects.filter(gender='male').count()
    female_candidates = Candidate.objects.filter(gender='female').count()

    context = {
        'page_title': 'Admin Dashboard',
        'total_elections': total_elections,
        'active_elections': active_elections,
        'past_elections': past_elections,
        'candidates': candidates,
        'candidates_running': candidates_running,
        'voters': voters,
        'admins': admins,
        # bar chart
        'election_titles': election_titles,
        'candidate_count': candidate_count,
        # doughnut chart
        'male_candidates': male_candidates,
        'female_candidates': female_candidates,
    }
    return render(request, 'administration/admin-dashboard.html', context=context)


# ELECTIONS

@staff_member_required()
def elections(request):
    elections = Election.objects.all()

    context = {
        'page_title': 'Elections',
        'elections': elections,
    }
    return render(request, 'administration/elections/admin-elections.html', context=context)


@staff_member_required()
def election_form(request):
    if request.method == "POST":
        form = ElectionCreateForm(request.POST, request.FILES)
        if form.is_valid():
            election = form.save()
            messages.success(request, 'Election created successfully')
            return redirect('election_detail', pk=election.pk)
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = ElectionCreateForm()

    context = {
        'page_title': 'Create Election',
        'form': form,
    }
    return render(request, 'administration/elections/election-form.html', context=context)


@staff_member_required()
def confirm_election_delete(request, pk):
    election = Election.objects.get(pk=pk)
    if request.method == "POST":
        election.delete()
        messages.success(request, 'Election deleted successfully')
        return redirect('admin-elections')

    context = {
        'page_title': 'Delete Election',
        'election': election,
    }
    return render(request, 'administration/elections/confirm_election_delete.html', context=context)


@staff_member_required()
def election_update_form(request, pk):
    election = Election.objects.get(pk=pk)
    if request.method == "POST":
        form = ElectionUpdateForm(request.POST, request.FILES, instance=election)
        if form.is_valid():
            election = form.save()
            messages.success(request, 'Election updated successfully')
            return redirect('election_update_form', pk=election.pk)
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = ElectionUpdateForm(instance=election)

    context = {
        'page_title': 'Edit Election',
        'form': form,
        'election': election,
    }
    return render(request, 'administration/elections/election_update_form.html', context=context)


# CANDIDATES

@staff_member_required()
def candidates(request):
    candidates = Candidate.objects.all()

    context = {
        'page_title': 'Candidates',
        'candidates': candidates,
    }
    return render(request, 'administration/candidates/admin_candidates.html', context=context)


@staff_member_required()
def candidate_form(request):
    if request.method == "POST":
        form = CandidateCreateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, 'Candidate created successfully')
            return redirect('candidate_detail', pk=candidate.pk)
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = CandidateCreateForm()

    context = {
        'page_title': 'Create Candidate',
        'form': form,
    }
    return render(request, 'administration/candidates/candidate_form.html', context=context)


@staff_member_required()
def confirm_candidate_delete(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    if request.method == "POST":
        candidate.delete()
        messages.success(request, 'Candidate deleted successfully')
        return redirect('admin_candidates')

    context = {
        'page_title': 'Delete Candidate',
        'candidate': candidate,
    }
    return render(request, 'administration/candidates/confirm_candidate_delete.html', context=context)


@staff_member_required()
def candidate_update_form(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    if request.method == "POST":
        form = CandidateCreateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, 'Candidate updated successfully')
            return redirect('candidate_update_form', pk=candidate.pk)
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = CandidateCreateForm(instance=candidate)

    context = {
        'page_title': 'Edit Candidate',
        'form': form,
        'candidate': candidate,
    }
    return render(request, 'administration/candidates/candidate_update_form.html', context=context)


# VOTERS

@staff_member_required()
def voters(request):
    voters = User.objects.exclude(pk=request.user.pk)

    context= {
        'page_title': 'Voters',
        'voters': voters,
    }
    return render(request, 'administration/voters/admin_voters.html', context=context)


@staff_member_required()
def confirm_voter_delete(request, pk):
    voter = User.objects.get(pk=pk)
    if request.method == "POST":
        voter.delete()
        messages.success(request, 'Voter deleted successfully')
        return redirect('admin_voters')

    context = {
        'page_title': 'Delete Voter',
        'voter': voter,
    }
    return render(request, 'administration/voters/confirm_voter_delete.html', context=context)


# RESULTS

@staff_member_required()
def results(request):
    results = Result.objects.all()
    active_elections = Election.objects.filter(is_active=True, end_date__gte=timezone.now())
    active_elections = active_elections.exclude(id__in=[result.election.id for result in results])

    top_candidates = []
    candidates_with_votes = Candidate.objects.filter(election__in=active_elections).annotate(total_votes=Count('vote'))
    for election in active_elections:
        top_candidate = candidates_with_votes.filter(election=election).order_by('-total_votes').first()
        if top_candidate:
            top_candidate_votes = Vote.objects.filter(candidate=top_candidate).count()
            top_candidate.total_votes = top_candidate_votes
            top_candidates.append(top_candidate)


    context = {
        'page_title': 'Results',
        'results': results,
        'active_elections': active_elections,
        'top_candidates': top_candidates,
    }
    return render(request, 'administration/results/admin_results.html', context=context)


@staff_member_required()
def confirm_result(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    votes = Vote.objects.filter(candidate=candidate).count()

    Result.objects.create(election=candidate.election, candidate=candidate, votes=votes)
    election = Election.objects.get(pk=candidate.election.pk)
    election.is_active = False
    election.save()
    messages.success(request, f"{candidate.name} has been confirmed as the winner with {votes} votes")

    return redirect('admin_results')


@staff_member_required()
def result_update_form(request):
    pass