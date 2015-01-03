#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json
import random
from google.appengine.ext import db
from quizapp.models.game import Game
from quizapp.models.player import Player
from quizapp.models.question import Question
from google.appengine.api import channel

class SubmitHandler(Handler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = int(self.request.get('user'))
        quiz_key = int(self.request.get('quiz_key'))  
        answer = self.request.get('answer')
        score = 100
            
        #Get the quiz being played by the player
        quiz = Game.get_by_id(quiz_key)
        
        #Update quiz based on player
        if user == quiz.a_ID:
            question = Question.get_by_id(quiz.question_set[len(quiz.a_ans_list)])
            if question.correct_ans.lower() == answer.lower():
                quiz.a_ans_list.append(True)
                quiz.a_score_list.append(score)
                quiz.a_score += score
            else:
                quiz.a_ans_list.append(False)
                quiz.a_score_list.append(0)
        elif user == quiz.b_ID:
            question = Question.get_by_id(quiz.question_set[len(quiz.b_ans_list)])
            if question.correct_ans.lower() == answer.lower():
                quiz.b_ans_list.append(True)
                quiz.b_score_list.append(score)
                quiz.b_score += score
            else:
                quiz.b_ans_list.append(False)
                quiz.b_score_list.append(0)
            
        quiz.put()
            
        #Check if a round has ended
        if len(quiz.a_ans_list) == len(quiz.b_ans_list):
            if len(quiz.a_ans_list) < 5:
                #Send message containing next question
                questionNumber = len(quiz.a_ans_list)
                questionNumber = quiz.question_set[questionNumber]
                nextQuestion = Question.get_by_id(questionNumber)
            
                #Shuffle answers to question
                answers = nextQuestion.wrong_ans
                answers.append(nextQuestion.correct_ans)
                random.shuffle(answers)
                
                for answer in answers:
                    answer = answer.title()
                
                questionUpdate = {
                                  'question' : nextQuestion.question,
                                  'img_link' : nextQuestion.img_link,
                                  'answers' : answers
                                  }
            
                questionUpdate = json.dumps(questionUpdate)
                channel.send_message(str(quiz.a_ID) + str(quiz_key), questionUpdate)
                channel.send_message(str(quiz.b_ID) + str(quiz_key), questionUpdate)
            else:
                player1 = Player.get_by_id(quiz.a_ID)
                player1.game_history.append(quiz.key().id())
                player1.put()
                player2 = Player.get_by_id(quiz.b_ID)
                player2.game_history.append(quiz.key().id())
                player2.put()
                questionUpdate = {
                                  'redirect_link' : '/results'
                                  }
            
                questionUpdate = json.dumps(questionUpdate)
                channel.send_message(str(quiz.a_ID) + str(quiz_key), questionUpdate)
                channel.send_message(str(quiz.b_ID) + str(quiz_key), questionUpdate)
