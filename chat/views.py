from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hashlib import md5
from accounts.decorators import verify_required

# Create your views here.

@login_required()
@verify_required
def room(request, room_name):
    context = {}
    if room_name == "general":
        return render(request, 'chat/room.html', {
            'room_name': 'general',
            'user':request.user
        })
    else:
        print(request.user.college.name)
        if (room_name == md5(request.user.college.name.encode("utf-8")).hexdigest()):
            return render(request, 'chat/room.html',{
                'room_name': room_name,
                'user' : request.user
            })
        else:
            context['message'] = "You are not authorised to view this college's chat room"
            return render(request, "chat/error.html", context)