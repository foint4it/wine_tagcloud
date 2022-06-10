import sqlite3
conn = sqlite3.connect('escuelas.db',check_same_thread=False)
c = conn.cursor()

# querys insercion registros

def add_insp_cab(unidad,fecha,obs,prioridad,apoyo):
    c.execute('INSERT INTO inspeccion(UnidadId,InspeccionDate,Observacion,PrioridadId,Apoyo) VALUES (?,?,?,?,?)',(unidad,fecha,obs,prioridad,apoyo))
    conn.commit()
    c.execute('SELECT MAX(InspeccionId) FROM inspeccion')
    data = c.fetchall()
    return data[0]

def add_insp_det(insp, prof_apoyo):
    c.execute('INSERT INTO inspeccion_apoyo(InspeccionId,ApoyoId) VALUES (?,?)',(insp,prof_apoyo))
    conn.commit()

def add_uee_cab(escuela,turno,ciclo,conduccion,periodo,descripcion):
    c.execute('INSERT INTO unidad_especial(EscuelaId,TurnoId,CicloId,ConduccionId,Periodo,Descripcion) VALUES (?,?,?,?,?,?)',(escuela,turno,ciclo,conduccion,periodo,descripcion))
    conn.commit()
    c.execute('SELECT MAX(UnidadId) FROM unidad_especial')
    data = c.fetchall()
    return data[0]

def add_uee_det(unidad,doc_esp):
    c.execute('INSERT INTO unidad_items(UnidadId,DocenteId) VALUES (?,?)',(unidad,doc_esp))
    conn.commit()

def add_pee(apellido, nombre, cat, funcion, telefono, email, docesp, conduccion, apoyo):
    c.execute('INSERT INTO personal(Apellido,Nombre,CatId,FuncionId,Telefono,Email,DocEspecial,Conduccion,Apoyo) VALUES (?,?,?,?,?,?,?,?,?)',(apellido, nombre, cat, funcion, telefono, email, docesp, conduccion, apoyo))
    conn.commit()

def add_eee(nombre, dist, conduccion, domicilio, ciudad, cpostal, tel, email, geo, escesp):
    c.execute('INSERT INTO escuela(Nombre,DistritoId,AutoridadId,Domicilio,Ciudad,CodigoPostal,Telefono,Email,LocationGeo,EduEspecial) VALUES (?,?,?,?,?,?,?,?,?,?)',(nombre, dist, conduccion, domicilio, ciudad, cpostal, tel, email, geo, escesp))
    conn.commit()


# vistas para consultas

def view_all_insp():
	c.execute('SELECT InspeccionId,UnidadId,Nombre_Unidad,InspeccionDate,Observacion,Prioridad,Apoyo,ApoyoId,Nombre_Completo FROM vw_inspeccion')
	data = c.fetchall()
	return data

def view_all_insp_cab():
	c.execute('SELECT InspeccionId,UnidadId,Nombre_Unidad,InspeccionDate,Observacion,Prioridad,Apoyo FROM vw_inspeccion_cab')
	data = c.fetchall()
	return data

def view_all_uee():
	c.execute('SELECT * FROM vw_unidad_especial')
	data = c.fetchall()
	return data

def view_all_escuelas():
	c.execute('SELECT * FROM vw_escuela')
	data = c.fetchall()
	return data

def view_all_docesp():
	c.execute('SELECT * FROM vw_docente_especial')
	data = c.fetchall()
	return data

def view_all_conduccion():
	c.execute('SELECT * FROM vw_conduccion')
	data = c.fetchall()
	return data

def view_all_apoyo():
	c.execute('SELECT * FROM vw_apoyo_especial')
	data = c.fetchall()
	return data

# vista "inspeccion_total" para tablas cruzadas, graficos y csv
def view_inspeccion_tot():
	c.execute('SELECT * FROM vw_inspeccion_all')
	data = c.fetchall()
	return data

def view_inspeccion_nodet():
	c.execute('SELECT * FROM vw_inspeccion_nodet')
	data = c.fetchall()
	return data

# vistas pick list

def pl_unidad():
	c.execute('SELECT DISTINCT UnidadId || "-" || Descripcion as Unidad FROM unidad_especial')
	data = c.fetchall()
	return data

def pl_prioridad():
	c.execute('SELECT DISTINCT PrioridadId || "-" || Nombre as Prioridad FROM prioridad')
	data = c.fetchall()
	return data

def pl_doc_esp():
    c.execute('select distinct PersonalId || "-" || Nombre_Completo || "-" || Funcion as DocEsp from vw_docente_especial')
    data = c.fetchall()
    return data

def pl_apoyo():
    c.execute('select distinct PersonalId || "-" || Nombre_Completo || "-" || Funcion as Apoyo from vw_apoyo_especial')
    data = c.fetchall()
    return data

def pl_conduccion():
    c.execute('select distinct PersonalId || "-" || Nombre_Completo || "-" || Funcion as Conduccion from vw_conduccion')
    data = c.fetchall()
    return data

def pl_cat():
	c.execute('SELECT DISTINCT CatId || "-" || Nombre as Categoria FROM categoria')
	data = c.fetchall()
	return data

def pl_funcion():
	c.execute('SELECT DISTINCT FuncionId || "-" || Nombre as Funcion FROM funcion')
	data = c.fetchall()
	return data

def pl_escuela():
	c.execute('SELECT DISTINCT EscuelaId || "-" || Nombre as Escuela FROM escuela')
	data = c.fetchall()
	return data

def pl_turno():
	c.execute('SELECT DISTINCT TurnoId || "-" || Nombre as Turno FROM turno')
	data = c.fetchall()
	return data

def pl_ciclo():
	c.execute('SELECT DISTINCT CicloId || "-" || Nombre as Ciclo FROM ciclo')
	data = c.fetchall()
	return data

def pl_distrito():
	c.execute('SELECT DISTINCT DistritoId || "-" || Nombre as Distrito FROM distrito')
	data = c.fetchall()
	return data





"""
def view_all_data():
	c.execute('SELECT * FROM taskstable')
	data = c.fetchall()
	return data

def view_all_task_names():
	c.execute('SELECT DISTINCT task FROM taskstable')
	data = c.fetchall()
	return data

def get_task(task):
	c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data

def get_task_by_status(task_status):
	c.execute('SELECT * FROM taskstable WHERE task_status="{}"'.format(task_status))
	data = c.fetchall()


def edit_task_data(new_task,new_task_status,new_task_date,task,task_status,task_due_date):
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_date,task,task_status,task_due_date))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(task):
	c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
	conn.commit()

"""

