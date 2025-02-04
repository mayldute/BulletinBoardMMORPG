from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from .models import Announcement, Respond, RESPOND_STATUS, STATUS_CHOICES
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AnnouncementForm, RespondForm
from .filters import AnnouncementFilter
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .tasks import notify_about_accepted_respond, notify_about_new_respond


class AnnouncementsList(ListView):
    model = Announcement
    ordering = ['-create_time']
    template_name = 'announcements/announcements.html'
    context_object_name = 'announcements'
    paginate_by = 20

    def get_queryset(self):
        queryset = Announcement.objects.filter(status='ACTIVE')
        self.filterset = AnnouncementFilter(self.request.GET, queryset=queryset) 
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset 
        return context


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        announcement = self.get_object()

        context['form'] = RespondForm() 
        context['responds'] = Respond.objects.filter(announcement=announcement) 
        context['is_owner'] = self.request.user == announcement.user  
        context['status_choices'] = STATUS_CHOICES  
        return context
    
    def post(self, request, *args, **kwargs):
        """Обрабатываем отправку отклика"""
        announcement = self.get_object()
        
        if not request.user.is_authenticated:
            return redirect('login') 

        form = RespondForm(request.POST)
        if form.is_valid():
            respond = form.save(commit=False)
            respond.announcement = announcement
            respond.user = request.user
            respond.save()

            notify_about_new_respond(respond.id)
            return redirect(reverse_lazy('announcement_detail', kwargs={'pk': announcement.pk})) 
        

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

class ChangeAnnouncementStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk, user=request.user)  

        new_status = request.POST.get("status")
        valid_statuses = [status_code for status_code, _ in STATUS_CHOICES]

        if new_status in valid_statuses:
            announcement.status = new_status
            announcement.save()
        
        return redirect(reverse_lazy('announcement_detail', args=[announcement.pk]))  

class AnnouncementCreate(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class AnnouncementUpdate(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_edit.html'

    def form_valid(self, form):
        announcement = form.save(commit=False)
        category_updated = False
        current_category = announcement.category
        new_category = form.cleaned_data.get('category')

        if set(current_category) != set(new_category):
            category_updated = True
                
        if category_updated:
            announcement.category.set(new_category)

        announcement.save()
        return super().form_valid(form)

class RespondDetail(DetailView):
    model = Respond
    template_name = 'announcements/respond_detail.html'
    context_object_name = 'respond'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class ChangeRespondStatusView(LoginRequiredMixin, UpdateView):
    model = Respond
    fields = []
    
    def post(self, request, pk):
        respond = get_object_or_404(Respond, pk=pk, announcement__user=request.user)
        
        new_status = request.POST.get("status")  
        valid_statuses = [status_code for status_code, _ in RESPOND_STATUS]  

        if new_status in valid_statuses:
            respond.status = new_status
            respond.save()

        if new_status == 'ACP':
            notify_about_accepted_respond.delay(respond.id)

        return redirect(reverse_lazy('respond_detail', args=[respond.pk]))