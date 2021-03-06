from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy as reverse
from meetup.models import Meeting, Inscricao
from meetup.filters import MeetingFilter
from meetup.forms import MeetingCreateForm, MeetingEditForm
from django.core.paginator import Paginator
from plugApps.tasks import send_confirmation_inscricao
from datetime import datetime, timezone, timedelta
from django.contrib import messages
from geopy.geocoders import Nominatim
import json
from django.contrib.auth.decorators import login_required





def meetup_list(request):
    """View para Listar Reuniões"""

    meetups = Meeting.objects.all()
    meetup_filter = MeetingFilter(request.GET, queryset=meetups)
    meeting = meetup_filter.qs
    paginator = Paginator(meeting, 3)
    page = request.GET.get('page')
    meeting = paginator.get_page(page)

    return render(request, 'meetup/meetup_list.html', {'meeting': meeting,
                                                        'meetups': meetup_filter,
                                                        'titulo': 'Reuniões'})

@login_required
def meetup_create(request):
    """View para Criar a Reunião"""

    form = MeetingCreateForm()
    if request.method == 'POST':
        form = MeetingCreateForm(request.POST, request.FILES)


        if form.is_valid():
            geolocator = Nominatim(user_agent="plugApps")
            meeting = form.save(commit=False)
            if meeting.data_hora < datetime.now(timezone.utc):
                messages.warning(request, "Você não pode cadastrar uma reunião numa data que já passou.")
            else:
                meeting.user = request.user

                if not Meeting.valida_local(meeting.local):
                    messages.warning(request, "Verifique sua coordenada, -7.6567567, 34.7866788 , seria uma coordenada válida. ")
                else:
                    location = geolocator.reverse(meeting.local)
                    if not location.address:
                        meeting.local = "Local não definido, pelo criador da reunião."
                    else:
                        meeting.local = location.address

                    meeting.save()

                    messages.success(request, "Reunião cadastrada  com sucesso.")
                    return redirect(reverse("meetup:detail", args=[meeting.pk]))

    return render(request, "meetup/cadastro.html", locals())


def meetup_detail(request, id):
    """View para visualizar o detalhes de uma Reunião"""

    meetup = get_object_or_404(Meeting, pk=id)

    return render(request, 'meetup/meetup_detail.html', locals())


@login_required
def meetup_edit(request, id):
    """"View para Editar uma Reunião"""

    meetup = get_object_or_404(Meeting, pk=id, user=request.user)

    breadcrumbs = [
        (reverse("meetup:meetup_list"), "Reuniões"),
        (reverse("meetup:meetup_detail", args=[id]), meetup.id),
        ("#", "Editar")
    ]

    form = MeetingEditForm(instance=meetup)

    if request.method == 'POST':
        form = MeetingEditForm(request.POST, request.FILES, instance=meetup)

        if form.is_valid():
            meeting = form.save(commit=False)
            if meeting.data_hora > datetime.now(timezone.utc):
                meeting.save()
                return redirect(reverse("meetup:detail", args=[meeting.pk]))
            else:
                messages.warning(request, "Evento já iniciado, você não pode mais editar")
                return redirect(reverse("meetup:detail", args=[meeting.pk]))

    return render(request, "meetup/cadastro.html", locals())

@login_required
def inscricao_create(request, id):
    """View pararealizar incrição na Reunião"""

    meeting = get_object_or_404(Meeting, pk=id)

    if meeting.user == request.user:
        messages.warning(request, "Você não pode se inscrever nesta reunião. Ela foi criada por você.")
    elif Inscricao.objects.filter(meeting_id=id, participante=request.user):
        messages.warning(request, "Você já está inscrito nesta reunião.")
    elif meeting.data_hora < datetime.now(timezone.utc):
        messages.warning(request, "Você não pode se inscrever em uma reunião que já passou.")
    elif Inscricao.objects.filter(data_meeting=meeting.data_hora):
        messages.warning(request, "Você já esta inscrito em uma reuniao nesta data.")
    else:
        inscricao = Inscricao.objects.all()
        Inscricao.objects.create(meeting_id=meeting.id,
                                    data_meeting=meeting.data_hora,
                                    participante=request.user)

        send_confirmation_inscricao.delay(
            meeting.user.first_name,
            meeting.user.last_name,
            meeting.titulo,
            meeting.user.email,
        )

        messages.success(request, "Você foi inscrito na reunião.")

    return redirect(reverse("meetup:detail", args=[meeting.id]))

@login_required
def inscricao_list(request):
    """View para listar inscrições de usuario logado."""

    inscricoes = Inscricao.objects.filter(participante=request.user).distinct('meeting_id')
    inscricao = []
    for item in inscricoes:
        inscricao.append(item.meeting_id)

    meetups = Meeting.objects.filter(id__in=inscricao)
    meetup_filter = MeetingFilter(request.GET, queryset=meetups)
    meeting = meetup_filter.qs
    paginator = Paginator(meeting, 3)
    page = request.GET.get('page')
    meeting = paginator.get_page(page)

    return render(request, 'meetup/meetup_list.html', {'meeting': meeting,
                                                        'meetups': meetup_filter,
                                                        'titulo': 'Minhas inscrições'})

@login_required
def reuniao_list_user(request):
    """View para listar reuniões cadastrada pelo usuario logado."""

    meetups = Meeting.objects.filter(user=request.user)
    meetup_filter = MeetingFilter(request.GET, queryset=meetups)
    meeting = meetup_filter.qs
    paginator = Paginator(meeting, 3)
    page = request.GET.get('page')
    meeting = paginator.get_page(page)

    return render(request, 'meetup/meetup_list.html', {'meeting': meeting,
                                                        'meetups': meetup_filter,
                                                        'titulo': 'Minhas reuniões'})

@login_required
def proximas_reunioes(request):
    """View listar minhas inscrições"""

    amanha = datetime.now(timezone.utc)+timedelta(days=1)
    semana = datetime.now(timezone.utc)+timedelta(days=7)
    mes = datetime.now(timezone.utc)+timedelta(days=30)
    reunioes_hoje = Meeting.objects.filter(data_hora__gte=datetime.now(timezone.utc),
                                            data_hora__lte=amanha).count()
    reunioes_semana = Meeting.objects.filter(data_hora__gte=datetime.now(timezone.utc),
                                                data_hora__lte=semana).count()
    reunioes_mes = Meeting.objects.filter(data_hora__gte=datetime.now(timezone.utc),
                                            data_hora__lte=mes).count()


    return render(request, 'meetup/meetups_count.html', {'dia': reunioes_hoje,
                                                            'semana': reunioes_semana,
                                                            'mes': reunioes_mes})
