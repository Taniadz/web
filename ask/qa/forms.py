from __future__ import unicode_literals

from django import forms
from qa.models import Question, Answer
class AskForm(forms.Form):
    title=forms.CharField(max_length=225)
    text=forms.CharField(widget=forms.Textarea)


    def clean_title(self):
        title = self.cleaned_data['title']
        if title.strip() == '':
            raise forms.ValidationError(
                u'Title is empty', code='validation_error')
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError(
                u'Text is empty', code='validation_error')
        return text

    def save (self):
        ask = Question(**self.cleaned_data)
        ask.save()
        return ask

class AnswerForm(forms.Form):
    
    text=forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            question = None
        return question_id

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError(
                u'Text is empty', code='validation_error')
        return text

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer