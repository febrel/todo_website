from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Para registro
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Todo

# Para la paginacion
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
@login_required
def home(request):

    contexto = {}

    if request.method == 'POST':
        tarea = request.POST.get('task')
        todo_nuevo = Todo(usuario=request.user, todo_nombre=tarea)
        todo_nuevo.save()
    

    # Para la Paginacion
    page_number = request.GET.get('page')
    contenido_todos_page = Paginator(Todo.objects.filter(usuario=request.user), 2) # Numero de pesentacion
    
    # Maneja errores
    try:
        todos = contenido_todos_page.page(page_number)
    
    except PageNotAnInteger:
        todos = contenido_todos_page.page(1)

    except EmptyPage:
        todos = contenido_todos_page.page(1) 


    contexto = {'todos': todos}

    return render(request, 'todoapp/todo.html', contexto)


def registar(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Captura los datos de inputs por POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Controla qe passwod tenga mas de 3
        if len(password) <= 3:
            messages.error(request, 'Password debe tener mas de 3 caracteres!')
            return redirect('registrar')

        # Controla que no se utilice el mismo usuario
        mismo_username = User.objects.filter(username=username)

        if mismo_username:
            messages.error(request, 'El usuario ingresado ya existe!')
            return redirect('registrar')

        # Registra usuario nuevo
        usuario_nuevo = User.objects.create_user(username=username, email=email, password=password)
        usuario_nuevo.save()

        messages.success(request, 'Usuario creado con exito!')
        return redirect('login')

    contexto = {}
    return render(request, 'todoapp/registrar.html', contexto)


@login_required
def eliminar_todo(request, pk):
    # Capturo el id del Pedido
    todo = Todo.objects.get(id=pk)

    print('Estes es: ', todo)

    # Si existe un post
    if(request.method == 'POST'):
        # Query SQL elimina el pedido
        todo.delete()
        # Redirecciona al home
        return redirect('/')

    contexto = {'item': todo}

    return render(request, 'todoapp/eliminar.html', contexto)


@login_required
def editar_todo(request, pk):
    # Capturo el id del Pedido
    todo = Todo.objects.get(id=pk)
    
    todo.todo_nombre = todo.todo_nombre
    
    # Para Cambiar de estado
    if todo.estado == True:
        todo.estado = False
    else:
        todo.estado = True

    # Guarda en la DB
    todo.save()

    return redirect('/')

    # Si existe un post
    if(request.method == 'POST'):
        # Query SQL elimina el pedido
        todo.delete()
        # Redirecciona al home
        return redirect('/')



def login_page(request):

    if request.method == 'POST':
        # Captura los datos de inputs por POST
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        valida_usuario = authenticate(request, username=username, password=password)

        if valida_usuario is not None:
            login(request, valida_usuario)
            return redirect('home')
        else:
            messages.error(request, 'Los datos no son correctos!')
            return redirect('login')


    contexto = {}

    return render(request, 'todoapp/login.html', contexto)


def logout_page(request):
    logout(request)

    return redirect('login')