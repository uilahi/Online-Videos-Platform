from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.views import generic
from .models import Page, Video
from .forms import VideoForm, SearchForm
import urllib
import requests
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


YOUTUBE_API_KEY = 'AIzaSyDGtRVYIzaUEgJx1gWvhAZGAT0YFujpWFc'


def home(request):
    recent_pages = Page.objects.all().order_by('-id')[:3]
    popular_pages = [Page.objects.get(pk=11), Page.objects.get(pk=9)]
    return render(request, 'home/home.html', {'recent_pages': recent_pages, 'popular_pages': popular_pages})


@login_required
def dashboard(request):
    pages = Page.objects.filter(user=request.user)
    return render(request, 'home/dashboard.html', {'pages': pages})


@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }')
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Not able to validate form'})


@login_required
def addvideo(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    page = Page.objects.get(pk=pk)
    print(page.id)

    if not page.user == request.user:
        raise Http404
    if request.method == 'POST':

        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.page = page
            # try:
            #     video.page = Page.objects.get(pk=pk)
            # except Page.DoesNotExist:
            #     video.page = None

            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detail_page', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a YouTube URL')
    return render(request, 'home/add_video.html', {'form': form, 'search_form': search_form, 'page': page})


class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'home/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.page.user == self.request.user:
            raise Http404
        return video


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreatePage(LoginRequiredMixin, generic.CreateView):
    model = Page
    fields = ['title']
    template_name = 'home/create_page.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreatePage, self).form_valid(form)
        return redirect('dashboard')


class DetailPage(generic.DetailView):
    model = Page
    template_name = 'home/detail_page.html'


class UpdatePage(LoginRequiredMixin, generic.UpdateView):
    model = Page
    template_name = 'home/update_page.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        page = super(UpdatePage, self).get_object()
        if not page.user == self.request.user:
            raise Http404
        return page


class DeletePage(LoginRequiredMixin, generic.DeleteView):
    model = Page
    template_name = 'home/delete_page.html'
    success_url = reverse_lazy('dashboard')
