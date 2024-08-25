from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib,base64



# Create your views here.
def home(request):
    #return render(request,'home.html')
    #return render(request,'home.html',{'name': 'David Lopera'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'searchTerm':searchTerm,'movies': movies})

def about(request):
    return render(request,'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request,'signup.html',{'email':email})

def statistics_view(request):
    matplotlib.use('Agg')
    # Obtener todos los años de las películas y contar cuántas hay por año
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {year: Movie.objects.filter(year=year).count() for year in years if year is not None}

    # Crear gráfica de barras para las películas por año
    bar_width = 0.5
    bar_position_year = range(len(movie_counts_by_year))

    plt.bar(bar_position_year, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_position_year, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

 
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()


    img_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(img_png).decode('utf-8')

    # Obtener todos los géneros de las películas y contar cuántas hay por género
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    first_genres = {genre.split(',')[0].strip() for genre in genres if genre}  # Tomar solo el primer género
    movie_counts_by_genre = {gen: Movie.objects.filter(genre__icontains=gen).count() for gen in first_genres if gen}

    # Crear gráfica de barras para las películas por género
    bar_position_genre = range(len(movie_counts_by_genre))

    plt.bar(bar_position_genre, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_position_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    img_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(img_png).decode('utf-8')

    return render(request, 'statistics.html', {
        'graphic': graphic_year,
        'graphic2': graphic_genre
    })
