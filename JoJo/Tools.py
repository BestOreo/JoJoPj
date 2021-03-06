from .models import User,Word
from django.http import JsonResponse

def getwordsfortest(username):
    words = User.objects.get_or_create(username=username)[0].word_total_plan
    wordlist = words.split(";")
    book = []
    for node in wordlist[:-1]:
        nodemap = node.split(",")
        word = nodemap[0]
        forget = int(nodemap[1])
        total = int(nodemap[2])
        wordsearch = Word.objects.get_or_create(wordname=word)[0]
        json = {'word': wordsearch.wordname}
        json['forget'] = forget
        json['total'] = total
        json['group'] = wordsearch.group
        json['soundmark'] = wordsearch.soundmark
        json['explanation'] = wordsearch.explanation.split(";")
        json['demo_1'] = wordsearch.demo_1
        json['demo_1_translate'] = wordsearch.demo_1_translate
        json['demo_2'] = wordsearch.demo_2
        json['demo_2_translate'] = wordsearch.demo_2_translate
        json['demo_3'] = wordsearch.demo_3
        json['demo_3_translate'] = wordsearch.demo_3_translate
        book.append(json)
    return book



def getWordbyUser(username):
    words = User.objects.get_or_create(username=username)[0].word_total_plan
    wordlist = words.split(";")[:-1]
    wordbook = []
    for w in wordlist:
        w = w.split(",")
        wordbook.append([w[0],int(w[1]),int(w[2])])
    return wordbook


def getWordfromBookbyGroup(group,plan):
    print(plan)
    wordsearch = Word.objects.filter(group=group)
    result = []
    count = 0
    for i in wordsearch:
        count += 1
        if i.wordname in plan: # 正在学习的单词不予显示
            result.append((i.wordname, i.explanation, "checkbox-10-" + str(count), 1) )
        else:
            result.append((i.wordname, i.explanation, "checkbox-10-"+str(count), 0) )
    return tuple(result)


def chooseWords(username, wordname, status):
    # print(username, wordname, status)
    user = User.objects.filter(username__exact=username)[0]
    userdict = user.word_total_plan
    # print("old:",userdict)
    userdict = userdict.split(";")[:-1]

    result = ""
    if status == "false":

        for word in userdict:
            name = word.split(",")[0]
            if name == wordname:
                continue
            else:
                result += word+";"

    else:
        for word in userdict:
            name = word.split(",")[0]
            if name == wordname:
                return
            result += word + ";"
            print(result)

        result += wordname+",1,1;"

    user.word_total_plan = result
    user.save()
    # print(result)


def getWords(request):
    username = request.COOKIES.get('username', '')
    words = User.objects.get_or_create(username="u1")[0].word_total_plan
    wordlist = words.split(";")
    book = {}
    count = 0
    for node in wordlist[:-1]:
        nodemap = node.split(",")
        word = nodemap[0]
        forget = int(nodemap[1])
        total = int(nodemap[2])
        wordsearch = Word.objects.get_or_create(wordname=word)[0]
        json = {'word': wordsearch.wordname}
        json['forget'] = forget
        json['total'] = total
        json['group'] = wordsearch.group
        json['soundmark'] = wordsearch.soundmark
        json['explanation'] = wordsearch.explanation.split(";")
        json['demo_1'] = wordsearch.demo_1
        json['demo_1_translate'] = wordsearch.demo_1_translate
        json['demo_2'] = wordsearch.demo_2
        json['demo_2_translate'] = wordsearch.demo_2_translate
        json['demo_3'] = wordsearch.demo_3
        json['demo_3_translate'] = wordsearch.demo_3_translate
        book[count] = json
        count += 1
    book['count'] = count
    return JsonResponse(book, safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cancelword(request):
    if request.method == "POST":
        username =  request.POST.get("id", "")
        wordname =  request.POST.get("wordname", "")
        print("cancel",username,wordname)

        user = User.objects.filter(username__exact=username)[0]
        userdict = user.word_total_plan.split(";")
        result = ""
        for i in userdict[:-1]:
            if wordname not in i:
                result += i+";"

        print(result)
        user.word_total_plan = result;
        user.save()

        return JsonResponse({"success":0}, safe=False)
    return JsonResponse({"success": 1}, safe=False)


@csrf_exempt
def chooseword(request):
    if request.method == "POST":
        username =  request.POST.get("id", "")
        wordname =  request.POST.get("wordname", "")

        user = User.objects.filter(username__exact=username)[0]
        userdict = user.word_total_plan
        userdict += wordname+",0,0;"
        user.word_total_plan = userdict;
        print(userdict)
        user.save()
        return JsonResponse({"success":0}, safe=False)
    return JsonResponse({"success": 1}, safe=False)



