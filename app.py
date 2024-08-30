from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np
popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name= list(popular_df['Book-Title'].values),
                           author= list(popular_df['Book-Author'].values),
                           image= list(popular_df['Image-URL-M'].values),
                           votes= list(popular_df['num-ratings'].values),
                           rating= list(popular_df['avg-ratings'].values),
                           )
@app.route('/autocomplete_books', methods=['POST'])
def autocomplete_books():
    query = request.form['query']
    matched_books = [book for book in books['Book-Title'] if query.lower() in book.lower()]
    suggestions = '\n'.join(matched_books[:4])  # Limit suggestions to 10
    return jsonify({'suggestions': suggestions})

@app.route('/recommend', methods=["POST", "GET"]) 
def recommend_ui():
        return render_template('recommend.html') 
  
  
@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input= request.form.get('user_input')
    if user_input not in pt.index:
        error_message = "This book isn't available."
        return render_template('recommend.html', error_message=error_message)

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1], reverse=True)[1:5]
    data=[]
    for i in similar_items:
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))

        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)

                        
                     



if __name__=='__main__':
    app.run(debug=True)