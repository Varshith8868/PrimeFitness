from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileSetupForm
from scipy.optimize import linprog
import numpy as np

def home(request):
    return render(request, 'home.html')

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            return redirect('login')  # Redirect to login page after successful signup
        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})
    
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# Profile Setup View
@login_required
def profile_setup_view(request):
    if request.method == "POST":
        form = ProfileSetupForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('workouts')  # Redirect to workouts page after saving
    else:
        form = ProfileSetupForm(instance=request.user)
    return render(request, 'profile_setup.html', {'form': form})

# Workouts View
@login_required
def workouts_view(request):
    if request.method == "POST":
        gender = request.POST.get("gender")
        height = float(request.POST.get("height", 0))
        weight = float(request.POST.get("weight", 0))
        fitness_level = request.POST.get("fitness_level")
        goal = request.POST.get("goal")

        # Generate workout plan
        workout_plan = optimize_workout(gender, height, weight, fitness_level, goal)
        return render(request, 'workouts.html', {'workout_plan': workout_plan})

    return render(request, 'workouts.html', {})

# Diet View
@login_required
def diet_view(request):
    """
    This view handles the diet plan generation.
    It uses Linear Programming to optimize meal plans based on the user's budget.
    """
    meal_plan = None
    budget = request.session.get("budget", 0)  # Retrieve budget from session
    days_in_month = 30  # Assume 30 days in a month

    if request.method == "POST" or budget > 0:
        if budget <= 4000:
            daily_protein_target = 150  # Low Budget
        elif budget <= 8000:
            daily_protein_target = 200  # Medium Budget
        else:
            daily_protein_target = 300  # High Budget

        # Meal options with cost, protein, and items
        meals = {
            "Breakfast": {"cost": 5, "protein": 10, "items": ["Oatmeal", "Eggs", "Banana"]},
            "Lunch": {"cost": 10, "protein": 20, "items": ["Grilled Chicken", "Brown Rice", "Salad"]},
            "Dinner": {"cost": 15, "protein": 25, "items": ["Steak", "Sweet Potato", "Broccoli"]},
            "Snacks": {"cost": 20, "protein": 15, "items": ["Protein Bar", "Greek Yogurt", "Almonds"]},
        }

        meal_costs = [meals[meal]["cost"] for meal in meals]
        meal_protein = [meals[meal]["protein"] for meal in meals]
        max_meals = [30, 20, 15, 10]  # Max servings per month

        equal_protein_per_meal = daily_protein_target / len(meals)

        # Linear Programming setup
        c = meal_costs
        A_eq = [meal_protein]
        b_eq = [daily_protein_target]
        A_ub = [meal_costs]
        b_ub = [budget / days_in_month]
        x_bounds = [(0, max_meals[i]) for i in range(len(meal_costs))]

        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=x_bounds, method="highs")

        if result.success:
            meal_plan = {}
            total_monthly_protein = 0
            for i, meal in enumerate(meals):
                per_day = equal_protein_per_meal
                per_month = per_day * days_in_month
                total_monthly_protein += per_month

                meal_plan[meal] = {
                    "items": meals[meal]["items"],
                    "protein_per_day": per_day,
                    "protein_per_month": per_month,
                }

            meal_plan["Total_Protein"] = total_monthly_protein
            meal_plan["Total_Protein_Per_Day"] = total_monthly_protein / days_in_month
        else:
            meal_plan = {"error": "Could not optimize meal plan within the given budget."}

    return render(request, "diet.html", {"meal_plan": meal_plan, "budget": budget})

# Budget View
@login_required
def budget_view(request):
    if request.method == "POST":
        budget = float(request.POST.get("budget", 0))
        request.session["budget"] = budget  # Store budget in session
        return redirect('diet')  # Redirect to the diet page
    return render(request, 'budget.html')

# Function to Optimize Workout Plan
def optimize_workout(gender, height, weight, fitness_level, goal):
    """
    Optimize workout plan based on user constraints like gender, height, weight, fitness level, and goal.
    Display the workout plan in hours per week and minutes per day.
    """
    # Example coefficients for optimization (adjust based on your logic)
    c = [-5, -4, -6, -3, -2, -1]  # Negative values to maximize muscle gain

    # Adjust constraints based on user's height and weight
    max_hours = 6 + (height / 100) + (weight / 50)  # Example: taller/heavier users can handle more hours
    fatigue_limit = 10 + (weight / 70)  # Example: heavier users have a higher fatigue limit

    A = [
        [1, 1, 1, 1, 1, 1],  # Total weekly workout time ≤ max_hours
        [3, 2, 4, 1, 1, 1]   # Fatigue limit
    ]
    b = [max_hours, fatigue_limit]
    x_bounds = [(0.5, 3) for _ in range(6)]  # Min 30 min, Max 3 hours per session

    # Solve the optimization problem
    result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method="highs")
    if result.success:
        # Convert hours to minutes per day
        workout_plan_in_hours = {
            "Chest": round(result.x[0], 1),
            "Back": round(result.x[1], 1),
            "Legs": round(result.x[2], 1),
            "Arms": round(result.x[3], 1),
            "Shoulders": round(result.x[4], 1),
            "Cardio": round(result.x[5], 1),
        }
        workout_plan_in_minutes_per_day = {
            muscle: round((hours * 60) / 7, 1) for muscle, hours in workout_plan_in_hours.items()
        }

        return {
            "weekly": workout_plan_in_hours,
            "daily": workout_plan_in_minutes_per_day,
        }
    return {"error": "Could not optimize workout"}