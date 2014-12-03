#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import logging
from google.appengine.ext import db
from quizapp.models.game import Game
from quizapp.models.question import Question
from google.appengine.api import channel

class SubmitHandler(Handler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = self.request.get('user')
        quiz_key = self.request.get('quiz_key')  
        answer = self.request.get('answer')
        score = self.request.get('score')
        
        
        #Get the quiz being played by the player
        quiz = Game.get_by_id(long(quiz_key))
        
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
            logging.info(questionNumber)
            questionNumber = quiz.question_set[questionNumber]
            logging.info(questionNumber)
            
            query = db.Query(Question)
            query.filter('topic_ID', quiz.topic_ID)
            query.filter('question_ID', questionNumber)
            nextQuestion = query.get()
            logging.info(nextQuestion)
            
            questionUpdate = {
                              'description' : nextQuestion.description,
                              'correctAns' : nextQuestion.correct_ans,
                              'wrongAns' : nextQuestion.wrong_ans[0:3]
                              }
            
            questionUpdate = json.dumps(quizUpdate)
            channel.send_message(quiz.a_ID + quiz.key().id(), questionUpdate)
            channel.send_message(quiz.b_ID + quiz.key().id(), questionUpdate)