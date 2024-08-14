# coding: utf-8
from django import forms

class ONESOptionsForm(forms.Form):
  email = forms.CharField(
    max_length=255,
    help_text='ones login email',
    required= 'true'
  )
  password = forms.CharField(
    max_length=255,
    help_text='ones login password',
    required= 'true'
  )
  assign = forms.CharField(
    max_length=255,
    help_text='ones assign id',
    required= 'true'
  )
  project_uuid = forms.CharField(
    max_length=255,
    help_text='ones project_uuidid',
    required= 'true'
  )
  issue_type_uuid = forms.CharField(
    max_length=255,
    help_text='ones issue_type id'
  )