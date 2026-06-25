# Edit this file, then run:
#     scripts/build_site.py
#     update_github_repo.sh or manually add/commit/push
#     (one time) scripts/enable_github_pages.sh git@github.com:SmoothKen/ucsd-cse-153R-github-pages master /
# GitHub Pages serves static HTML. This Python file is build-time config;
# it is not executed by GitHub Pages in the browser/server.

# ----------------course identity-----------------

institution = "UCSD"
department = "CSE"
course = "153R"
term = "Summer 2026"
topic = "Machine Learning for Music & Audio"
timezone = "Pacific Time"
last_extracted = "2026-06-18"

course_code = f"{department} {course}"
short_title = f"{institution} {course_code}"
site_title = f"{short_title}: {topic}"
site_description = f"{topic} course site migrated from Google Sites to GitHub Pages."

# This changes automatically if course changes from "190" to another number.
course_slug = f"ucsd-cse-{course.lower()}"

# ----------------people-----------------

professor = "Shlomo Dubnov"
professor_email = "sdubnov@ucsd.edu"
professor_office_hours = "Zoom office hours: Mondays 8 AM - 9 AM"
professor_office_hours_url = "https://ucsd.zoom.us/j/97315192509"

ta = "Keren Shao"
ta_email = "k5shao@ucsd.edu"
ta_office_hours = "Zoom office hours: Thursdays 4 PM - 5 PM or by appointment"
ta_office_hours_url = "https://ucsd.zoom.us/my/k5shao"

# ----------------home links/notes-----------------

course_links = [
    {"label": "UCSD DataHub", "url": "https://datahub.ucsd.edu/", "note": "Recommended Jupyter Notebook programming environment"},
    {"label": "Canvas", "url": "https://canvas.ucsd.edu/courses/76569", "note": "Announcements, solutions, recordings, and private course material"},
    {"label": "Gradescope", "url": "https://www.gradescope.com/courses/1328914", "note": "Homework submission"},
    {"label": "Piazza", "url": "https://piazza.com/class/mqk3zewxiah1hd", "note": "Q&A"},
]

home_notes = [
    "Asynchronous course.",
    "Office hours occur during lecture-hour windows listed above.",
    "Gradescope and Piazza course enrollment codes are on Canvas.",
]

# ----------------syllabus top matter-----------------

prerequisite = "MATH 18 AND MATH 20B AND (CSE 103 or ECON 120A or MATH 183 or ECE 109 or MATH 180A or MATH 181A) or instructor approval. Programming ability in Python required. Musical skills are not required but would be an advantage."
enrollment = "Submit course clearance request via Enrollment Authorization System (EASy)."
description = "The course covers topics of Machine Learning dealing with music and audio signals, including basic concepts in digital signal processing, MIDI, audio analysis and feature extraction, temporal models including Markov and autoregressive models, and generative neural networks representation learning with applications to automatic music generation and sound synthesis. There will be several short programming assignments that correspond to the lecture materials. Students are given an option to choose between a more advanced final programming assignment set or performing a small group final project of their choice. Prior musical knowledge is not required but would be an advantage."


recording_notes = [
    "Recording links below direct to YouTube lecture recordings.",
    "For events specific to this course, such as office hours and project presentations, videos can be found on Canvas under Media Gallery.",
    "Please allow 24 hours for recording uploads. There can be a lag in Zoom processing, and some clips require editing.",
]

# ----------------lecture schedule-----------------

