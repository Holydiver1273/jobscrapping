from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing
from .forms import JobListingForm

def search_jobs(request):
    query = request.GET.get('q', '')  # Get the search query from the request's GET parameters
    job_listings = JobListing.objects.filter(title__icontains=query) 

    return render(request, 'search_jobs.html', {'job_listings': job_listings, 'query': query})

def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    if request.method == 'POST':
        form = JobListingForm(request.POST, instance=job)  # Bind the form to the job instance

        if form.is_valid():
            form.save()
            return redirect('search_jobs') 

    else:
        form = JobListingForm(instance=job)  # Create a form instance with the job's data

    return render(request, 'edit_job.html', {'form': form, 'job': job})

def delete_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    if request.method == 'POST':
        # Handle the form submission to delete the job listing
        job.delete() 
        return redirect('search_jobs')  
    return render(request, 'delete_job.html', {'job': job})
