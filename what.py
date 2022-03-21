#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


"WHAT: Scelta da un menù a tendina dell'argomento"


"Creazione del dataframe con gli argomenti"
def WHAT():
    argomenti = {'Topic': ['No topic can be identified','News item','Scientific publication','Dogma','Maximum phrase','Political propaganda','Commercial propaganda','Satire']}
    df_Argomenti = pd.DataFrame(data=argomenti)
    df_Argomenti.head()
    
    
    "Scegliere un argomento per il What"
    
    import inquirer
    questions = [
      inquirer.List('topic',
                    message="Which of these accurately describes the topic of the text?",
                    choices=df_Argomenti['Topic'].tolist(),
                ),
    ]
    answers = inquirer.prompt(questions)
    
    
    if (answers["topic"] == 'No topic can be identified'):
        score=0
    elif (answers["topic"] == 'News item' or answers["topic"] == 'Scientific publication'):
        score=1
    else:
        score=0.5
    return(score)


