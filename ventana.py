import flet
from flet import *
import sqlite3
import time

conn = sqlite3.connect('base.db')
c = conn.cursor()

# Ventana Principal
def ventana_principal(page: Page):

    # tema
    page.theme_mode = ThemeMode.DARK
    page.scroll = ScrollMode.AUTO
    

    # Variables
        # Funciones
    def cerrar_dlg(e):
        alerta.open = False
        page.update()
    
    alerta = AlertDialog(
            modal=True,
            title=Text('Se ha guardado Correctamente'),
            actions=[
                TextButton('Ok', on_click=cerrar_dlg)
                ],
            )
    def mostrar_agregar(e):
        mostrar.offset = transform.Offset(0,0)
        page.update()
    
    def cerrar_agregar(e):
        mostrar.offset = transform.Offset(2,0)
        page.update()

    # Display
    txt_nombre = TextField(label='Nombre', autofocus=True)
    txt_edad = TextField(label='Edad')
    txt_comentario = TextField(label='Comentario')
    selet_consulta = Dropdown(
            options=[
                dropdown.Option('Limpieza'),
                dropdown.Option('Extraccion Cordal'),
                dropdown.Option('Ortodoncia'),
            ],
    )
    
    def guardar_datos(e):
        conn = sqlite3.connect('base.db')
        c = conn.cursor()        
        c.execute('INSERT INTO pacientes(nombre, edad, consulta, comentario) VALUES(?,?,?,?)', (txt_nombre.value, txt_edad.value, selet_consulta.value, txt_comentario.value))
        conn.commit()
        conn.close()

        txt_nombre.value = ""
        txt_edad.value = ""
        selet_consulta.value = ""
        txt_comentario.value = ""

        tabla.rows.clear()
        llamar_base(e)
        tabla.update()

        page.dialog = alerta
        alerta.open = True
        page.update()


    

    # Check Primera Vez
    check_primera = Checkbox(label='Primera vez del paciente?', value=False)
    
    # Boton Guardar
    
    # Tabla
    tabla = DataTable(
            columns=[
                DataColumn(Text('Accion')),
                DataColumn(Text('Nombre')),
                DataColumn(Text('Edad')),
                DataColumn(Text('Consulta')),
                DataColumn(Text('Comentario')),
                ],
            rows=[]

            )
    
    def eliminar(e):
        myid = int(e.control.data)
        conn = sqlite3.connect('base.db')
        c = conn.cursor()
        c.execute('DELETE FROM pacientes WHERE id=?', [myid])
        conn.commit()
        conn.close()

        tabla.rows.clear()
        llamar_base(e)
        tabla.update()

    def editar(e):
        pass
        

    def llamar_base(e):
        conn = sqlite3.connect('base.db') 
        c = conn.cursor()
        c.execute('SELECT * FROM pacientes')
        pacientes = c.fetchall()
        print(pacientes)
        if not pacientes == "":
            keys = ['id', 'nombre', 'edad','consulta', 'comentario']
            result = [dict(zip(keys, values)) for values in pacientes]
            for x in result:
                tabla.rows.append(
                        DataRow(
                cells=[
                    DataCell(Row([
                        IconButton(icon='create', icon_color='blue',
                                   data=x,
                                   on_click=editar
                                   ),
                        IconButton(icon='delete', icon_color='red',
                                   data=x['id'],
                                   on_click=eliminar
                                   ),

                        ])),
                    DataCell(Text(x['nombre'])),
                    DataCell(Text(x['edad'])),
                    DataCell(Text(x['consulta'])),
                    DataCell(Text(x['comentario'])),

                    ],
                ),
        )
        tabla.update()
        page.update()
        

    
    mostrar = Card(
            offset=transform.Offset(2,0),
            animate_offset = animation.Animation(300, curve='bounceOut'),
            elevation=30,
            content=Container(
                content=Column([
                    Row([
                        Text('Agrega un nuevo paciente', size=20, weight='bold', font_family='CaskaydiaCove Nerd Font Mono'),
                        IconButton(icon='close', icon_size=30,
                        on_click=cerrar_agregar
                        ),
                        ]),
                    
                    txt_nombre,
                    txt_edad,
                    selet_consulta,
                    txt_comentario,
                    FilledButton('Guardar', on_click=guardar_datos)
                    ])
                )

            )


    
    page.add(
            Row([
                Text('Agenda Consultorio', size=30, weight='bold', font_family='CaskaydiaCove Nerd Font Mono'),
                ]),
            Row([
                ElevatedButton('Agregar Nuevo Paciente', on_click=mostrar_agregar),
                ElevatedButton('Mostrar Datos', on_click=llamar_base),
                ]),
            Column([
                tabla,
                mostrar
                ])
            )


    

flet.app(target=ventana_principal)
