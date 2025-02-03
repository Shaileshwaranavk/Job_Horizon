from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegistrationForm, OrganizationRegistrationForm
from .models import UserProfile, OrganizationProfile, JobOpening
from django.contrib.auth.decorators import login_required

# Home page view
def home(request):
    return render(request, 'index.html')

# User Registration page view
def register(request):
    if request.method == 'POST':
        # Extract data from POST request
        name = request.POST.get('name')
        role = request.POST.get('role')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        experience = request.POST.get('experience', '')
        domains = request.POST.get('domains', '')
        expected_pay = request.POST.get('expected_pay', '')
        projects = request.POST.get('projects', '')
        github = request.POST.get('github', '')
        portfolio = request.POST.get('portfolio', '')
        linkedin = request.POST.get('linkedin', '')
        photo = request.FILES.get('photo')
        resume = request.FILES.get('resume')

        # Check for missing required fields
        if not all([name, role, email, phone, password, gender]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'RegisterPage.html')

        # Create and save the UserProfile instance
        user = UserProfile(
            name=name,
            role=role,
            email=email,
            phone=phone,
            password=password,  # No hashing here as per your requirement
            gender=gender,
            experience=experience,
            domains=domains,
            expected_pay=expected_pay,
            projects=projects,
            github=github,
            portfolio=portfolio,
            linkedin=linkedin,
            photo=photo,
            resume=resume,
        )
        user.save()

        messages.success(request, 'Your account has been created successfully!')
        return redirect('login_page')  # Redirect to login page after successful registration

    return render(request, 'RegisterPage.html')

# Login page view for users
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(email=email)
            if password == user.password:  # Compare plain text password
                request.session['user_id'] = user.id
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('User_Profile')  # Redirect to user profile after successful login
            else:
                messages.error(request, 'Invalid password.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'LoginPage.html')

# Profile page view for user
def user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'You need to log in to view your profile.')
        return redirect('login_page')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        user = None

    return render(request, 'Profile.html', {'user': user})



