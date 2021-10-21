import os, pathlib, random
from operator import contains
from flask import request
from ..modelos import db, Usuario, UsuarioSchema, Tarea, TareaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
from werkzeug.utils import secure_filename 

usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()
 
# end point: /api/tasks
class VistaTareas(Resource):
    def post(self):
        usuario_id = 1
        # Carpeta de subida    
        UPLOAD_FOLDER = '../backend/files/uploaded/'
        # obtenemos el archivo del input "fileName" de postman 
        f = request.files['fileName'] 
        filename = secure_filename(f.filename)
        path = pathlib.Path(UPLOAD_FOLDER + filename)
        # obtenemos el input "fileName" de postman con el Formato al que desea cambiar el archivo cargado
        formato = request.form['newFormat']
        #Si entrada está vacio, se ejecuta el if
        if not f:
            return {"mensaje":"INGRESE ARCHIVO A CONVERTIR"}
        elif not formato:
            return {"mensaje":"INGRESE FORMATO A CONVERTIR EL ARCHIVO"}
        else:        
            Extension = path.suffix
            # Guardamos el archivo en el directorio "UPLOAD_FOLDER"
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            
            # Retornamos una respuesta satisfactoria
            Parent = path.parent
            Filename = path.name
            Extension = path.suffix
            nueva_tarea = Tarea(archivo = Filename,
            formato = formato,
            fecha = datetime.today(),
            estado = "UPLOADED",
            usuario_id = usuario_id)            
            db.session.add(nueva_tarea)
            db.session.commit()
            token_de_acceso = create_access_token(identity = usuario_id)
            return {"mensaje":"La tarea fue creada exitosamente", "token":token_de_acceso}
             
# end point: /api/tasks/<int:id_task>
class VistaTarea(Resource):
    def get(self, id_task):
        exit_tarea = Tarea.query.filter(Tarea.id == id_task).first()
        db.session.commit()
        if exit_tarea is None:
            return {"mensaje":"La tarea no existe, no se puede consultar"}
        else:
            return tarea_schema.dump(Tarea.query.get_or_404(id_task))