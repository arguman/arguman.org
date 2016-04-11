def community(request):
    if not request.community:
        return {}

    can_submit_argument = (
        request.community.user_can_create_argument(request.user)
    )

    is_owner = (
        request.community.user_is_owner(request.user)

    )

    return {
        'community': request.community,
        'user_can_create_argument': can_submit_argument,
        'user_is_owner': is_owner
    }
