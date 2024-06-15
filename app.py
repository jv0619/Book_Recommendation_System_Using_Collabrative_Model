from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from pickle import load


popular_df = pd.read_pickle('pickle_files/popular.pkl')
pt = pd.read_pickle('pickle_files/pt.pkl')
books = pd.read_pickle('pickle_files/books.pkl')
similarity_scores = pd.read_pickle('pickle_files/similarity_scores.pkl')
searchable_list = load(open('pickle_files/searchable_books.pkl','rb'))



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/info')
def info_page():
    return render_template('project_info.html', image=list(popular_df['Image-URL-M'].values))

@app.route('/team')
def team_page():
    return render_template('team.html')

@app.route('/recommend')
def recommend_ui():
    # books_list = list(books['Book-Title'].values)
    books_list = searchable_list
    return render_template('recommendation.html',booksList=books_list, recommendPage=1)

@app.route('/recommend_books',methods=['post'])
def recommend():
    # books_list = list(books['Book-Title'].values)
    books_list = searchable_list
    user_input = request.form.get('user_input')
    data = []
    if user_input in books_list:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:6]

        
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        print(data)

        return render_template('recommendation.html',data=data, usrInput=user_input.title(), booksList=books_list)
    else:
        return render_template('recommendation.html', data=data, usrInput=user_input,booksList=books_list)


if __name__ == '__main__':
    app.run(debug=True)