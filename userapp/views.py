from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.views import debug
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from django.conf import settings
from userapp.models import *
import urllib.request
import time
from adminapp.models import *
import urllib.parse
import random
import re
import pickle
import string
import pickletools
import re
from pathlib import Path
from nltk.stem import WordNetLemmatizer
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Create your views here.
def sendSMS(user, otp, mobile):
    data = urllib.parse.urlencode({
        'username': 'Codebook',
        'apikey': '56dbbdc9cea86b276f6c',
        'mobile': mobile,
        'message': f'Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you',
        'senderid': 'CODEBK'
    })
    data = data.encode('utf-8')
    # Disable SSL certificate verification
    # context = ssl._create_unverified_context()
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data)
    return f.read()


def user_index(request):
    return render(request, 'user/index.html')

def user_register(req):
    if req.method == "POST":
        username = req.POST.get('user_name')
        email = req.POST.get('email_address')
        password = req.POST.get('email_password')
        number = req.POST.get('contact_number')
        file = req.FILES['user_file']
        print(req)
        print(username,email,password,number,file,"register")
        otp=str(random.randint(1000,9999))
        print(otp, "generate otp")
        try:
            user_data = UserDetails.objects.get(user_email=email)
            return redirect("register")
        except:
            mail_message=f"register successfully \nYour four digit pin is below \n {otp}"
            print(mail_message)
            send_mail("student password",mail_message,settings.EMAIL_HOST_USER, [email]) #we take the register name variable in this case which is "email"
            #send SMS
            sendSMS(username, otp, number)

            UserDetails.objects.create(otp=otp, user_contact = number, user_username = username, user_email = email, user_password = password, user_file = file)
            req.session["user_email"] = email
            return redirect ("otp")
    return render(req, 'user/register.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        email = request.POST.get('email_address')
        password = request.POST.get('email_password')
        number = request.POST.get('contact_number')
        file = request.FILES['user_file']
        print(request)
        print(username, email, password, number, file, 'data')
        otp = str(random.randint(1000, 9999))
        print(otp, 'generated otp')
        try:
            UserDetails.objects.get(user_email = email)
            messages.info(request, 'mail already registered')
            return redirect('register')
        except:
            mail_message = f'Registration Successfully\n Your 4 digit Pin is below\n {otp}'
            print(mail_message)
            send_mail("Student Password", mail_message , settings.EMAIL_HOST_USER, [email])
            # text message
            sendSMS(username, otp, number)
        
            UserDetails.objects.create(otp=otp, user_contact = number, user_username = username, user_email = email, user_password = password, user_file = file)
            request.session['user_email'] = email
            return redirect('otp')
    return render(request, 'user/register.html')

def user_about(request):
    return render(request, 'user/about.html')

def user_blog(request):
    return render(request, 'user/blog.html')

def user_userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email_address')
        password = request.POST.get('email_password')
        print(email, password)
        try:
            user = UserDetails.objects.get(user_email = email, user_password = password)
            print(user)
            request.session['user_id'] = user.user_id
            a = request.session['user_id']
            print(a)

            if user.user_password ==  password :
                if user.user_status == 'Accepted':
                    if user.otp_status == 'verified':
                        messages.success(request,'login successfull')
                        request.session['user_id'] = user.user_id
                        print('login sucessfull')
                        user.No_Of_Times_Login += 1
                        user.save()
                        return redirect('dashboard')
                    else:
                         return redirect('otp')
                elif user.user_password ==  password and user.user_status == 'Rejected':
                    messages.warning(request,"you account is rejected")
                else:
                    messages.info(request,"your account is in pending")
            else:
                 messages.error(request,'Login credentials was incorrect...')
        except:
            print(';invalid credentials')
            print('exce')
            return redirect('user')
    return render(request, 'user/user.html')

def user_otp(request):
    user_id = request.session['user_email']
    user =UserDetails.objects.get(user_email = user_id)
    messages.success(request, 'OTP  Sent successfully')
    print(user_id)
    print(user, 'user avilable')
    print(type(user.otp))
    print(user. otp, 'creaetd otp')   
    if request.method == 'POST':
        u_otp = request.POST.get('otp')
        u_otp = int(u_otp)
        print(u_otp, 'enter otp')
        if u_otp == user.otp:
            print('if')
            user.otp_status  = 'verified'
            user.save()
            messages.success(request, 'OTP  verified successfully')
            return redirect('user')
        else:
            print('else')
            messages.error(request, 'Invalid OTP') 
            return redirect('otp')
    return render(request, 'user/otp.html')

def user_admin(request):
    admin_name = 'admin@gmail.com'
    admin_password = 'admin'
    if request.method == 'POST':
        adminemail = request.POST.get('emailaddress')
        adminpassword = request.POST.get('emailpassword')
        if admin_name == adminemail and admin_password == adminpassword:
            return redirect('admin_dashboard')
        else:
            return redirect('admin')
    return render(request, 'user/admin.html')

def user_contact(request):
    return render(request, 'user/contact.html')

def user_dashboard(request):
    prediction_count =  UserDetails.objects.all().count()
    user_id = request.session["user_id"]
    user = UserDetails.objects.get(user_id = user_id)
    return render(request, 'user/dashboard.html', {'predictions' : prediction_count, 'la' : user})

def user_myprofile(request):
    views_id = request.session['user_id']
    user = UserDetails.objects.get(user_id = views_id)
    print(user, 'user_id')
    if request.method =='POST':
        username = request.POST.get('user_name')
        email = request.POST.get('email_address')
        number = request.POST.get('contact_number')
        password = request.POST.get('email_password')
        date = request.POST.get('date')
        print(username, email, number, password, date,  'data') 

        user.user_username = username
        user.user_email = email
        user.user_contact = number
        user.user_password = password
        user.user_dates = date 

        if len(request.FILES)!=0:
            file = request.FILES['user_file']
            user.user_file = file

            user.user_username = username
            user.user_email = email
            user.user_contact = number
            user.user_password = password
            user.save()
        else:
            user.user_username = username
            user.user_email = email
            user.user_contact = number
            user.user_password = password
            user.save()


    return render(request, "user/myprofile.html", {'i':user})


wo = WordNetLemmatizer()

def preprocess(data):
    text = str(data).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = ' '.join(wo.lemmatize(word) for word in text.split())
    return text

import os
import pickle
import numpy as np
from scipy.sparse import hstack
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

# =========================
# LOAD MODEL & VECTORIZER
# =========================
vectorizer = None
model = None


def _find_existing_file(*relative_paths):
    base_dir = Path(settings.BASE_DIR)
    for relative_path in relative_paths:
        candidate = base_dir / relative_path
        if candidate.exists():
            return candidate
    searched_paths = ", ".join(str(base_dir / path) for path in relative_paths)
    raise FileNotFoundError(f"Required file not found. Checked: {searched_paths}")


def load_detection_assets():
    global vectorizer, model

    if vectorizer is not None and model is not None:
        return vectorizer, model

    vectorizer_path = _find_existing_file(
        "Email_spam/vectorizer.pkl",
        "vectorizer.pkl",
    )
    model_path = _find_existing_file(
        "Email_spam/xgboost_model.pkl",
        "xgboost_model.pkl",
    )

    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    return vectorizer, model

# =========================
# OPTIONAL: Digital Density (if used in training)
# =========================
def digital_density(text):
    digits = sum(c.isdigit() for c in text)
    return digits / len(text) if len(text) > 0 else 0


def get_xgboost_chart_context():
    xgb_result = XG_ALGO.objects.last()
    return {
        'xgb_name': getattr(xgb_result, 'Name', 'XG Boost Algorithm'),
        'xgb_accuracy': float(getattr(xgb_result, 'Accuracy', 0) or 0),
        'xgb_precision': float(getattr(xgb_result, 'Precession', 0) or 0),
        'xgb_f1_score': float(getattr(xgb_result, 'F1_Score', 0) or 0),
        'xgb_recall': float(getattr(xgb_result, 'Recall', 0) or 0),
    }

# =========================
# VIEW FUNCTION
# =========================
def user_detection(req):
    if req.method == 'POST':
        try:
            loaded_vectorizer, loaded_model = load_detection_assets()
        except FileNotFoundError as exc:
            messages.error(req, str(exc))
            return render(req, 'user/detection.html', {'final_result': "Model files are missing."})

        msg = req.POST.get('mood_pred', '')

        # preprocess text
        a = preprocess(msg)

        # TF-IDF transform
        X_text = loaded_vectorizer.transform([a])

        # 🔥 If you USED digital density in training → keep this
        dd = np.array([digital_density(a)]).reshape(-1, 1)
        X_input = hstack((X_text, dd))

        # 🔥 If NOT used → use this instead:
        # X_input = X_text

        # prediction
        pred = loaded_model.predict(X_input)[0]

        print(pred, "<<< Prediction >>>")

        if pred == 0:
            messages.success(req, 'Result = Normal')
            return render(req, 'user/result.html', {'final_result': "Normal"})

        elif pred == 1:
            messages.warning(req, 'Result = Fraud')
            return render(req, 'user/result.html', {'final_result': "Fraud"})

        # optional session
        req.session['res'] = pred

    return render(req, 'user/detection.html')

def user_feedback(request):
    views_id = request.session['user_id']
    user = UserDetails.objects.get(user_id = views_id)
    if request.method == 'POST':
        u_feedback = request.POST.get('feedback')
        u_rating = request.POST.get('rating')
        if not user_feedback:
            return redirect('')
        sid=SentimentIntensityAnalyzer()
        score=sid.polarity_scores(u_feedback)
        sentiment=None
        if score['compound']>0 and score['compound']<=0.5:
            sentiment='positive'
        elif score['compound']>=0.5:
            sentiment='very positive'
        elif score['compound']<-0.5:
            sentiment='very negative'
        elif score['compound']<0 and score['compound']>=-0.5:
            sentiment='negative'
        else :
            sentiment='neutral'
        messages.success(request,'Feedback sent successfully')

        print(sentiment)
        user.star_feedback=u_feedback
        user.star_rating = u_rating
        user.save()
        UserFeedbackModels.objects.create(user_details = user, star_feedback = u_feedback, star_rating = u_rating, sentment= sentiment)
        rev=UserFeedbackModels.objects.filter()

    return render(request, 'user/feedback.html')

def user_result(request):
    result = request.session.get('res')
    if result == 0:
            messages.success(request, 'Result = Normal')
            context = {'final_result': "Normal"}
            context.update(get_xgboost_chart_context())
            return render(request, 'user/result.html', context)

    elif result == 1:
            messages.warning(request, 'Result = Fraud')
            context = {'final_result': "Fraud"}
            context.update(get_xgboost_chart_context())
            return render(request, 'user/result.html', context)
    context = {'resul': result}
    context.update(get_xgboost_chart_context())
    return render(request, "user/result.html", context) 

def userlogout(request):
    view_id = request.session["user_id"]
    user = UserDetails.objects.get(user_id = view_id) 
    t = time.localtime()
    user.Last_Login_Time = t
    current_time = time.strftime('%H:%M:%S', t)
    user.Last_Login_Time = current_time
    current_date = time.strftime('%Y-%m-%d')
    user.Last_Login_Date = current_date
    user.save()
    messages.info(request, 'You are logged out..')
    # print(user.Last_Login_Time)
    # print(user.Last_Login_Date)
    return redirect('user')


def user_detection(req):
    if req.method == 'POST':
        try:
            loaded_vectorizer, loaded_model = load_detection_assets()
        except FileNotFoundError as exc:
            messages.error(req, str(exc))
            return render(req, 'user/detection.html', {'final_result': "Model files are missing."})

        msg = req.POST.get('mood_pred', '')
        processed_text = preprocess(msg)
        X_text = loaded_vectorizer.transform([processed_text])
        model_feature_count = getattr(loaded_model, 'n_features_in_', X_text.shape[1])

        if model_feature_count == X_text.shape[1]:
            X_input = X_text
        elif model_feature_count == X_text.shape[1] + 1:
            dd = np.array([digital_density(processed_text)]).reshape(-1, 1)
            X_input = hstack((X_text, dd))
        else:
            messages.error(
                req,
                f"Model expects {model_feature_count} features, but the app generated {X_text.shape[1]}.",
            )
            return render(req, 'user/detection.html', {'final_result': "Model feature mismatch."})

        pred = int(loaded_model.predict(X_input)[0])
        req.session['res'] = pred

        if pred == 0:
            messages.success(req, 'Result = Normal')
            context = {'final_result': "Normal"}
            context.update(get_xgboost_chart_context())
            return render(req, 'user/result.html', context)

        if pred == 1:
            messages.warning(req, 'Result = Fraud')
            context = {'final_result': "Fraud"}
            context.update(get_xgboost_chart_context())
            return render(req, 'user/result.html', context)

    return render(req, 'user/detection.html')
