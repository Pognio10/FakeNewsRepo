#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inquirer

"WHY: Scelta da un menù a tendina dell'argomento"


def WHY():
    questions = [inquirer.List('risposta', message="Does the article would like to convince you to buy some product or to change your opinion about some fact/person?", choices=['Yes', 'No'],),]
    answers = inquirer.prompt(questions)


    if answers["risposta"] == "Yes":
        score = 0
    else:
        score=1

    return score