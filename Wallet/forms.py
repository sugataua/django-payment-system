from django import forms
from Wallet import models
from django.contrib.auth.models import User


class ClientRegistrationForm(forms.Form):
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    email = forms.EmailField()
    date_of_birth = forms.DateField()
    password = forms.CharField(max_length=30)
    password_confirm = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=13)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30)


class ConfirmForm(forms.Form):
    #code = forms.CharField(max_length=6,min_length=6)
    code = forms.RegexField(label="Confirmation code", max_length=6, min_length=6,
                                regex=r'^\d{6,6}$',
                                #help_text="Code of 6 digits",
                                error_messages={
                                    'invalid': "This value must be code of 6 digits"})

class MoneyTransferForm(forms.Form):
    wallet_number = forms.CharField(max_length=32)
    transfer_amount = forms.FloatField()

class ChangePassword(forms.Form):
    old_password = forms.CharField(max_length=30)
    new_password = forms.CharField(max_length=30)
    new_password_confirm = forms.CharField(max_length=30)

class AddMoney(forms.Form):
    money = forms.FloatField()

    error_messages = {
        'negative_money': "Your amount is negative. It must be value > 0."
    }

    def clean_money(self):
        money = self.cleaned_data.get("money")
        if money < 0:
            raise forms.ValidationError(
                self.error_messages['negative_money'])
        return money



class ClientRegistration(forms.ModelForm):
    """
    A form that creates a client.
    """
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        }
    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))
"""
    email = forms.EmailField()
    class Meta:
        model = models.Client
        fields = [
            "name",
            "surname",
            "date_of_birth",
            "phone_number",
        ]

"""
    def save(self, commit=True):
        self.
        if commit:
            self.user.save()
        return self.user
"""

"""
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
        """
"""
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
"""
"""
    def save(self, commit=True, userid):
        client = super(ClientRegistration, self).save(commit=False)
        user = User.objects.get(id=userid)
        client.set_user_id(user)
        if commit:
            client.save()
        return client
"""

class MoneyTransfer(forms.Form):
    account_number = forms.RegexField(label="Account number", max_length=15,
                                                 regex=r'^\d{1,15}$',
                                                 #help_text="Code of 6 digits",
                                                 error_messages={
                                                     'invalid': "This value must be valid account number"})
    number = forms.DecimalField(max_digits=15)
    amount = forms.FloatField()
    message = forms.CharField(max_length=140, required=False)
    error_messages = {
        'negative_money': "Your amount is negative or equals zero. It must be value > 0.",
        'account_not_exist': "This account number is not valid!"
    }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError(
                self.error_messages['negative_money'])
        return amount
    def clean_account_number(self):
        ac_number = self.cleaned_data.get("account_number")
        try:
            account = models.Wallet.objects.get(number=ac_number)
        except models.Wallet.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['account_not_exist'])
        return ac_number






    class MoneyTransaction(forms.ModelForm):
        message = forms.CharField(max_length=30,required=False)
        number = forms.CharField(max_length=15,required=False)
        error_messages = {
            'negative_money': "Your amount is negative or equals zero. It must be value > 0."
        }

        class Meta:
            model = models.Transaction
            fields = [
                "to_wallet",
                "money",
                ]

        def clean_money(self):
            money = self.cleaned_data.get("money")
            if money <= 0:
                raise forms.ValidationError(
                    self.error_messages['negative_money'])
            return money
