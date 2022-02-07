from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app = Flask(__name__)

#defining database administration
ENV ='prod'
if ENV =='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:developer15@localhost/cardealership'

else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://lmfcerprhsptog:e22fbe18692083efb6f02695da0e24bdf0f7ce3c5aa32b2d9a3ecad5cd0eec13@ec2-54-235-98-1.compute-1.amazonaws.com:5432/d1bsqpf2k6eqeq'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db =SQLAlchemy(app)#SQLAlchemy works by creating models

class Feedback(db.Model):
    __tablename__='feedback'
    id=db.Column(db.Integer, primary_key=True)
    customer=db.Column(db.String(100))
    dealer=db.Column(db.String(100))
    rating=db.Column(db.Integer)
    comments=db.Column(db.Text())

    #Constructior or initializer
    def __init__(self, customer, dealer, rating, comments):
        self.customer=customer
        self.dealer=dealer
        self.rating=rating
        self.comments=comments



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method=='POST':
        customer=request.form['customer']
        dealer=request.form['dealer']
        rating = request.form['rating']
        comments=request.form['comments']

        print(customer,dealer,rating,comments)
        if customer=='' or dealer=='':
            return render_template('index.html', message='Please enter required fields')
        #checking if the customer exist and if they dont add them to the database
        if db.session.query(Feedback).filter(Feedback.customer==customer).count()==0:
            data = Feedback(customer,dealer,rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted a feedback')



if __name__=='__main__':
    app.run()
