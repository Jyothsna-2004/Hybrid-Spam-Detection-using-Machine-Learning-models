from django.shortcuts import render,redirect
from userapp.models import*
from adminapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from sklearn.ensemble  import AdaBoostClassifier
from sklearn.svm  import SVC
from django.core.paginator import Paginator
from xgboost import XGBClassifier
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import re
import string
import pickle
from pathlib import Path

# Create your views
def admin_dashboard(req):
    all_users_count =  UserDetails.objects.all().count()
    pending_users_count = UserDetails.objects.filter(user_status = 'Pending').count()
    rejected_users_count = UserDetails.objects.filter(user_status = 'removed').count()
    accepted_users_count =UserDetails.objects.filter(user_status = 'accepted').count()
    Feedbacks_users_count= UserFeedbackModels.objects.all().count()
    return render(req,'admin/dashboard.html',{'a' : all_users_count, 'b' : pending_users_count, 'c' : rejected_users_count, 'd' : accepted_users_count, 'e':Feedbacks_users_count})

def adminpendingusers(req):
    pending = UserDetails.objects.filter(user_status = 'Pending')
    paginator = Paginator(pending, 5) 
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,'admin/pending_user.html', { 'user' : post})

def adminallusers(req):
    all_users  = UserDetails.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,'admin/all_user.html', {"allu" : all_users, 'user' : post})

def Change_Status(req,id):
    # user_id=req.session["User_id"]
    user=UserDetails.objects.get(user_id=id)
    if user.user_status=="Accepted":
        user.user_status=="Rejected"
        user.save()
        messages.success(req,"Status Changed Successfully")

        return redirect("adminallusers")
    
    else:
        user.user_status="Accepted"
        user.save()
        messages.success(req,"Status Successfully Changed")

        return redirect("adminallusers")



def accept_user(req, id):
    status_update = UserDetails.objects.get(user_id = id)
    status_update.user_status = 'Accepted'
    status_update.save()
    messages.success(req, 'User was accepted..!')
    return redirect('adminpendingusers')

def reject_user(req, id):
    status_update2 = UserDetails.objects.get(user_id = id)
    status_update2.user_status = 'Rejected'
    status_update2.save()
    messages.warning(req, 'User was Rejected..!')
    return redirect('adminpendingusers')

def delete_user(req, id):
    User.objects.get(user_id = id).delete()
    messages.warning(req, 'User was Deleted..!')
    return redirect('adminallusers')




def adaboost(request):
    return render(request, "admin/ada_boost.html")


# ADABoost_btn
def ADABoost_btn(req):
    dataset = Upload_dataset_model.objects.last()
    # print(dataset.Dataset)
    df=pd.read_csv(dataset.Dataset.path)

    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["message"] = df["message"].apply(wordopt)
    x = df["message"]
    label_map = {'ham': 0, 'spam': 1}
    y = df["label"].astype(str).str.strip().str.lower().map(label_map)

    if y.isnull().any():
        messages.error(req, 'Dataset labels must contain only ham and spam values for XGBoost.')
        return redirect('xgboost')

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)

    from sklearn.ensemble import AdaBoostClassifier

    ADB = AdaBoostClassifier(random_state=0)
    ADB.fit(xv_train, y_train)
    pred_lr=ADB.predict(xv_test)
    ADB.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))


    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr,average = 'macro')*100, 2)
    recall = round(recall_score(y_test,pred_lr,average = 'macro')*100, 2)
    f1 = round(f1_score(y_test,pred_lr,average = 'macro')*100, 2)
    # Accuracy_train(accuracy_score(prediction_train,y_train))
    name = "ADA Boost Algorithm"
    ADA_ALGO.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = ADA_ALGO.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    return render(req, 'admin/ada_boost.html',{'i': data})

def logistic(request):
    return render(request, "admin/logistic.html")

