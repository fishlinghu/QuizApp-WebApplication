#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json
from google.appengine.ext import db
from quizapp.models.game import Game
from quizapp.models.question import Question
from google.appengine.api import channel

class QuizUpdater(Game):
    quiz = None
    
    def __init__(self, quiz):
        self.quiz  = quiz
        
    def get_quiz(self):
        return quiz
    
    def get_quiz_message(self):
        quizUpdate = {
                      'a_ID' : self.quiz.a_ID,
                      'b_ID' : self.quiz.b_ID,
                      'question_set' : self.quiz.question_set,
                      'a_ans_list' : self.quiz.a_ans_list,
                      'b_ans_list' : self.quiz.b_ans_list,
                      'a_score' : self.quiz.a_score,
                      'b_score' : self.quiz.b_score,
                      'a_score_list' : self.quiz.a_score_list,
                      'b_score_list' : self.quiz.b_score_list
                      }
        return json.dumps(quizUpdate)
    
    def send_update(self):
        channel.send_message(self.quiz.a_ID + self.game.key().id(), self.get_game_message())
        if self.quiz.b_ID:
            channel.send_message(self.quiz.b_ID + self.game.key().id(), self.get_game_message())

class SubmitHandler(Handler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = int(self.request.get('user'))
        quiz_key = int(self.request.get('quiz_key'))  
        answer = True
        score = int(self.request.get('score'))
        
        
        #Get the quiz being played by the player
        quiz = Game.get_by_id(quiz_key)
        
        #Update quiz based on player
        if user == quiz.a_ID:
            quiz.a_ans_list.append(answer)
            quiz.a_score_list.append(score)
            quiz.a_score += score
        elif user == quiz.b_ID:
            quiz.b_ans_list.append(answer)
            quiz.b_score_list.append(score)
            quiz.b_score += score
            
        quiz.put()
            
        #Check if a round has ended
        if len(quiz.a_ans_list) == len(quiz.b_ans_list):
            #Send message containing next question
            questionNumber = len(quiz.a_ans_list)
            questionNumber = quiz.question_set[questionNumber]
            
            query = db.Query(Question)
            query.filter('topic_ID', quiz.topic_ID)
            query.filter('question_ID', questionNumber)
            nextQuestion = query.get()
            
            questionUpdate = {
                              'description' : nextQuestion.description,
                              'correctAns' : nextQuestion.correct_ans,
                              'wrongAns' : nextQuestion.wrong_ans[0:3]
                              }
            
            questionUpdate = json.dumps(questionUpdate)
            channel.send_message(str(quiz.a_ID) + str(quiz_key), questionUpdate)
            channel.send_message(str(quiz.b_ID) + str(quiz_key), questionUpdate)