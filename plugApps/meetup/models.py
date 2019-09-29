# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import os
from plugApps import settings
from django.db import models
from plugApps.tasks import resize
from django.db.models import signals
import json


class Meeting(models.Model):
    """
    Modelo responsável por criar uma reunião
    """
    titulo = models.CharField(max_length=50)
    descricao =  models.TextField()
    data_hora = models.DateTimeField()
    imagem = models.ImageField()
    local = models.CharField(max_length=255)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super(Meeting, self).save(*args, **kwargs)
        resize.delay(json.dumps(str(self.imagem)))

    def valida_local(local):
        validacao = []
        validacao =  local.split(',')
        if len(validacao) == 2:
            x = validacao[0].replace('-','').replace('.','')
            y = validacao[0].replace('-','').replace('.','')
            if x.isdigit() and y.isdigit():
                return True;
            else:
                return False;
        else:
            return False;

class Inscricao(models.Model):
    """
    Modelo responsável por armazenar as inscrições nas reuniões
    """
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    participante = models.ForeignKey(User, on_delete=models.CASCADE)
    data_meeting = models.DateTimeField()
    data_inscricao = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.participante