weeks = [
    {
        "week": "Week 1",
        "classes": [
            {
                "title": "Class 1",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1Sy3uJRgqTbGeFvPL3w5Hs7JjwG1byBGp/view?usp=sharing"}],
                "items": [
                    {"label": "Welcome Session, Syllabus Overview, and Introduction to Assignments", "note": "recording available on Canvas"},
                    {"label": "Features, Structures, and Representation of Sound and Music Data (MIDI, audio)", "url": "https://youtu.be/do8p-nkA7UM"},
                    {"label": "LMMS and Audio Tools", "url": "https://www.youtube.com/watch?v=n8z94IbYoic"},
                    {"label": "Audio features: pitch, timbre, loudness, MFCC, Chroma, Pitch", "url": "https://youtu.be/YY99OlXHB5g"},
                ],
            },
            {
                "title": "Class 2",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1QpnXxvC-opsmh1i44NQIz3bc2d98qEu4/view?usp=sharing"}],
                "items": [
                    {"label": "Aleatoric music, stochastic processes in music (Mozart Dice Game, Xenakis)", "url": "https://youtu.be/TyKmghiQ2QA"},
                    {"label": "Generative Music", "url": "https://youtu.be/yE3Z4b7zx7s"},
                    {"label": "Noise, Periodicity, Spectral Flatness, Perception and Cognition in Music Information Dynamics", "url": "https://youtu.be/I2FW3sjB-UY"},
                ],
            },
            {
                "title": "Class 3",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1UW_DkrUYpAfNYLg9wmQfeFV_V3aaCEfA/view?usp=sharing"}],
                "items": [
                    {"label": "Spectral Analysis, Fourier transform", "url": "https://youtu.be/FDZanwtZ4as"},
                    {"label": "Linear Filters and Convolution Theorem", "url": "https://youtu.be/bQsamazN9UY"},
                ],
            },
            {
                "title": "Class 4",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1xCIBwEOzqRQwhrJWMpsOK_cGvOf5ctMK/view?usp=sharing"}],
                "items": [
                    {"label": "Short Time Fourier Analysis, Perfect Reconstruction (COLA), and Griffin-Lim phase reconstruction", "url": "https://youtu.be/I2M8HfTXdV8"},
                ],
            },
        ],
    },
    {
        "week": "Week 2",
        "classes": [
            {
                "title": "Class 5",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1Be-K2PuHyYn-DuoEY1zAWX70mQpwZd07/view?usp=sharing"}],
                "items": [
                    {"label": "Information Theory and Music, Shannon’s Theorems for Compression and Rate-Distortion", "url": "https://youtu.be/mAlzCpTX9Vw"},
                    {"label": "Markov Models for Text and Music, Lempel-Ziv Algorithm and Musical Style", "url": "https://youtu.be/9pCeH-xw6H0"},
                    {"label": "Machine Improvisation", "url": "https://youtu.be/1o5zooFptFs"},
                ],
            },
            {
                "title": "Class 6",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1498etwKdlcI0YA84Z6xEeawNLcPhpR8m/view?usp=sharing"}],
                "items": [
                    {"label": "History of the voder / vocoder, Text to Speech", "url": "https://youtu.be/-zrXl2YL9TA"},
                    {"label": "Linear Prediction, Formants and Spectral Density", "url": "https://youtu.be/NtTYdYffalY"},
                    {"label": "Source Filter Model", "url": "https://www.youtube.com/watch?v=RnmWXmf-tYY"},
                    {"label": "OMax Software Demo", "url": "https://www.youtube.com/watch?v=pT-dUNrnxLM"},
                ],
            },
            {
                "title": "Class 7",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1rtYxC9BshjtBpRRYX3r7aBbVt7pOkcZi/view?usp=sharing"}],
                "items": [
                    {"label": "HMM (Hidden Markov Model) in Speech and Music", "url": "https://youtu.be/v4k_oWBZGeI"},
                    {"label": "Variable Markov Oracle (VMO), Music Information Dynamics", "url": "https://youtu.be/T37xMmap3g8"},
                ],
            },
            {
                "title": "Class 8",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1o0zPQZyOgwu6zlxH03x07gORUQyjJdOb/view?usp=sharing"}],
                "items": [{"label": "Introduction to Neural Networks & Keras", "url": "https://youtu.be/gcT7ASY7yXQ"}],
            },
        ],
    },
    {
        "week": "Week 3",
        "classes": [
            {"title": "Lecture on CNN & U-Net", "items": [{"label": "Lecture on CNN & U-Net", "url": "https://youtu.be/IfK9JG-TcXY"}]},
            {
                "title": "Class 9",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1tJ1jtG_L2EQNW59HBb5QHmneeBwkqANA/view?usp=sharing"}],
                "items": [
                    {"label": "Neural Network Models of Music", "url": "https://youtu.be/R8Yg3adZeNU"},
                    {"label": "Autoencoder (AE) and Feature Learning", "url": "https://youtu.be/x1wfqhJonDA"},
                ],
            },
            {
                "title": "Class 10",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1wjW9gzw8OYDKqnl1LfdSwXN3H0hG9q0F/view?usp=sharing"}],
                "items": [{"label": "Variational AE, ELBO", "url": "https://youtu.be/6VIBOP7U4Qw"}],
            },
            {
                "title": "Class 11",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1nuF71J9zLvoJMpwvmHumDSjjKy4vxJ5-/view?usp=sharing"}],
                "items": [
                    {"label": "Recurrent Neural Network for Music", "url": "https://youtu.be/ZYBjvBONmF0"},
                    {"label": "Generative Adversarial Networks", "url": "https://youtu.be/ntRkUrnxM2Q"},
                ],
            },
            {
                "title": "Class 12",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1QIZZ1gMGi2komIaXzgzsmBigxTx6Vl8c/view?usp=sharing"}],
                "items": [
                    {"label": "Transformers", "url": "https://www.youtube.com/watch?v=-Zkwgs1SuRY"},
                    {"label": "VAE Demo", "url": "https://youtu.be/ya44IoIGFKI"},
                    {"label": "Transformers & Word2Vec", "url": "https://www.youtube.com/watch?v=Co83y2nlqUo"},
                ],
            },
        ],
    },
    {
        "week": "Week 4",
        "classes": [
            {
                "title": "Class 13: Diffusion Models",
                "slides": [
                    {"label": "slides", "url": "https://drive.google.com/file/d/1Oyc3zpmPfsXq-ydXM26Z_e9RLFFUFYuB/view?usp=drive_link"},
                    {"label": "extra slides 1", "url": "https://drive.google.com/file/d/17by1su04chpwAYY3JMqeNrnKx9J_s873/view?usp=drive_link"},
                    {"label": "extra slides 2", "url": "https://drive.google.com/file/d/1bkQEmrPGemjdCDleajnI_7oeds5bOpHm/view?usp=drive_link"},
                ],
                "items": [
                    {"label": "Score Function and SDE", "url": "https://youtu.be/p8g1D20NMZM"},
                    {"label": "Generative Models and DDPM", "url": "https://youtu.be/GoAXcOqGG6k"},
                    {"label": "PF-ODE, DDIM and Consistency", "url": "https://youtu.be/mJ_4DraoRYY"},
                    {"label": "DSM Colab Simulation", "url": "https://youtu.be/SLdw6f6Dhdw"},
                    {"label": "Diffusion Guidance", "url": "https://youtu.be/n7v0HY5l1qs"},
                    {"label": "CLAP and Music Examples", "url": "https://youtu.be/0ERW7GHqGbk"},
                ],
            },
            {"title": "Project Proposal Presentations", "items": [{"label": "Project Proposal Presentations"}]},
            {"title": "Class 14", "items": [{"label": "Project Proposal Presentations"}]},
            {
                "title": "Class 15",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/1srV4PrDmYXUH79ahyJAbTM6BpbpmdESg/view?usp=sharing"}],
                "items": [
                    {"label": "Course Materials Review", "url": "https://www.youtube.com/watch?v=mJDibKm-L1g"},
                    {"label": "Note: There is no quiz in the class and this video is for review purposes only."},
                ],
            },
            {
                "title": "Class 16",
                "slides": [{"label": "slides", "url": "https://drive.google.com/file/d/18LaUo91ItgO8o9-iFeLk6hHWiByBgyip/view?usp=sharing"}],
                "items": [
                    {"label": "VMO Threshold, Deep Music Information Dynamics", "url": "https://www.youtube.com/watch?v=k1RuRD6Ub1U"},
                    {"label": "Creative Applications", "url": "https://www.youtube.com/watch?v=TSz5b19T-UM"},
                ],
            },
        ],
    },
    {
        "week": "Week 5",
        "classes": [{"title": "Project Presentations and Discussion", "items": [{"label": "Project Presentations and Discussion"}]}],
    },
]

