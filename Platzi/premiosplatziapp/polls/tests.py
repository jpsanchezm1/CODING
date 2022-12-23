from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.urls.base import reverse

# Create your tests here.

class QuestionModelTests(TestCase):

    def setUp(self):
        self.question = Question(question_text="¿Quién es el mejor CD?")

    def test_was_published_recently_with_future_questions(self):
        "Returns False for questions published in the future"
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        "Returns True for questions published not recently"
        time = timezone.now() - datetime.timedelta(days=17)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_current_time(self):
        "Returns False for questions published just now"
        time = timezone.now()
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

def Create_question(question_text,days):
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):


    def test_no_questions(self):
        """If no question exists, an appropriate message will be displayed """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_no_future_questions(self):
        "No questions scheduled to be published in the future will be displayed"
        Create_question("Future Question",20)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_questions(self):
        "Questions published in the past will be displayed"
        question=Create_question("Past_Question",days=-2)
        response = self.client.get(reverse("polls:index"))
        self.assertSequenceEqual(response.context['latest_question_list'],[question])


    def test_future_and_past_questions(self):
        """Even if both past and future questions exist, only past questions are displayed"""
        past_q = Create_question("Past question",-5)
        future_q = Create_question("Future question",5)
        response = self.client.get(reverse("polls:index"))
        self.assertSequenceEqual(response.context['latest_question_list'],[past_q])

    def test_multiple_future_questions(self):
        """The questions index page may display multiple questions"""
        question = Create_question("Future Question 1",2)
        question2 = Create_question("Future Question 2",5)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
        #print("test questions")

    def test_multiple_past_questions(self):
        """The questions index page may display multiple questions"""
        question = Create_question("Past Question 1",-2)
        question2 = Create_question("Past Question 2",-5)
        response = self.client.get(reverse("polls:index"))
        self.assertSequenceEqual(response.context['latest_question_list'],[question,question2])
        #print(response.context['latest_question_list'],[question,question2])


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future should display the error 404: Not Found"""
        future_q = Create_question("Future Question",2)
        url = reverse("polls:detail",args=(future_q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past
        should display the question's text"""
        past_q = Create_question("Future Question",-2)
        url = reverse("polls:detail",args=(past_q.id,))
        response = self.client.get(url)
        self.assertContains(response,past_q.question_text)