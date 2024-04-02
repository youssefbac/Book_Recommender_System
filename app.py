from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
pop_df = pd.read_pickle('pop.pkl')
books_df = pd.read_pickle('books.pkl')
with open('similarity_score.pkl', 'rb') as file:
    similarity = pickle.load(file)
pt = pd.read_pickle('pt.pkl')
app = Flask(__name__)




@app.route('/')
def index():
    return render_template('Index.html',
                           book_name=list(pop_df['Book-Title'].values),
                           author=list(pop_df['Book-Author'].values),
                           image=list(pop_df['Image-URL-M'].values),
                           votes=list(pop_df['num_ratings'].values),
                           rating=list(pop_df['avg_ratings'].values)

                           )


@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def to_recommend():
        user_input = request.form.get('input')
        index = np.where(pt.index == user_input)[0][0]
        # get the top 6 similar items to the first Book_Title
        similarity_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similarity_items:
            item = []
            temp_df = books_df[books_df['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        print(data)
        return render_template('recommend.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)
