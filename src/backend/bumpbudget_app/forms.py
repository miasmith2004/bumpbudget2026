from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "life_stage",
            "due_date",
            "child_age_months",
            "monthly_income",
            "partner_monthly_income",
            "maternity_leave_start",
            "maternity_leave_end",
            "savings_goal_total",
            "savings_deadline",
            "currency",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "maternity_leave_start": forms.DateInput(attrs={"type": "date"}),
            "maternity_leave_end": forms.DateInput(attrs={"type": "date"}),
            "savings_deadline": forms.DateInput(attrs={"type": "date"}),
        }
        help_texts = {
            "life_stage": "Choose the stage that best matches your situation.",
            "due_date": "If you're expecting, enter your estimated due date.",
            "child_age_months": "If you're in early parenthood, enter your child's age in months (0–24).",
            "monthly_income": "Your average monthly take-home income.",
            "partner_monthly_income": "Optional: partner's monthly take-home income.",
            "savings_goal_total": "Optional: how much you want to save overall for baby-related costs.",
            "savings_deadline": "Optional: when you want to reach your savings goal by.",
        }

    def clean(self):
        cleaned = super().clean()
        life_stage = cleaned.get("life_stage")
        due_date = cleaned.get("due_date")
        child_age_months = cleaned.get("child_age_months")
        leave_start = cleaned.get("maternity_leave_start")
        leave_end = cleaned.get("maternity_leave_end")
        savings_deadline = cleaned.get("savings_deadline")

        today = timezone.now().date()

        # Stage rules
        if life_stage == UserProfile.LifeStage.EXPECTING:
            if not due_date:
                self.add_error("due_date", "Due date is required if you are expecting.")
            if child_age_months is not None:
                self.add_error("child_age_months", "Child age should be empty if you are expecting.")

        if life_stage == UserProfile.LifeStage.EARLY:
            if child_age_months is None:
                self.add_error("child_age_months", "Child age is required if you are in early parenthood (0–2 years).")
            elif child_age_months > 24:
                self.add_error("child_age_months", "Please enter an age between 0 and 24 months.")
            if due_date:
                self.add_error("due_date", "Due date should be empty if you are in early parenthood.")

        # Leave date rules (optional but must be logical)
        if leave_start and leave_end and leave_start > leave_end:
            self.add_error("maternity_leave_end", "Leave end date must be after the start date.")

        # Savings deadline should be in the future (if provided)
        if savings_deadline and savings_deadline < today:
            self.add_error("savings_deadline", "Savings deadline should be today or later.")

        return cleaned


