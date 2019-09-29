import secrets
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View
from account.forms import UserForm
from account.models import ConfirmationToken
from .tasks import send_confirmation_email
from datetime import datetime


class RegistrationView(View):
    """View para realizar cadastro de usuários"""

    def get(self, request):
        user_form = UserForm()
        context = {
            "form": user_form,
        }
        return render(request, "account/register.html", context)

    def post(self, request):
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            confirmation_token = ConfirmationToken.objects.create(
                user=user,
                confirmation_key=secrets.token_hex(16)
            )


            send_confirmation_email.delay(
                confirmation_token.confirmation_key,
                user.id,
                user.email,
            )

            messages.success(request, 'Usuário cadastrado com sucesso.')

            return redirect('meetup:meetup_list')

        messages.warning(
            request, 'Verifique todos os dados antes de prosseguir.')

        context = {
            "form": user_form,
        }
        return render(request, "account/register.html", context)


class ConfirmRegistrationView(View):
    """View para verificar token de usuário"""

    def get(self, request):
        user_id = request.GET.get("id", None)
        confirmation_key = request.GET.get("confirmation_key", None)

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            messages.warning(
                request, 'Usuário não cadastrado.')
            return redirect('account:registration')

        if user.confirmation_token.is_confirmed:
            messages.warning(
                request, 'Cadastro do usuário já foi confirmado.')
            return redirect('account:confirm')

        print(user.confirmation_token.data_criacao)

        if user.confirmation_token.confirmation_key == confirmation_key:
            user.confirmation_token.is_confirmed = True
            user.confirmation_token.data_confirmacao = datetime.now()
            user.confirmation_token.save()

            messages.success(
                request, 'Cadastro do usuário confirmado com sucesso.')
        else:
            messages.warning(
                request, 'Chave de confirmação inválida.')

        return render(request, "account/confirmation.html", locals())