def org_registration(request):
    if request.method == 'POST':
        # Extract data from the form
        organization_name = request.POST.get('organization_name')
        manager_name = request.POST.get('manager_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        company_size = request.POST.get('company_size')
        company_description = request.POST.get('company_description')
        company_type = request.POST.get('company_type')
        password = request.POST.get('password')

        # Create and save the new organization profile
        organization = OrganizationProfile(
            organization_name=organization_name,
            manager_name=manager_name,
            email=email,
            contact_number=contact_number,
            company_size=company_size,
            company_description=company_description,
            company_type=company_type,
            password=password,
        )
        organization.save()

        # Display success message
        messages.success(request, "Organization registered successfully!")
        return redirect('organization_login')  # Redirect to a success page or any other page

    return render(request, 'OrgRegisterPage.html')

# Organization Login page view
def organization_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            organization = OrganizationProfile.objects.get(email=email)
            if password == organization.password:  # Compare plain text password
                request.session['organization_id'] = organization.id  # Store organization ID in session
                messages.success(request, f"Welcome back, {organization.organization_name}!")
                return redirect('organization_dashboard')  # Redirect to organization dashboard after successful login
            else:
                messages.error(request, 'Invalid email or password.')
        except OrganizationProfile.DoesNotExist:
            messages.error(request, 'Account does not exist. Please register first.')

    return render(request, 'OrgLoginPage.html')

# Organization Dashboard page view
def organization_dashboard(request):
    organization_id = request.session.get('organization_id')
    if not organization_id:
        messages.error(request, 'You must be logged in to view the dashboard.')
        return redirect('organization_login')

    try:
        organization = OrganizationProfile.objects.get(id=organization_id)
    except OrganizationProfile.DoesNotExist:
        messages.error(request, 'Organization profile not found.')
        return redirect('organization_login')

    job_openings = organization.job_openings.all()
    return render(request, 'organization_dashboard.html', {'organization': organization, 'job_openings': job_openings})

# Job openings list page view
def job_openings_list(request):
    # For anonymous users, no organization data is needed, just fetch all job openings
    job_openings = JobOpening.objects.all()

    # For authenticated users, we may display organization-related data if needed
    if request.user.is_authenticated:
        try:
            # Get the organization associated with the logged-in user
            organization_profile = OrganizationProfile.objects.get(user=request.user)
        except OrganizationProfile.DoesNotExist:
            organization_profile = None

        # Pass the organization data to the template if needed (optional)
        context = {
            'organization_profile': organization_profile,
            'job_openings': job_openings,
        }
    else:
        context = {
            'job_openings': job_openings,
        }

    return render(request, 'job_openings_list.html', context)

# Create Job Opening view (for organization)
def create_job(request, organization_id):
    organization = get_object_or_404(OrganizationProfile, id=organization_id)

    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        pay = request.POST.get('pay')
        requiredskills=request.POST.get('required_skills')
        location=request.POST.get('location')

        if pay is not None:  # Ensure pay is not null
            job_opening = JobOpening(
                organization=organization,
                job_title=job_title,
                job_description=job_description,
                pay=pay,
                required_skills=requiredskills,
                location=location,
            )
            job_opening.save()
            messages.success(request, 'Job opening created successfully!')
            return redirect('organization_dashboard')

        else:
            messages.error(request, 'Pay is required!')
            return render(request, 'create_job.html', {'organization': organization})

    return render(request, 'create_job.html', {'organization': organization})


# Edit Job Opening view (for organization)
def edit_job(request, job_id):
    organization_id = request.session.get('organization_id')
    if not organization_id:
        messages.error(request, 'You must be logged in to edit a job opening.')
        return redirect('organization_login')

    organization = get_object_or_404(OrganizationProfile, id=organization_id)
    job_opening = get_object_or_404(JobOpening, id=job_id)

    if job_opening.organization != organization:
        messages.error(request, 'You are not authorized to edit this job opening.')
        return redirect('organization_dashboard')

    if request.method == 'POST':
        job_opening.job_title = request.POST.get('job_title')
        job_opening.job_description = request.POST.get('job_description')
        job_opening.save()
        messages.success(request, 'Job opening updated successfully!')
        return redirect('organization_dashboard')

    return render(request, 'edit_job.html', {'organization': organization, 'job_opening': job_opening})

# Delete Job Opening view (for organization)
def delete_job(request, job_id):
    organization_id = request.session.get('organization_id')
    if not organization_id:
        messages.error(request, 'You must be logged in to delete a job opening.')
        return redirect('organization_login')

    organization = get_object_or_404(OrganizationProfile, id=organization_id)
    job_opening = get_object_or_404(JobOpening, id=job_id)

    if job_opening.organization != organization:
        messages.error(request, 'You are not authorized to delete this job opening.')
        return redirect('organization_dashboard')

    job_opening.delete()
    messages.success(request, 'Job opening deleted successfully!')
    return redirect('organization_dashboard')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Simple check for 'admin' username and password
        if username == 'admin' and password == 'admin':
            # Successful login, redirect to a dashboard (or another page)
            return redirect('dashboard')  # Replace with your desired redirect

        else:
            messages.error(request, "Authentication failed. Incorrect username or password.")

    return render(request, 'AdminLoginPage.html')


def dashboard(request):
    # Get all users and job postings
    users = UserProfile.objects.all()
    jobs = JobOpening.objects.all()

    # Handle search functionality
    if request.method == "POST":
        search_query = request.POST.get('search_query', '').strip()

        # Filter users and jobs based on search query
        if search_query:
            users = users.filter(name__icontains=search_query)
            jobs = jobs.filter(job_title__icontains=search_query)

    return render(request, 'dashboard.html', {'users': users, 'jobs': jobs})

def suggest_user_to_job(request, job_id):
    if request.method == 'POST':
        # Get the user and job details
        user = UserProfile.objects.get(id=request.POST['user_id'])
        job = JobOpening.objects.get(id=job_id)

        # Send email to the company
        send_mail(
            subject=f"Suggested Candidate for {job.job_title}",
            message=f"User {user.name} is interested in the job {job.job_title}. \n"
                    f"User Details: \n Name: {user.name} \n Email: {user.email} \n Phone: {user.phone} \n "
                    f"Portfolio: {user.portfolio} \n GitHub: {user.github}",
            from_email='admin@jobportal.com',
            recipient_list=[job.organization.email],  # Assuming the organization profile has an email field
        )

        # Redirect back to the dashboard with success message
        return render(request, 'dashboard.html', {'success': "Email sent to the company!"})