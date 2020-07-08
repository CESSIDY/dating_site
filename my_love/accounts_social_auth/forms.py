from allauth.account.forms import LoginForm

class MyCustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.
        print(self.user)
        print(kwargs)

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)