from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for controlling signup behaviour in the application.

    This adapter overrides the default behaviour of the `is_open_for_signup` method
    to disable user signup.
    """

    def is_open_for_signup(self, request):
        """
        Determines whether the application is open for new user signups.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: Always returns False to disable user signup.
        """
        return False
