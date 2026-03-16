from django.shortcuts import render

def dashboard(request):

    if request.method == "POST":
        uploaded_file = request.FILES.get("sms_csv")

        if uploaded_file:
            print(uploaded_file.name)  

    return render(request, "index.html")
