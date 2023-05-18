import os
import time
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_string = '''I would like you now to take the list of words expressed most prevalently in a sentiment cloud (IGNORING words
    like "Tweet," "Appeal," "Demographic," "Audience," "Engage," "Enhance," "Tweet," "Incorporate," and "Improvements,") and the
    explanations for the appeal of this social media post to each demographic segment, and rewrite the post so that it would score higher on
    a ranking of weighted favorability to most of these groups, by incorporating the suggestions in the analysis, and incorporating
    the words and themes in this word cloud. Make as few revisions as possible to influence favorability. Keep in mind that posts are short, 280 characters or less, and keep in mind the importance of striking a balance 
    and to maintain the authenticity, voice, perspective, and original intent of the post. DO NOT WRITE PROMOTION OR ADVERTISEMENT COPY, unless it is clear that promotion is the original
    intention of the post. If the original post is a joke, your post should also be a best attempt at improving the joke. Avoid coming across as clickbaity
    or desparate for engagement. Do NOT use topic hashtags at the end of your tweet. If your response contains a '#' (pound symbol) I will regenerate your response.
    Summarize how your changes reflect an overall similarity in authorial voice, perspective, and intention, but do not print or otherwise reveal this summary; it is simply a check of the appropriateness of the revisions.
    After "Rewritten:" print the result in 280 characters or less, nothing else.'''

def completeAI(system_content, user_content):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
                
            ],
            temperature=1.0)
    time.sleep(30)
    return response['choices'][0]['message']['content']

@app.route("/", methods=("GET", "POST"))
def index():
    
    if request.method == "POST":
        tweet = request.form["tweet"]
        response, demo_analysis, word_cloud = improve_tweet(tweet)
        if len(response) > 280:
            new_tweet = response
            response = truncate(tweet, new_tweet, word_cloud, demo_analysis)
        return redirect(url_for("index", result=response, tweet=tweet))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_analysis(tweet):
    user_content = """Analyze this post by grouping by similarity between the people who like it: what demographics,
    alignments, groups or clusters they might they belong to, based on the information in common about them. Create analysis. Take the
    following post, and based on the limited information you have in the content of the post, analyze it in terms of the 3 demographic
    segments of highest likelihood of this post's favorability, explain the meaning of this tweet, why it is likely that this post would appeal to each of these principal demographics,
    suggest alterations and additions such that the post might improve its performance among these groups, based on why the post appeals to each demographic:
    
    Post:
    {} """.format(tweet)
    
    system_content = '''You are a social media archivist/modern cultural anthropologist, who wants to help me interpret this social media post, in context.
    You do not care about profanity as you are a cultural researcher and are able to maintain a relative perspective on cultural values without censoring inappropriate content.'''
    
    return completeAI(system_content, user_content)
    
      
def generate_word_cloud(demo_analysis):
    user_content='''Look for the most common words and sentiments and distill them into a list sorted by prevalence: most
    to least common, just like a word cloud of the descriptive words in this analysis a social media archivist/modern cultural anthropologist just wrote: {}'''.format(demo_analysis)
    
    system_content = 'You are accessing the database of a social media archivist/modern cultural anthropologist, who wants to help me interpret a social media post, in context. '
               
    return completeAI(system_content, user_content)
    
def improve_favorability(tweet, demo_analysis, word_cloud):
    
    user_content=prompt_string + '''
    
    list of words:
    
    {}
    
    analysis:
    
    {}
    
    Tweet:
    
    {}
    
    Rewritten:
    '''.format(word_cloud, demo_analysis, tweet)
    
    system_content = 'You are a social media archivist/modern cultural anthropologist, who wants to help me interpret this social media post, in context.'
    
    return completeAI(system_content, user_content)
    
def improve_tweet(tweet):
    demo_analysis = generate_analysis(tweet)
    word_cloud = generate_word_cloud(demo_analysis)
    improved_tweet = improve_favorability(tweet, demo_analysis, word_cloud)
    
    return improved_tweet, demo_analysis, word_cloud
    
def truncate(tweet, new_tweet, demo_analysis, word_cloud):
    charcount = len(new_tweet)
    user_content='''Here is what you wrote:
    
    {}
    
    which is {} characters. That output was greater than 280 characters; you need to truncate it to 280 characters or less. Please rewrite the tweet again but be mindful of character limits.
    
    ''' + prompt_string + '''
    analysis:
    
    {}
    
    word cloud:
    
    {}
    
    Tweet:
    
    {}
    
    Rewritten:
    '''.format(new_tweet, charcount, word_cloud, demo_analysis, tweet)
    
    system_content = '''You are a social media archivist/modern cultural anthropologist, who wants to help me interpret this social media post, in context.
    You do not care about profanity as you are a cultural researcher and are able to maintain a relative perspective on cultural values without being normative about censoring inappropriate content.'''
    
    return completeAI(system_content, user_content)
    

