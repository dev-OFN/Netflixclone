import imp 
import random 
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from .models import Profile, Movie
from django.contrib.auth import logout

# Create your views here.

# def Home(request):
#     return render(request, 'netflixapp/index.html')

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('netflixapp:profile-list')
        return render(request,'index.html')

method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self,request,*args,**kwargs):

        profiles =request.user.profiles.all()
        context = {
            'profiles':profiles
        }
        return render(request, 'profilelist.html',context)    
    
method_decorator(login_required, name='dispatch')
# class ProfileCreate(View):
#     def get(self, request, *args, **kwargs):
#         form = ProfileForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'profileCreate.html', context)

#     def post(self, request, *args, **kwargs):
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.save()
#             request.user.profiles.add(profile)
#             return redirect('netflixapp:profile-list')
#         context = {
#             'form': form
#         }
#         return render(request, 'profileCreate.html', context)
class ProfileCreate(View):
    def get(self,request,*args,**kwargs):
        form = ProfileForm()
        context = {
            'form':form
        }
        return render(request, 'profileCreate.html',context)
    
    def post(self, request,*args,**kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            profile = Profile.objects.create (**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect ('netflixapp:profile-list')
        context = {
            'form':form
        }
       
        return render(request, 'profileCreate.html',context)   

method_decorator(login_required, name='dispatch')
class MovieList(View):
    def get(self, request,profile_id, *args, **kwargs): 
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit= profile.age_limit)
            if profile not in request.user.profiles.all():
                return redirect ('netflixapp:profile-list')
            context = {
                'movies':movies
            }

            return render(request, 'movielist.html',context)  
        except Profile.DoesNotExist:
            return redirect ('netflixapp:profile-list')
    

def random_movie(request):
        total_movies = Movie.objects.count()
        random_index = random.randint(0, total_movies - 1)
        random_movie = Movie.objects.all()[random_index]

        return render(request, 'movielist.html', {'random_movie': random_movie})



@method_decorator(login_required, name='dispatch')
class MovieDetail(View):
    def get(self, request,movie_id, *args, **kwargs): 
        try:
            movie = Movie.objects.get(uuid = movie_id)
            
            context = {
                'movie':movie
            }

            return render(request, 'moviedetail.html',context)  
        except Movie.DoesNotExist:
            return redirect ('netflixapp:profile-list')
        

@method_decorator(login_required, name='dispatch')
class PlayMovie(View):
    def get(self, request,movie_id, *args, **kwargs): 
        try:
            movie = Movie.objects.get(uuid = movie_id)
            movie = movie.video.values()
            
            context = {
                'movie':list(movie)
            }

            return render(request, 'playmovie.html',context)  
        except Movie.DoesNotExist:
            return redirect ('netflixapp:profile-list')


# def random_movie(request):
#     # Get the total number of movies in the database
#     total_movies = Movie.objects.count()

#     # Generate a random index
#     random_index = random.randint(0, total_movies - 1)

#     # Get the random movie
#     random_movie = Movie.objects.all()[random_index]

#     # Render the 'moviedetail.html' template with the random_movie context
#     return render(request, 'movielist.html', {'random_movie': random_movie})

# def random_movie(request):
#     if 'random_movie' not in request.session:
#         total_movies = Movie.objects.count()
#         random_index = random.randint(0, total_movies - 1)
#         random_movie = Movie.objects.all()[random_index]
#         request.session['random_movie'] = random_movie.id

#     return render(request, 'movielist.html', {'random_movie': request.session.get('random_movie')})



# def random_movie(request):
#     # Check if the request path is for the 'movielist.html' URL
#     if request.path == 'http://127.0.0.1:8080/watch/f3a59b40-b42f-40c9-8dc0-2b8639bf06be/':
#         # Get the total number of movies in the database
#         total_movies = Movie.objects.count()

#         # Generate a random index
#         random_index = random.randint(0, total_movies - 1)

#         # Get the random movie
#         random_movie = Movie.objects.all()[random_index]

#         # Render the 'movielist.html' template with the random_movie context
#         return render(request, 'movielist.html', {'random_movie': random_movie})

#     # If the request path is not for 'movielist.html', return a different response
#     return HttpResponse("This is a different page.")




def custom_logout(request):
    logout(request)
    return redirect('netflixapp:Home')