def logistic_btn(req):
    dataset = Upload_dataset_model.objects.last()
    # print(dataset.Dataset)
    df=pd.read_csv(dataset.Dataset.path)

    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["message"] = df["message"].apply(wordopt)
    x = df["message"]
    label_map = {'ham': 0, 'spam': 1}
    y = df["label"].astype(str).str.strip().str.lower().map(label_map)

    if y.isnull().any():
        messages.error(req, 'Dataset labels must contain only ham and spam values for XGBoost.')
        return redirect('xgboost')

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)

    from sklearn.linear_model import LogisticRegression

    LR = LogisticRegression()
    LR.fit(xv_train,y_train)
    pred_lr=LR.predict(xv_test)
    LR.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))

    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr,average = 'macro')*100, 2)
    recall = round(recall_score(y_test,pred_lr,average = 'macro')*100, 2)
    f1 = round(f1_score(y_test,pred_lr,average = 'macro')*100, 2)
    # Accuracy_train(accuracy_score(prediction_train,y_train))
    name = "Logistic Regression Algorithm"
    Logistic.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = Logistic.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    req.session['accuracy']=accuracy
    return render(req, 'admin/logistic.html',{'i': data})




def decision(request):
    return render(request, "admin/decision_tree.html")

def Decisiontree_btn(req):
    dataset = Upload_dataset_model.objects.last()
    df=pd.read_csv(dataset.Dataset.path)
    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["message"] = df["message"].apply(wordopt)
    x = df["message"]
    y = df["label"]

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)
    from sklearn.tree import DecisionTreeClassifier

    DT = DecisionTreeClassifier()
    DT.fit(xv_train, y_train)
    # prediction
    pred_lr=DT.predict(xv_test)
    DT.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))

    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr,average = 'macro')*100, 2)
    recall = round(recall_score(y_test,pred_lr,average = 'macro')*100, 2)
    f1 = round(f1_score(y_test,pred_lr,average = 'macro')*100, 2)
    name = "Decision Tree Algorithm"
    DECISSION_ALGO.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = DECISSION_ALGO.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    req.session['des_accuracy']=accuracy

    return render(req, 'admin/decision_tree.html',{'i':data})

def knn(req):
    return render(req,'')

def knn(request):
    return render(request, "admin/knn.html")

def KNN_btn(req):
    dataset = Upload_dataset_model.objects.last()
    # print(dataset.Dataset)
    df=pd.read_csv(dataset.Dataset.path)

    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["message"] = df["message"].apply(wordopt)
    x = df["message"]
    y = df["label"]

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)
    from sklearn.neighbors import KNeighborsClassifier

    KNN = KNeighborsClassifier()
    KNN.fit(xv_train, y_train)
    # prediction
    pred_lr=KNN.predict(xv_test)
    KNN.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))



    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr,average = 'macro')*100, 2)
    recall = round(recall_score(y_test,pred_lr,average = 'macro')*100, 2)
    f1 = round(f1_score(y_test,pred_lr,average = 'macro')*100, 2)
    # Accuracy_train(accuracy_score(prediction_train,y_train))
    name = "KNN Algorithm"
    KNN_ALGO.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = KNN_ALGO.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    return render(req, 'admin/knn.html',{'i': data})

def admin_svm_algo(request):
    return render(request, "admin/svm-algo.html")

def SVM_btn(req):
    dataset = Upload_dataset_model.objects.last()
    # print(dataset.Dataset)
    df=pd.read_csv(dataset.Dataset.path)
 
    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["text"] = df["text"].apply(wordopt)
    x = df["text"]
    y = df["class"]

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)
    from sklearn.neighbors import KNeighborsClassifier

    SXM = SVC()
    SXM.fit(xv_train, y_train)
    # prediction
    pred_lr=SXM.predict(xv_test)
    SXM.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))


    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr,average = 'macro')*100, 2)
    recall = round(recall_score(y_test,pred_lr,average = 'macro')*100, 2)
    f1 = round(f1_score(y_test,pred_lr,average = 'macro')*100, 2)
    # Accuracy_train(accuracy_score(prediction_train,y_train))
    name = "SVM Algorithm"
    SXM_ALGO.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = SXM_ALGO.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    return render(req, 'admin/svm-algo.html',{'i':data})


def randomforest(request):
    return render(request, "admin/random_forest.html")

