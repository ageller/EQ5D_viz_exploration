# from Claude (will need to confirm this is correct)

# EQ-5D-5L Questions and Response Options
eq5d_questions = {
    "mobility": {
        "type": "dropdown",
        "question": "MOBILITY",
        "options": {
            1: "I have no problems in walking about",
            2: "I have slight problems in walking about",
            3: "I have moderate problems in walking about",
            4: "I have severe problems in walking about",
            5: "I am unable to walk about"
        }
    },
    "selfcare": {
        "type": "dropdown",
        "question": "SELF-CARE",
        "options": {
            1: "I have no problems washing or dressing myself",
            2: "I have slight problems washing or dressing myself",
            3: "I have moderate problems washing or dressing myself",
            4: "I have severe problems washing or dressing myself",
            5: "I am unable to wash or dress myself"
        }
    },
    "usual_activities": {
        "type": "dropdown",
        "question": "USUAL ACTIVITIES (e.g. work, study, housework, family or leisure activities)",
        "options": {
            1: "I have no problems doing my usual activities",
            2: "I have slight problems doing my usual activities",
            3: "I have moderate problems doing my usual activities",
            4: "I have severe problems doing my usual activities",
            5: "I am unable to do my usual activities"
        }
    },
    "pain": {
        "type": "dropdown",
        "question": "PAIN / DISCOMFORT",
        "options": {
            1: "I have no pain or discomfort",
            2: "I have slight pain or discomfort",
            3: "I have moderate pain or discomfort",
            4: "I have severe pain or discomfort",
            5: "I have extreme pain or discomfort"
        }
    },
    "anxiety": {
        "type": "dropdown",
        "question": "ANXIETY / DEPRESSION",
        "options": {
            1: "I am not anxious or depressed",
            2: "I am slightly anxious or depressed",
            3: "I am moderately anxious or depressed",
            4: "I am severely anxious or depressed",
            5: "I am extremely anxious or depressed"
        }
    },
    "health_today": {
        "type": "slider",
        "question": "YOUR HEALTH TODAY",
        "instructions": "Please let us know how good or bad your health is TODAY. 0 indicated the worst health you can imagine.  100 indicates the best health you can imagine.",
        "min_val": 0,
        "max_val":100,
        "initial_val":50,
        "step":1
    }
}

