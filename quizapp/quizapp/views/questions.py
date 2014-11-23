#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views import Handler
import json

class QuestionHandler(Handler):
    def render_question(self, json_text):
        self.write_plain(json_text)

    def get(self, topic):
        question1 = {
            "question": "What is foo?",
            "topic": "trivia",
            "correct": "bar",
            "incorrect": ["baz", "qux", "norf"],
            "description": "The terms foobar (/ˈfuːbɑr/), fubar, or foo, bar, baz and qux (alternatively, quux) and sometimes norf[1] are sometimes used as placeholder names (also referred to as metasyntactic variables) in computer programming or computer-related documentation.[2] They have been used to name entities such as variables, functions, and commands whose purpose is unimportant and serve only to demonstrate a concept. The words themselves have no meaning in this usage. Foobar is sometimes used alone; foo, bar, and baz are sometimes used, when multiple entities are needed.",
            "wiki": "https://en.wikipedia.org/wiki/Foobar"
        }
        question2 = {
            "question": "What is foo?",
            "topic": "trivia",
            "correct": "bar",
            "incorrect": ["baz", "qux", "norf"],
            "description": "The terms foobar (/ˈfuːbɑr/), fubar, or foo, bar, baz and qux (alternatively, quux) and sometimes norf[1] are sometimes used as placeholder names (also referred to as metasyntactic variables) in computer programming or computer-related documentation.[2] They have been used to name entities such as variables, functions, and commands whose purpose is unimportant and serve only to demonstrate a concept. The words themselves have no meaning in this usage. Foobar is sometimes used alone; foo, bar, and baz are sometimes used, when multiple entities are needed.",
            "wiki": "https://en.wikipedia.org/wiki/Foobar"
        }
        question3 = {
            "question": "What is foo?",
            "topic": "trivia",
            "correct": "bar",
            "incorrect": ["baz", "qux", "norf"],
            "description": "The terms foobar (/ˈfuːbɑr/), fubar, or foo, bar, baz and qux (alternatively, quux) and sometimes norf[1] are sometimes used as placeholder names (also referred to as metasyntactic variables) in computer programming or computer-related documentation.[2] They have been used to name entities such as variables, functions, and commands whose purpose is unimportant and serve only to demonstrate a concept. The words themselves have no meaning in this usage. Foobar is sometimes used alone; foo, bar, and baz are sometimes used, when multiple entities are needed.",
            "wiki": "https://en.wikipedia.org/wiki/Foobar"
        }
        questions = {
            "questions": [question1, question2, question3]
        }
        self.write_plain("You requested questions for topic: " + topic + "\n" + json.dumps(
            questions, 
            sort_keys=True, 
            indent=4, 
            separators=(',', ': '))
        )
