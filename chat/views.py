from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm

@login_required
def chat_room(request):
    messages = Message.objects.order_by('-timestamp')[:50]  # last 50 messages
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect("chat:chat_room")
    else:
        form = MessageForm()
    return render(request, "chat/chat_room.html", {"messages": messages, "form": form})
