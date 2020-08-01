from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from ..forms import AboytMeQuestionaryForm
from ..models import Questionary, Question, Answer, AboutMe, AboutYou

User = get_user_model()


def get_edit_form(request):
    questions = Question.objects.filter(content_type=ContentType.objects.get_for_model(request.user.aboutme))
    formset_init = []
    for question in questions:
        answers_list = []
        for answer in Answer.objects.filter(question=question):
            answers_list.append(answer)
        QuestionarySet = AboytMeQuestionaryForm(user=request.user, question_obj=question)
        formset_init.append(QuestionarySet)
    return formset_init

# make like to article(obj)
def add_to_questionary(obj, questionary):
    obj_type = ContentType.objects.get_for_model(obj)
    for question_id, answer_id in questionary:
        questionary_obj, is_created = Questionary.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, question=question_id, defaults={'answer': answer_id})
        questionary_obj.save()
