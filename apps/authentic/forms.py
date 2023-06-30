from apps.users.forms import CustomUserCreationForm
from apps.users.models import User


class createUserForm(CustomUserCreationForm):
    class meta:
        model = User
        fields = "__all__"
