from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

User = get_user_model()


def _is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(_is_superuser)
def manage_users(request):
    users = User.objects.order_by("-date_joined")
    return render(
        request,
        "account/manage_users.html",
        {"users": users},
    )


@login_required
@user_passes_test(_is_superuser)
def delete_user(request, pk):
    if request.method != "POST":
        return redirect("manageUsers")

    target = get_object_or_404(User, pk=pk)

    if target.pk == request.user.pk:
        messages.error(request, "You cannot delete your own account while logged in.")
        return redirect("manageUsers")

    if target.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
        messages.error(request, "You cannot delete the only superuser account.")
        return redirect("manageUsers")

    username = target.username
    target.delete()
    messages.success(request, f"Deleted account “{username}”.")
    return redirect("manageUsers")
