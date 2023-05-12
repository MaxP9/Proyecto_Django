from django.shortcuts import render, redirect
from appTienda.models import Categoria, Producto
from django.db import Error 

# Create your views here.

def inicio(request):
    return render(request, "inicio.html")
    
def vistaCategoria(request):
    return render(request, "frmCategoria.html")


def agregarCategoria(request):
    nombre = request.POST["txtNombre"]
    try:
        categoria = Categoria(catNombre= nombre)
        categoria.save()
        mensaje = "Categoria Agregada Correctamente"
    except Error as error:
        mensaje = f"Problemas al agregar categoria"

    retorno = {"mensaje":mensaje}
    return render(request,"frmCategoria.html",retorno)


def listarProductos(request):
    try:
        productos = Producto.objects.all()
        mensaje = ""
    except Error as error:
        mensaje = f"Problemas al listar los productos {error}"

    retorno = {"mensaje":mensaje, "listaProductos":productos}
    return render(request,"listarProductos.html",retorno)


def vistaProducto(request):
    try:
        categorias = Categoria.objects.all()
        mensaje = ""
    except Error as error:
        mensaje = f"Problemas {error}"       

    retorno = {"mensaje":mensaje, "listaCategorias": categorias, "producto":None}  
    return render(request,"frmProducto.html",retorno) 


def agregarProducto(request):
    nombre = request.POST["txtNombre"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"])
    idCategoria = int(request.POST["cbCategoria"])
    archivo = request.FILES["fileFoto"]
    try:
        #obtener la categoria de acuerdo a su id
        categoria = Categoria.objects.get(id=idCategoria)
        #crear el producto
        producto = Producto(proNombre=nombre, proCodigo=codigo, proPrecio=precio,
                            proCategoria=categoria, proFoto=archivo)
        #registrarlo en la base de datos
        producto.save()
        mensaje = "Producto agregado correctamente"
        return redirect('/listarProductos/')
    except Error as error:
        mensaje = f"Problemas al registrar el producto {error}" 

        categoria = Categoria.objects.all()
        retorno = {"mensaje": mensaje, "listaCategorias": categoria, "producto": producto,}
        return render(request, "frmProducto.html", retorno)


def consultarProducto(request, id):
    try:
        producto = Producto.objects.get(id=id)
        categorias = Categoria.objects.all()
        mensaje=""
    except Error as error:
        mensaje = f"Problemas {error}"

    retorno = {"mensaje": mensaje, "producto": producto,
                "listaCategorias": categorias}
    return render(request, "frmEditarProducto.html", retorno)


def actualizarProducto(request):
    idProducto = int(request.POST["idProducto"])
    nombre = request.POST["txtNombreP"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"])
    idCategoria = int(request.POST["cbCategoria"])
    archivo = request.FILES.get("fileFoto", False)
    try:
        #obtener la categoria de acuerdo a su id
        categoria = Categoria.objects.get(id=idCategoria)
        #actualizar el producto. PRIMERO SE CONSULTA
        producto = Producto.objects.get(id=idProducto)
        producto.proNombre=nombre
        producto.proPrecio=precio
        producto.proCategoria=categoria
        producto.proCodigo=codigo
        #si el campo de foto tiene datos actualiza foto
        if(archivo):
            producto.proFoto = archivo
        else:
            producto.proFoto  = producto.proFoto
        producto.save()
        mensaje = "Producto actualizado correctamente"
        return redirect("/listarProductos/")

    except Error as error:
        mensaje = f"Problemas al realizar el proceso de actualizar el producto {error}"
    categorias = Categoria.objects.all()
    retorno = {"mensaje":mensaje, "listaCategorias":categorias, "producto":producto}      
    return render(request,"frmEditarProducto.html",retorno)

def eliminar(request,id):
    try:
        producto = Producto.objects.get(id=id)
        rutaFile = (producto.proFoto.url).split("/")
        root = "\\"+str(rutasFile[2])+"\\"+(rutaFile[3])

        os.moremove(os.path.join(settings.MEDIA_ROOT+root))
        
        producto.delete()
        mensaje="Producto eliminado!"

    except Error as error:
        mensaje = f"Problemas al eliminar el producto {error}"
    retorno = {"mensaje":mensaje}
    return redirect("/listarProductos/",retorno)