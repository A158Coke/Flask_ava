from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db1, Producto, Albaran, albaran_producto, Factura, factura_producto
from form import FacturaForm, AlbaranForm
from flask import flash
from datetime import datetime
from sqlalchemy import update


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "YuChenProject"
db1.init_app(app)


def create_tables():
    with app.app_context():
        db1.create_all()


create_tables()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stock", methods=["GET", "POST"])
def stock():
    productos = Producto.query.all()
    #print("productos: " + str(productos))
    return render_template("stock.html", productos=productos)


@app.route("/factura", methods=["GET", "POST"])
def factura():
    form = FacturaForm()
    productos = Producto.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            factura = Factura(fecha=datetime.utcnow())
            db1.session.add(factura)  
            db1.session.commit()  
            for i in range(1, 6):
                nombre_field = getattr(form, f"nombre{i}")
                cantidad_field = getattr(form, f"cantidad{i}")
                nombre = nombre_field.data
                cantidad = cantidad_field.data
                producto = Producto.query.filter_by(nombre=nombre).first()
                if producto:
                    if cantidad is not None and cantidad > 0:
                        if producto.cantidad >= cantidad:
                            factura.productos.append(producto) 
                            producto.cantidad -= cantidad
                            db1.session.commit()
                            db1.session.execute(update(factura_producto).where(factura_producto.c.producto_id == producto.id).values(cantidad = cantidad))
                            db1.session.commit()
                        else:
                            print(f"No hay suficiente cantidad de {producto.nombre} en stock.")
                else:
                    print("NO encuentra el producto en el base de datos")
            return redirect(request.url)
            print("Factura procesada correctamente")
            return redirect(url_for("stock"))
        else:
            print("Error en el formulario.")
    return render_template("factura.html", productos=productos, form=form)




@app.route("/albaran", methods=["GET", "POST"])
def albaran():
    print("Dentro del albaran")
    form = AlbaranForm()
    if request.method == "POST" and form.validate():
        print("HA pasado el validator de form")
        albaran = Albaran()
        albaran.fecha = datetime.utcnow()
        db1.session.add(albaran) 
        db1.session.commit()
        for i in range(1, 6):
            nombre_field = getattr(form, f"nombre{i}")
            cantidad_field = getattr(form, f"cantidad{i}")
            nombre = nombre_field.data
            cantidad = cantidad_field.data
            if nombre and cantidad:
                producto_existe = Producto.query.filter_by(nombre=nombre).first()
                if producto_existe:
                    print(f"{nombre} ya existe, añadimos la cantidad sin crear un nuevo producto")
                    producto_existe.cantidad += cantidad 
                    albaran.productos.append(producto_existe)
                    db1.session.commit()
                    db1.session.execute(update(albaran_producto).where(albaran_producto.c.producto_id == producto_existe.id).values(cantidad = cantidad))
                    db1.session.commit()
                else:
                    nuevo_producto = Producto(nombre=nombre, cantidad=cantidad)
                    albaran.productos.append(nuevo_producto)
                    db1.session.add(nuevo_producto)
                    db1.session.commit()  
                    db1.session.execute(update(albaran_producto).where(albaran_producto.c.producto_id == nuevo_producto.id).values(cantidad = cantidad))
                    db1.session.commit() 
        print("Actualizado")
        return redirect(url_for("stock"))
    return render_template("albaran.html", form=form)









if __name__ == "__main__":
    app.run(debug=False)
