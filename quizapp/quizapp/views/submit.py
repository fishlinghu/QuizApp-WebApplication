#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json
import random
from google.appengine.ext import db
from quizapp.models.game import Game
from quizapp.models.question import Question
from google.appengine.api import channel

class SubmitHandler(Handler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = int(self.request.get('user'))
        quiz_key = int(self.request.get('quiz_key'))  
        answer = self.request.get('answer')

        #Get the quiz being played by the player
        quiz = Game.get_by_id(quiz_key)
        gameAnswers = quiz.question_answers
        
        #Update quiz based on player
        if user == quiz.a_ID:
            quiz.a_ans_list.append(answer)
            if gameAnswers[len(quiz.a_ans_list) - 1].lower() == answer.lower():
                quiz.a_score_list.append(100)
                quiz.a_score += 100
            else:
                quiz.a_score_list.append(0)
            
            quiz.put()
            
            #Check if a round has ended for the player
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
        elif user == quiz.b_ID:
            quiz.b_ans_list.append(answer)
            if gameAnswers[len(quiz.b_ans_list) - 1].lower() == answer.lower():
                quiz.b_score_list.append(100)
                quiz.b_score += 100
            else:
                quiz.b_score_list.append(0)
            
            quiz.put()
            
            #Check if a round has ended for the player
            if len(quiz.b_ans_list) < 5:
                #Send message containing next question
                questionNumber = len(quiz.b_ans_list)
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
                channel.send_message(str(quiz.b_ID) + str(quiz_key), questionUpdate)
        
        if len(quiz.a_ans_list) >= 5:
            questionUpdate = {
                              'redirect_link' : '/process'
            }
            
            questionUpdate = json.dumps(questionUpdate)
            channel.send_message(str(quiz.a_ID) + str(quiz_key), questionUpdate)
            
        if len(quiz.b_ans_list) >= 5:
            questionUpdate = {
                              'redirect_link' : '/process'
            }
            
            questionUpdate = json.dumps(questionUpdate)
            channel.send_message(str(quiz.b_ID) + str(quiz_key), questionUpdate)
                