def randomforest_btn(req):
    dataset = Upload_dataset_model.objects.last()
    # print(dataset.Dataset)
    df=pd.read_csv(dataset.Dataset.path)
    
    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["message"] = df["message"].apply(wordopt)
    x = df["message"]
    y = df["label"]

    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test = train_test_split(x,y,test_size = 0.3, random_state = 0)
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(X_train)
    xv_test = vectorization.transform(X_test)

    from sklearn.ensemble import RandomForestClassifier

    RFC = RandomForestClassifier(random_state=0)
    RFC.fit(xv_train, y_train)
    pred_lr=RFC.predict(xv_test)
    RFC.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))


    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr,average = 'macro')*100, 2)
    recall = round(recall_score(y_test,pred_lr,average = 'macro')*100, 2)
    f1 = round(f1_score(y_test,pred_lr,average = 'macro')*100, 2)
    # Accuracy_train(accuracy_score(prediction_train,y_train))
    name = "Random Forest"
    RandomForest.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = RandomForest.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    req.session['ran_accuracy']=accuracy

    return render(req, 'admin/random_forest.html',{'i': data})



def gradient(request):
    return render (request, 'admin/gradient.html')

def gradient_btn(req):
    dataset = Upload_dataset_model.objects.last()
    # print(dataset.Dataset)
    df=pd.read_csv(dataset.Dataset.path)
    
    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["message"] = df["message"].apply(wordopt)
    x = df["message"]
    y = df["label"]

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)

    from sklearn.ensemble import GradientBoostingClassifier

    GBC = GradientBoostingClassifier(random_state=0)
    GBC.fit(xv_train, y_train)
    pred_lr=GBC.predict(xv_test)
    GBC.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))

    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr, pos_label='spam')*100, 2)
    recall = round(recall_score(y_test,pred_lr, pos_label='spam')*100, 2)
    f1 = round(f1_score(y_test,pred_lr, pos_label='spam')*100, 2)
    name = "Gradient Boost Algorithm"
    GradientBoosting.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = GradientBoosting.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    return render(req, 'admin/gradient.html',{'i': data})

# Admin XGBOOST Algorithm
def xgboost(req):
    data = XG_ALGO.objects.last()
    return render(req, 'admin/xg_boost.html', {'i': data})

