from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment, Reply,Chat,Messages


class ReplyComment(LoginRequiredMixin,View):
    def get(self,request,comment_id):
        comment=get_object_or_404(Comment,id=comment_id)
        return render(request, 'reply_page.html', {'comment': comment})


    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        reply_text = request.POST.get('reply_text')

        if comment.user == request.user:
            messages.error(request, "O'z sharhingizga javob yozishingiz mumkin emas!")
            return redirect('####', pk=comment.post.pk)

        if reply_text:
            Reply.objects.create(
                comment=comment,
                user=request.user,
                text=reply_text
            )
            messages.success(request, "Javobingiz muvaffaqiyatli qo'shildi!")
            return redirect('####', pk=comment.post.pk)

        else:
            messages.warning(request, "Javob matnini kiriting!")
            return redirect('reply_comment_page', comment_id=comment_id)



class CommentUpdate(LoginRequiredMixin,View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        return render(request, 'comment_update.html', {'comment': comment})
    def post(self,request, comment_id):
        comment=get_object_or_404(Comment,id=comment_id,user=request.user)
        text=request.POST.get('text')
        if text:
            comment.text=text
            comment.save()
            messages.success(request, "Sharh yangilandi")
        return redirect('####',pk=comment.post.pk)



class CommentDelete(LoginRequiredMixin,View):
    def post(self,request,comment_id):
        comment = get_object_or_404(Comment,id=comment_id,user=request.user)
        comment.delete()
        messages.success(request, "Sharh o‘chirildi")
        return redirect('####', pk=comment.post.pk)



class ChatView(LoginRequiredMixin,View):
    def get(self,request):
        chats=Chat.objects.filter(participants=request.user).prefetch_related('participants').order_by('-created_at')

        context={
            'chats':chats
        }

        return render(request,'chat_list.html',context)

class ChatDetail(LoginRequiredMixin,View):
    def get(self,request,chat_id):
        chat=get_object_or_404(Chat,id=chat_id,participants=request.user)
        messages=chat.messages.all().order_by('created_at')
        recipient=chat.get_recipient(request.user)
        context = {
            'chat': chat,
            'messages': messages,
            'recipient': recipient
        }
        return render(request, 'chat_detail.html', context)

    def post(self,request,chat_id):
        chat=get_object_or_404(Chat,id=chat_id,participants=request.user)
        text = request.POST.get('text')
        image = request.FILES.get('image')

        if text or image:
            Messages.objects.create(
                user=request.user,
                chat=chat,
                text=text,
                image=image
            )
        return redirect('chat_detail', chat_id=chat.id)
class ChatCreate(LoginRequiredMixin,View):
    def get(self,request,recipient_id):
        chat=Chat.objects.filter(participants=request.user).filter(participants__id=recipient_id).first()

        if not chat:
            chat=Chat.objects.create()
            chat.participants.add(request.user,recipient_id)
            chat.save()

        return redirect('chat_detail', chat_id=chat.id)

class MessageUpdate(LoginRequiredMixin,View):
    def post(self,request,message_id):
        message=get_object_or_404(Messages,id=message_id,user=request.user)
        new_text = request.POST.get('text')

        if new_text:
            message.text=new_text
            message.save()
        return redirect('chat_detail',chat_id=message.chat.id)

class MessageDelete(LoginRequiredMixin,View):
    def post(self,request,message_id):
        message=get_object_or_404(Messages,id=message_id,user=request.user)
        message.delete()
        messages.success(request, "Xabar o‘chirildi")
        return redirect('chat_detail',chat_id=message.chat.id)











