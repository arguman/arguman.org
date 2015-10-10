from django.dispatch import Signal

follow_done = Signal(providing_args=["follower", "following"])
unfollow_done = Signal(providing_args=["follower", "following"])
