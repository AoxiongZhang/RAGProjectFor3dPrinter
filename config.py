GRAPH_TEMPLATE = {
    'stringing_definition': {
        'slots': ['error'],
        'question': 'What is stringing or oozing in 3D printing? / Can you explain stringing?',
        'cypher': "MATCH (e:Error) WHERE e.name='stringing' OR e.name='oozing' RETURN e.description AS RES",
        'answer': 'Stringing/Oozing: %RES%',
    },
    'stringing_cause': {
        'slots': ['error'],
        'question': 'What causes stringing or oozing? / Why does stringing happen during 3D printing?',
        'cypher': "MATCH (e:Error) WHERE e.name='stringing' OR e.name='oozing' RETURN e.cause AS RES",
        'answer': 'Causes of stringing/oozing: %RES%',
    },
    'stringing_solution': {
        'slots': ['error'],
        'question': 'How can I reduce stringing? / How to fix oozing in my prints?',
        'cypher': "MATCH (e:Error)-[:HAS_SOLUTION]->(s:Solution) WHERE e.name='stringing' OR e.name='oozing' RETURN s.description AS RES",
        'answer': 'Ways to reduce stringing/oozing: %RES%',
    },
    'retraction_setting': {
        'slots': ['setting'],
        'question': 'What retraction settings help prevent stringing? / How should I set retraction distance and speed?',
        'cypher': "MATCH (s:Setting) WHERE s.type='retraction' RETURN s.recommendation AS RES",
        'answer': 'Recommended retraction settings: %RES%',
    },
    'temperature_setting': {
        'slots': ['material'],
        'question': 'What is the best temperature to avoid stringing with %material%? / How should I set the nozzle temperature for %material%?',
        'cypher': "MATCH (m:Material) WHERE m.name='%material%' RETURN m.anti_stringing_temperature AS RES",
        'answer': 'Recommended nozzle temperature for [%material%] to reduce stringing: %RES%',
    },
    'benchy_line_definition': {
        'slots': ['error'],
        'question': 'What is the Benchy hull line? / Why does my Benchy print have a visible line?',
        'cypher': "MATCH (e:Error) WHERE e.name='Benchy hull line' RETURN e.description AS RES",
        'answer': 'Benchy hull line: %RES%',
    },
    'benchy_line_cause': {
        'slots': ['error'],
        'question': 'What causes the Benchy hull line? / Why is there a line on my Benchy print?',
        'cypher': "MATCH (e:Error) WHERE e.name='Benchy hull line' RETURN e.cause AS RES",
        'answer': 'Causes of Benchy hull line: %RES%',
    },
    'benchy_line_solution': {
        'slots': ['error'],
        'question': 'How can I eliminate the Benchy hull line? / What can I do to fix the Benchy hull line?',
        'cypher': "MATCH (e:Error)-[:HAS_SOLUTION]->(s:Solution) WHERE e.name='Benchy hull line' RETURN s.description AS RES",
        'answer': 'Solution for Benchy hull line: %RES%',
    },
    # 通用项可保留，也可以加入下面这些
    'printer_feature_list': {
        'slots': ['printer'],
        'question': 'What are the features of %printer%?',
        'cypher': "MATCH (n:Printer)-[:HAS_FEATURE]->(f:Feature) WHERE n.name='%printer%' RETURN COLLECT(f.name) AS RES",
        'answer': 'Main features of [%printer%]: %RES%',
    },
    'material_compatibility': {
        'slots': ['printer'],
        'question': 'Which materials can %printer% print with?',
        'cypher': "MATCH (n:Printer)-[:SUPPORTS_MATERIAL]->(m:Material) WHERE n.name='%printer%' RETURN COLLECT(m.name) AS RES",
        'answer': '[%printer%] supports these materials: %RES%',
    },
}