# ----------------assignments-----------------

required_intro = "You are required to submit the following 6 programming assignments, each worth 10% of your grade. All due dates are for 11:59 PM Pacific Time."
choice_intro = "For the remaining 40% of the grade, you can choose to complete 4 additional assignments or a final project."

required_assignments = [
    {"number": 0, "title": "Introduction to Music Representation", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/Introduction%20to%20Music%20Representation.ipynb"},
    {"number": 1, "title": "Probability & Discrete Fourier Transform", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/Probability%20and%20Discrete%20Fourier%20Transform.ipynb"},
    {"number": 2, "title": "Spectrograms, Short-Time Fourier Transform, and Griffin-Lim", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/Spectrograms%2C%20STFT%20and%20Griffin-Lim%20Phase%20Reconstruction.ipynb"},
    {"number": 3, "title": "Markov & Lempel Ziv", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/Markov%20Chain%20and%20LZify.ipynb"},
    {"number": 4, "title": "Autoencoder De-noising", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/PCA%20with%20Linear%20Autoencoder.ipynb"},
    {"number": 5, "title": "RNN MIDI Generation", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/RNN%20MIDI%20Generation.ipynb"},
]


optional_assignments = [
    {"number": 6, "topic": "Digital Signal Processing", "title": "Speech Formants & LPC", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/Speech%20Formants%20with%20Linear%20Predictive%20Coding%20and%20Vocoder.ipynb"},
    # {"number": 7, "topic": "Shallow Learning", "title": "VMO Audio", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/VMO%20Audio%20Oracle%2C%20Information%20Rate%2C%20Generation%20by%20Recombination%2C%20and%20Query-based%20Resynthesis.ipynb"},
    # {"number": 8, "topic": "Deep Learning", "title": "CNN-RNN Genre Classification", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/CNN-RNN%20Genre%20Classification.ipynb"},
    # {"number": 6, "topic": "Deep Learning", "title": "GAN pix2pix & chroma", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/GAN%20pix2pix%20Chroma.ipynb"},
    {"number": 7, "topic": "Deep Learning", "title": "Transformer (GPT) for Music Generation", "options": [
        {"label": "PyTorch version", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/jazz_transformer_pytorch_ver.ipynb"},
        {"label": "TensorFlow/Keras version", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/jazz_transformer_tensorflow_ver.ipynb"},
    ]},
    {"number": 8, "topic": "Deep Learning", "title": "Diffusion/Style Transfer", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/diffusion_student_ver/homework4_diffusion_assignment.ipynb"},
    {"number": 9, "topic": "Deep Learning", "title": "Improvisation Voice Agent", "url": "https://github.com/SmoothKen/ucsd-cse-153R-github-pages/blob/master/homework/voice_agents_student_ver/submission.py"},
]





# Mirror assignment deadlines to the course year's July calendar.
# Python weekdays: Monday=0, Wednesday=2, Friday=4, Saturday=5.
from datetime import date, timedelta

assignment_year = int(term.split()[-1])

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5

def july_weekday(n, weekday):
    d = date(assignment_year, 7, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7, weeks=n - 1)
    return f"{d.month}/{d.day}"

for i, due_week, self_grade_week in [
    (0, 1, 2),
    (1, 1, 2),
    (2, 2, 3),
    (3, 2, 3),
    (4, 3, 4),
    (5, 3, 4),
]:
    required_assignments[i]["due"] = july_weekday(due_week, SATURDAY)
    required_assignments[i]["self_grade_due"] = july_weekday(self_grade_week, WEDNESDAY)

optional_due = july_weekday(5, THURSDAY)
optional_self_grade_due = july_weekday(5, SATURDAY)





project = {
    "title": "Final Project",
    "url": "https://drive.google.com/file/d/1ILRju3uoe4Rf_vzHJU2KE4lX8fJ_3gHE/view?usp=sharing",
    "milestones": [
        {"label": "Project Proposal", "weight": "10%", "due": july_weekday(4, WEDNESDAY)},
        {"label": "Presentation", "weight": "15%", "due": f"{july_weekday(5, WEDNESDAY)} recorded + live Q&A session on {july_weekday(5, THURSDAY)} during Keren's Wednesday office hours"},
        {"label": "Report", "weight": "15%", "due": optional_self_grade_due},
    ],
    "previous_projects_url": "https://drive.google.com/drive/folders/1kDGynccVlXuGgM0RzlfUTYNLqQs1vLfX?usp=sharing",
}

self_grading_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdlNjPimuBSKSwlVJnav5MsH6wNqLnn39TeLpBncbrRdjK4IQ/viewform?usp=sf_link"
self_grading_instructions = [
    "After the homework deadline, solutions will be posted online on Canvas. Students are expected to read the solutions and enter their own scores and comments for every part of every problem using the self-grading form.",
    "After filling out the form, upload a corrected version of the assignment to Gradescope.",
    "If you made mistakes in the initial submission, use the posted solutions to correct your submission.",
    "If you think you solved the homework perfectly, you can resubmit the original work, but critical self-evaluation and improvements are encouraged.",
    "If you lose points on the initial submission, you can earn up to 5 points back if the corrected version successfully corrects the mistakes.",
]

# ----------------resources-----------------

resources = [
    {"label": "Deep & Shallow: Machine Learning in Music and Audio", "url": "https://www.routledge.com/Deep-and-Shallow-Machine-Learning-in-Music-and-Audio/Dubnov-Greer/p/book/9781032133911"},
    {"label": "Music Information Retrieval", "url": "https://musicinformationretrieval.com/"},
    {"label": "Audio Content Analysis", "url": "https://www.audiocontentanalysis.org/"},
    {"label": "Course Readings", "url": "https://drive.google.com/drive/folders/1g6625TkfabNHLzVNYzeKsRAyxsJS9kD1?usp=sharing"},
    {"label": "Course Videos playlist", "url": "https://youtube.com/playlist?list=PLgYzBgzekNBXMhJXv4ln9QcauHtnKK82o"},
    {"label": "Past Project Presentations: Day 1", "url": "https://ucsd.zoom.us/rec/share/FQW0eWQOfC5dL0P0gFvQYEEJ7w6pWKZhlbqGMF0LrQ5CFzO-9TS3l11rYhnZL4BU.9RsRtw4UsiLBFDPk?startTime=1630465481000", "note": "pw: mlmusic1!"},
    {"label": "Past Project Presentations: Day 2", "url": "https://ucsd.zoom.us/rec/share/WQOcJugBO0ANd3mmJ4UIOyo5yUnL27CVhOwvJgcRCrF0iELZZwZgDN7Cdr9aMIrn.p8N2nfX_BukwiNsS?startTime=1630552034000", "note": "pw: mlmusic1!"},
]

fun_resources = [
    {"label": "Nvidia / AVIA music making workshop", "url": "https://www.nvidia.com/en-us/on-demand/session/gtcspring21-se2345/"},
    {"label": "AWS DeepComposer", "url": "https://aws.amazon.com/deepcomposer/"},
    {"label": "Google Magenta", "url": "https://research.google/teams/brain/magenta/"},
    {"label": "FB Universal Music Translation Network", "url": "https://research.fb.com/publications/a-universal-music-translation-network/"},
    {"label": "IRCAM OMax Project", "url": "https://recherche.ircam.fr/equipes/repmus/OMax/"},
]

# ----------------assembled data consumed by scripts/build_site.py-----------------

course_data = {
    "site": {
        "title": site_title,
        "term": term,
        "short_title": short_title,
        "description": site_description,
        "timezone": timezone,
        "last_extracted": last_extracted,
    },
    "people": [
        {"role": "Professor", "name": professor, "email": professor_email, "office_hours": professor_office_hours, "office_hours_url": professor_office_hours_url},
        {"role": "TA", "name": ta, "email": ta_email, "office_hours": ta_office_hours, "office_hours_url": ta_office_hours_url},
    ],
    "course_links": course_links,
    "home_notes": home_notes,
    "syllabus": {
        "recording_notes": recording_notes,
        "prerequisite": prerequisite,
        "enrollment": enrollment,
        "description": description,
    },
    "weeks": weeks,
    "assignments": {
        "required_intro": required_intro,
        "choice_intro": choice_intro,
        "required": required_assignments,
        "optional_due": optional_due,
        "optional_self_grade_due": optional_self_grade_due,
        "optional": optional_assignments,
        "project": project,
        "self_grading": {"form_url": self_grading_form_url, "instructions": self_grading_instructions},
    },
    "resources": resources,
    "fun_resources": fun_resources,
}
