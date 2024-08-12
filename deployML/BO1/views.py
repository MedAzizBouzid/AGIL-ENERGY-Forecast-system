from django.shortcuts import render
from joblib import load 
model=load('./notebooks/model_lgbm.joblib')
def predictor(request):
    return render(request,'main.html')
def formInfo(request):
    ancscp=request.GET['ANCSCP']
    DATLIV=request.GET['DATLIV']
    LIBPRD=request.GET['LIBPRD']
    LIBGVR=request.GET['libgvr']
    LIBLOC=request.GET['libloc']
    prixHt=request.GET['prixHT']
    
    y_pred=model.predict([[ancscp,DATLIV,LIBPRD,LIBGVR,LIBLOC,prixHt]])
    print(y_pred)
    return render(request,'result.html',{'ancscp':ancscp})