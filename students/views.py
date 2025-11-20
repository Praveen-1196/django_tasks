from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Student
import cloudinary

# Create your views here.

MAX_FILE_SIZE=5*1024*1024

@csrf_exempt
def student_list(request):
    if request.method != 'GET':
        return JsonResponse({'error':'GET METHOD REQUIRED!!'},status=405)
    
    students=list(Student.objects.values())
    return JsonResponse(students,safe=False)


@csrf_exempt
def student_create(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    name = request.POST.get('name')
    age = request.POST.get('age')
    photo = request.FILES.get('photo')
    img_url=cloudinary.uploader.upload(photo)

    if not name or not age or not photo:
        return JsonResponse({'error': 'All fields (name, age, photo) are required'}, status=400)

    try:
        age = int(age)
    except ValueError:
        return JsonResponse({'error': 'Age must be a number'}, status=400)

    if photo.size > MAX_FILE_SIZE:
        return JsonResponse({'error': 'Photo exceeds max size of 5 MB'}, status=400)

    student = Student(name=name, age=age, photo=img_url["secure_url"])
    student.save()
    return JsonResponse({'id': student.id, 'message': 'Student created'})


@csrf_exempt
def student_update(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    student = get_object_or_404(Student, pk=pk)

    name = request.POST.get('name')
    age = request.POST.get('age')
    photo = request.FILES.get('photo')

    if name:
        student.name = name

    if age:
        try:
            student.age = int(age)
        except ValueError:
            return JsonResponse({'error': 'Age must be a number'}, status=400)

    if photo:
        if photo.size > MAX_FILE_SIZE:
            return JsonResponse({'error': 'Photo exceeds max size of 5 MB'}, status=400)
        student.photo = photo

    student.save()
    return JsonResponse({'message': 'Student updated'})


@csrf_exempt
def student_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return JsonResponse({'message': 'Student deleted'})



@csrf_exempt
def student_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    data = json.loads(request.body)
    name = data.get('name')
    age = data.get('age')

    try:
        student = Student.objects.get(name=name, age=age)
        return JsonResponse({
            'message': 'Login successful',
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'photo': student.photo
        })
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
