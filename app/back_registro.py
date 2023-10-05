from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connetor

app = Flask(__name__)

# Configuración de la base de datos
db = mysql.connetor.connect(
    host="localhost",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="mydb"
)

# Ruta para el formulario de registro
@app.route('/registrarse', methods=['GET', 'POST'])
def registro():
    global request
    if request.method == 'POST':
        nombre = request.form['inputNombre']
        apellido = request.form['inputApellido']
        email = request.form['inputEmail']
        confirmar_email = request.form['inputConfirmarEmail']
        contraseña = request.form['inputContraseña']
        confirmar_contraseña = request.form['inputConfirmarContraseña']
        direccion = request.form['inputDirección']
        telefono = request.form['inputTeléfono']
        ciudad = request.form['inputCiudad']
        codigo_postal = request.form['inputCódigoPostal']

        # Validar que los campos de contraseña y correo electrónico coincidan
        if email != confirmar_email:
            flash('Los correos electrónicos no coinciden', 'danger')
            return redirect(url_for('registrarse'))

        if contraseña != confirmar_contraseña:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('registrarse'))

        cursor = db.cursor()

        # Verificar si el correo electrónico ya está registrado
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('registrarse'))
        else:
            # Insertar el nuevo usuario en la base de datos
            cursor.execute(
                "INSERT INTO users (nombre, apellido, email, contraseña, direccion, telefono, ciudad, codigo_postal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (nombre, apellido, email, contraseña, direccion, telefono, ciudad, codigo_postal)
            )
            db.commit()
            flash('Registro exitoso', 'success')
            return redirect(url_for('registrarse'))

    return render_template('registrarse.html')

if __name__ == '__main__':
    app.run(debug=True)