from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Count
from .models import Election, Candidate, Vote, Result

@login_required()
def home(request):
    active_elections = Election.objects.filter(is_active=True)
    past_elections = Election.objects.filter(is_active=False)

    context = {
        'page_title': 'Elections', 
        'active_elections': active_elections,
        'past_elections': past_elections,
    }
    return render(request, 'elections/elections.html', context=context)


@login_required()
def election_detail(request, pk):
    election = Election.objects.get(pk=pk)
    candidates = Candidate.objects.filter(election=election)
    total_votes = Vote.objects.filter(election=election).count()
    result = Result.objects.filter(election=election)
    voted = Vote.objects.filter(election=election, voter=request.user).exists()
    election_active = election.is_active and election.end_date > timezone.now()
    
    winner_id = 0
    if result:
        winner_id = result[0].candidate.id


    context = {
        'page_title': election.title,
        'election': election,
        'candidates': candidates,
        'total_votes:': total_votes,
        'results': result,
        'voted': voted,
        'election_active': election_active,
        'winner_id': winner_id
    }
    return render(request, 'elections/election_detail.html', context=context)


@login_required()
def candidates(request):
    candidates = Candidate.objects.all()

    final_candidates = []
    for candidate in candidates:
        candidate.votes = Vote.objects.filter(candidate=candidate).count()
        final_candidates.append(candidate)

    context = {
        'page_title': 'Candidates',
        'candidates': final_candidates,
    }
    return render(request, 'elections/candidates/candidates.html', context=context)


@login_required()
def election_candidates(request, pk):
    election = Election.objects.get(pk=pk)
    candidates = Candidate.objects.filter(election=election)

    final_candidates = []
    for candidate in candidates:
        candidate.votes = Vote.objects.filter(candidate=candidate).count()
        final_candidates.append(candidate)

    context = {
        'page_title': election.title + ' - Candidates',
        'election': election,
        'candidates': final_candidates,
    }
    return render(request, 'elections/candidates/election_candidates.html', context=context)


@login_required()
def candidate_detail(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    votes = Vote.objects.filter(candidate=candidate).count()
    voted = Vote.objects.filter(election=candidate.election, voter=request.user).exists()
    age = timezone.now().year - candidate.dob.year
    rivals = Candidate.objects.filter(election=candidate.election).exclude(pk=candidate.pk).count()

    context = {
        'page_title': candidate.name,
        'candidate': candidate,
        'age': age,
        'votes': votes,
        'voted': voted,
        'rivals': rivals,
        'total_candidates': rivals + 1,
    }
    return render(request, 'elections/candidates/candidate_details.html', context=context)


@login_required()
def confirm_vote(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    election = candidate.election
    voter = request.user

    if request.method == 'POST':
        vote = Vote.objects.create(candidate=candidate, election=election, voter=voter)
        vote.save()
        messages.success(request, f'Vote for {candidate.name} accepted!')
        return redirect('election_detail', pk=election.pk)

    context = {
        'page_title': 'Confirm Vote',
        'candidate': candidate,
        'election': election,
    }

    return render(request, 'elections/votes/confirm_vote.html', context=context)



@login_required()
def confirm_vote_delete(request, pk):
    vote = Vote.objects.get(pk=pk)

    if request.method == 'POST':
        vote.delete()
        messages.success(request, f'Vote for {vote.candidate.name} deleted!')
        return redirect('vote_history')

    context = {
        'page_title': 'Delete Vote',
        'vote': vote,
    }

    return render(request, 'elections/votes/confirm_vote_delete.html', context=context)



@login_required()
def vote_history(request):
    votes = Vote.objects.filter(voter=request.user)

    context = {
        'page_title': 'Vote History',
        'votes': votes,
    }

    return render(request, 'elections/votes/vote_history.html', context=context)



# stats
@login_required()
def election_stats(request, pk):
    election = Election.objects.get(pk=pk)
    votes = Vote.objects.filter(election=election).count()
    raw_candidates = Candidate.objects.filter(election=election)

    candidates = []
    for candidate in raw_candidates:
        candidate.votes = Vote.objects.filter(candidate=candidate).count()
        candidates.append(candidate)

    male_count = Candidate.objects.filter(election=election, gender='male').count()
    female_count = Candidate.objects.filter(election=election, gender='female').count()

    # bar chart
    candidate_names = []
    candidate_votes = []
    for candidate in raw_candidates:
        candidate_names.append(candidate.name)
        candidate_votes.append(Vote.objects.filter(candidate=candidate).count())

    # line chart
    # Get the past seven days' dates
    today = timezone.now().date()
    past_seven_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    # Query the Vote model to get the vote count for each day
    vote_counts = Vote.objects.filter(created_at__date__in=past_seven_days, election=election) \
                              .values('created_at__date') \
                              .annotate(count=Count('id'))

    # Format the dates and vote counts into separate arrays
    labels = [date.strftime('%b-%d') for date in past_seven_days]
    vote_data = [0] * 7  # Initialize with zeros for each day
    for vote_count in vote_counts:
        vote_date = vote_count['created_at__date']
        index = past_seven_days.index(vote_date)
        vote_data[index] = vote_count['count']

    context = {
        'page_title': election.title + ' - Stats',
        'election': election,
        'candidates': candidates,
        'votes': votes,
        'candidate_names': candidate_names,
        'candidate_votes': candidate_votes,
        'male_count': male_count,
        'female_count': female_count,
        # line chart
        'labels': labels,
        'vote_data': vote_data,
    }
    return render(request, 'elections/stats/election_stats.html', context=context)