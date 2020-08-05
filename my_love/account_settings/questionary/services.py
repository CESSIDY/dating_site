from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from ..forms import AboutMeQuestionaryForm, AboutYouQuestionaryForm
from .settings import form_answer_prefix
from ..models import Questionary, Question, Answer, AboutMe, AboutYou

User = get_user_model()


def get_aboutMe_edit_form(request):
    questions = Question.objects.all()
    formset_init = []
    for question in questions:
        answers_list = []
        for answer in Answer.objects.filter(question=question):
            answers_list.append(answer)
        QuestionarySet = AboutMeQuestionaryForm(user=request.user.pk, question_obj=question)
        formset_init.append(QuestionarySet)
    return formset_init


def get_aboutYou_edit_form(request):
    questions = Question.objects.all()
    formset_init = []
    for question in questions:
        answers_list = []
        for answer in Answer.objects.filter(question=question):
            answers_list.append(answer)
        QuestionarySet = AboutYouQuestionaryForm(user=request.user.pk, question_obj=question)
        formset_init.append(QuestionarySet)
    return formset_init


def save_aboutYou_questionary_form(request):
    for field in request.POST:
        if form_answer_prefix in str(field):
            question_id = str(field)[len(form_answer_prefix):]
            answer_id = request.POST[field]
            obj = request.user.aboutyou
            try:
                question = Question.objects.get(pk=question_id)
                answer = Answer.objects.get(pk=answer_id)
                obj_type = ContentType.objects.get_for_model(obj)
                questionary_obj, is_created = Questionary.objects.get_or_create(content_type=obj_type,
                                                                                user=request.user, question=question,
                                                                                defaults={'answer': answer})
                questionary_obj.answer = answer
                questionary_obj.save()
            except:
                pass


def save_aboutMe_questionary_form(request):
    for field in request.POST:
        if form_answer_prefix in str(field):
            question_id = str(field)[len(form_answer_prefix):]
            answer_id = request.POST[field]
            obj = request.user.aboutme
            question = Question.objects.get(pk=question_id)
            answer = Answer.objects.get(pk=answer_id)
            obj_type = ContentType.objects.get_for_model(obj)
            questionary_obj, is_created = Questionary.objects.get_or_create(content_type=obj_type,
                                                                                user=request.user, question=question,
                                                                                defaults={'answer': answer})
            questionary_obj.answer = answer
            questionary_obj.save()
