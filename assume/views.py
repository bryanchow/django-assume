from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.models import User
from django.contrib import messages


@staff_member_required
def assume_user(request, id, next_url='/'):
    """
    Custom admin view that logs into a specified user account.
    """

    user = get_object_or_404(User, pk=id)

    # Don't allow staff members cannot be assumed
    if user.is_staff:
        messages.error(request, "Sorry, staff members cannot be assumed.")
        return HttpResponseRedirect(reverse('admin:auth_user_change', args=(user.id,)))

    # Call authenticate without a password (this only works with our custom backend)
    user = authenticate(username=user.username)

    # We could just call django.contrib.auth.login(request, user) here, but
    # instead we use duplicate code so that the last_login field doesn't get
    # updated when a user is assumed.
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != user.id:
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = user.id
    request.session[BACKEND_SESSION_KEY] = user.backend
    if hasattr(request, 'user'):
        request.user = user
    # End of custom login

    return HttpResponseRedirect(next_url)