# XGBOOST_btn
def XGBOOST_btn(req):
    dataset = Upload_dataset_model.objects.last()
    if dataset is None or not dataset.Dataset:
        messages.warning(req, 'Please upload a dataset before running the XGBoost algorithm.')
        return redirect('uploaddataset')

    # print(dataset.Dataset)
    df=pd.read_csv(dataset.Dataset.path)
    

    def wordopt(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W"," ",text) 
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)    
        return text
    df["message"] = df["message"].apply(wordopt)
    x = df["message"]
    label_map = {'ham': 0, 'spam': 1}
    y = df["label"].astype(str).str.strip().str.lower().map(label_map)

    if y.isnull().any():
        messages.error(req, 'Dataset labels must contain only ham and spam values for XGBoost.')
        return redirect('xgboost')

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)
    xv_test = vectorization.transform(x_test)

    XGB = XGBClassifier(random_state=42, eval_metric='logloss')
    XGB.fit(xv_train, y_train)
    pred_lr=XGB.predict(xv_test)
    XGB.score(xv_test, y_test)
    print(classification_report(y_test, pred_lr))

    model_dir = Path(__file__).resolve().parent.parent / 'Email_spam'
    with open(model_dir / 'vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorization, f)
    with open(model_dir / 'xgboost_model.pkl', 'wb') as f:
        pickle.dump(XGB, f)


    # evaluation
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    accuracy = round(accuracy_score(y_test,pred_lr)*100, 2)
    precession = round(precision_score(y_test,pred_lr, average='macro')*100, 2)
    recall = round(recall_score(y_test,pred_lr, average='macro')*100, 2)
    f1 = round(f1_score(y_test,pred_lr, average='macro')*100, 2)
    name = "XG Boost Algorithm"
    XG_ALGO.objects.create(Accuracy=accuracy,Precession=precession,F1_Score=f1,Recall=recall,Name=name)
    data = XG_ALGO.objects.last()
    messages.success(req, 'Algorithm executed Successfully')
    req.session['xgb_accuracy'] = accuracy
    return render(req, 'admin/xg_boost.html',{'i': data})

def admin_comparison_graph(request):
    accuracy = request.session.get('accuracy')
    ran_accuracy = request.session.get('ran_accuracy')
    des_accuracy = request.session.get('des_accuracy')


    details = XG_ALGO.objects.last()
    a = details.Accuracy
    deatails1 = ADA_ALGO.objects.last()
    b = deatails1.Accuracy

    details4 = des_accuracy
    # e = details4.Accuracy
    details6 = accuracy
    # g = details6.Accuracy
    details7 = ran_accuracy
    # h = details7.Accuracy
    print( details4, details6, details7,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

    return render(request, 'admin/comparison-graph.html', {'xg':a,'ada':b,'dt':details4,'log':details6, 'ran':details7})


def delete_dataset(request, id):
    dataset = Upload_dataset_model.objects.get(user_id = id).delete()
    messages.warning(request, 'Dataset was deleted..!')
    return redirect('view_view')


def uploaddataset(req):
    if req.method == 'POST':
        file = req.FILES['data_file']
        file_size = str((file.size)/1024) +' kb'
        Upload_dataset_model.objects.create(File_size = file_size, Dataset = file)
        messages.success(req, 'Your dataset was uploaded..')
    return render(req,'admin/upload_dataset.html')

def viewdataset(req):
    dataset = Upload_dataset_model.objects.all()
    paginator = Paginator(dataset, 5)
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req,'admin/view_dataset.html', {'data' : dataset, 'user' : post})


def view_view(request):
    # df=pd.read_csv('heart.csv')
    data = Upload_dataset_model.objects.last()
    print(data,type(data),'sssss')
    file = str(data.Dataset)
    df = pd.read_csv(f'./media/{file}')
    table = df.to_html(table_id='data_table')
    return render(request,'admin/view-view.html', {'t':table})















def admin_dataset_btn(req):
    messages.success(req, 'Dataset Total:990 files uploaded successfully')
    return redirect('uploaddataset') 


def admin_graph(req):
    def metric_or_zero(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    accuracy = metric_or_zero(req.session.get('accuracy'))
    ran_accuracy = metric_or_zero(req.session.get('ran_accuracy'))
    des_accuracy = metric_or_zero(req.session.get('des_accuracy'))

    ada_details = ADA_ALGO.objects.last()
    knn_details = KNN_ALGO.objects.last()
    gradient_details = GradientBoosting.objects.last()
    xgboost_details = XG_ALGO.objects.last()

    context = {
        'ada': metric_or_zero(getattr(ada_details, 'Accuracy', 0)),
        'knn': metric_or_zero(getattr(knn_details, 'Accuracy', 0)),
        'dt': des_accuracy,
        'log': accuracy,
        'ran': ran_accuracy,
        'gst': metric_or_zero(getattr(gradient_details, 'Accuracy', 0)),
        'xgb': metric_or_zero(getattr(xgboost_details, 'Accuracy', 0)),
    }
    return render(req, 'admin/admin_graph.html', context)



def user_feedbacks(request):
    feed =UserFeedbackModels.objects.all()
    return render(request,'admin/user_feedbacks.html', {'back':feed})

def user_sentiment(request):
    fee = UserFeedbackModels.objects.all()
    return render(request,'admin/user_sentiment.html', {'cat':fee})

def user_graph(request):
    positive = UserFeedbackModels.objects.filter(sentment = 'positive').count()
    very_positive = UserFeedbackModels.objects.filter(sentment = 'very positive').count()
    negative = UserFeedbackModels.objects.filter(sentment = 'negative').count()
    very_negative = UserFeedbackModels.objects.filter(sentment = 'very negative').count()
    neutral = UserFeedbackModels.objects.filter(sentment = 'neutral').count()
    context ={
        'vp': very_positive, 'p':positive, 'n':negative, 'vn':very_negative, 'ne':neutral
    }
    return render(request,'admin/user_graph.html',context)



def adminlogout(req):
    messages.info(req,'You are logged out...!')
    return redirect('admin')

