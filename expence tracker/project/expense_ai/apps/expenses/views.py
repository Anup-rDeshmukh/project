from django.shortcuts import render


def home(request):

    if request.method == "POST":
        uploaded_file = request.FILES.get("sms_csv")

        if uploaded_file:
            print(uploaded_file.name)

    return render(request, "index.html")


def dashboard(request):
    # Sample data — replace with parsed CSV / DB totals later
    spending_by_category = [
        {"category": "Food", "amount": 4200.0},
        {"category": "Shopping", "amount": 2800.0},
        {"category": "Travel", "amount": 5100.0},
        {"category": "Transport", "amount": 1950.0},
        {"category": "Bills", "amount": 3600.0},
        {"category": "Entertainment", "amount": 1200.0},
    ]
    chart_data = {
        "labels": [row["category"] for row in spending_by_category],
        "amounts": [row["amount"] for row in spending_by_category],
    }
    total_spending = sum(row["amount"] for row in spending_by_category)
    return render(
        request,
        "dashboard.html",
        {
            "spending_by_category": spending_by_category,
            "chart_data": chart_data,
            "total_spending": total_spending,
        },
    )


def signin(request):
    return render(request, "signin.html")
