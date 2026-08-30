from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(message="El nombre del proveedor es obligatorio."),
            Length(min=2, max=100, message="Debe tener entre 2 y 100 caracteres.")
        ]
    )

    empresa = StringField(
        "Empresa",
        validators=[
            DataRequired(message="La empresa es obligatoria."),
            Length(min=2, max=100, message="Debe tener entre 2 y 100 caracteres.")
        ]
    )

    email = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=7, max=15, message="El teléfono debe tener entre 7 y 15 caracteres.")
        ]
    )

    submit = SubmitField("Guardar proveedor")