from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from .models import *


# Create your views here.
def test(request):
    if request.method == "POST":
        # DB에 저장하는 로직
        qna_form = QnaForm(request.POST, request.FILES)
        # 유효성 검사
        if qna_form.is_valid():
            qna = qna_form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            qna.user = request.user
            qna.save()
            
            # tags = qna_form.cleaned_data['tag'].split(',')
            # for tag in tags:
            #     if not tag : 
            #         continue
            #     else:
            #         tag = tag.strip()
            #         tag_, created = Tag.objects.get_or_create(name = tag)
            #         Qna.tag.add(tag_)


            # return redirect("qna:index")
    else:
        qna_form = QnaForm()
    context = {"qna_form": qna_form}
    return render(request, "qna/form.html", context=context)

def index(request):
    qna = Qna.objects.order_by("-pk")
    qna_hits = Qna.objects.order_by("-hits")
    context = {
        "qna": qna,
        "qna_hits": qna_hits,
    }

    return render(request, "qna/index.html", context)

@login_required
def create(request):
    if request.method == "POST":
        # DB에 저장하는 로직
        qna_form = QnaForm(request.POST, request.FILES)
        # 유효성 검사
        if qna_form.is_valid():
            qna = qna_form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            qna.user = request.user
            qna.save()
            return redirect("qna:index")
            
            # tags = qna_form.cleaned_data['tag'].split('#')
            # for tag in tags:
            #     if not tag : 
            #         continue
            #     else:
            #         tag = tag.strip()
            #         tag_, created = Tag.objects.get_or_create(name = tag)
            #         Qna.tag.add(tag_)


            # return redirect("qna:index")
    else:
        qna_form = QnaForm()
    context = {"aqna_form": qna_form}
    return render(request, "qna/form.html", context=context)
  
def detail(request, pk):
    # 특정 글을 가져온다.
    qna = get_object_or_404(Qna, pk=pk)
    answer_form = AnswerForm()

    # 조회수 측정
    qna.hits += 1
    qna.save()

    # template에 객체 전달
    context = {
        "qna": qna,
        # 역참조 (qna에 포함된 answer data를 전부 불러온다.)
        "answers": qna.answer_set.all(),
        "answer_form": answer_form,
    }
    return render(request, "qna/detail.html", context)

@login_required
def update(request, pk):
    qna = Qna.objects.get(pk=pk)
    if request.user == qna.user:
        if request.method == "POST":
            qna_form = QnaForm(request.POST, request.FILES, instance=qna)
            if qna_form.is_valid():
                qna_form.save()
                return redirect("qna:detail", qna.pk)
        else:
            qna_form = QnaForm(instance=qna)
        context = {
            "qna_form": qna_form,
            "qna": qna,
        }
        return render(request, "qna/form.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("qna:detail", qna.pk)


@login_required
def delete(request, pk):
    Qna.objects.get(pk=pk).delete()

    return redirect("qna:index")



@login_required
def answers_create(request, pk):
    if request.method == "POST":
        # DB에 저장하는 로직
        qna = Qna.objects.get(pk=pk)
        answer_form = AnswerForm(request.POST)
        # 유효성 검사
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.qna = qna
            answer.user = request.user
            answer.save()
        return redirect("qna:detail", qna.pk)
    else:
        qna = Qna.objects.get(pk=pk)
        answer_form = AnswerForm()
        context = {
            "answer_form": answer_form,
            "qna" : qna, }
        return render(request,"qna/answer.html", context)

@login_required
def answers_update(request, qna_pk, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk)
    qna = Qna.objects.get(pk=qna_pk)
    if request.user == answer.user:
        if request.method == "POST":
            answer = AnswerForm(request.POST, instance=answer)
            if answer.is_valid():
                answer.save()
                return redirect("qna:detail", qna_pk)
        else:
            answer_form = AnswerForm(instance=answer)
        context = {
            "answer_form": answer_form,
            "answer": answer,
            "qna": qna
        }
        return render(request, "qna/answer.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("qna:detail", qna_pk)


@login_required
def answers_delete(request, qna_pk, answer_pk):
    if request.user.is_authenticated:
        answer = get_object_or_404(Answer, pk=answer_pk)
        if request.user == answer.user:
            answer.delete()
    return redirect("qna:detail", qna_pk)

@login_required
def like(request, pk):
    qna = get_object_or_404(Qna, pk=pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if answer.like_users.filter(id=request.user.id).exists():
    if request.user in qna.like_users.all():
        # 좋아요 삭제하고
        qna.like_users.remove(request.user)
        is_liked = False
    else:
        # 좋아요 추가하고
        qna.like_users.add(request.user)
        is_liked = True
    # 상세 페이지로 redirect
    context = {"isLiked": is_liked, "likeCount":qna.like_users.count()}
    return JsonResponse(context)


def qna_closed(request, pk):
    qna = Qna.objects.get(pk=pk)
    if qna.closed == False:
        qna.closed = True
        qna.save()
    else:
        qna.closed = False
        qna.save()
    return redirect("qna:detail", pk)