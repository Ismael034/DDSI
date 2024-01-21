from app.query.articulo import articulo
from app.query.tienda import tienda
from app.query.social import social
from app.query.dev import dev
import logging

class query:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def create_tables(self):
        try:
            social(self.db).create_tables()
            articulo(self.db).create_tables()
            tienda(self.db).create_tables()
            dev(self.db).create_tables()
        
        except Exception as ex:
            logging.error("Error creating tables: ", ex)
            self.db.rollback()

    def get_tables(self):
        try:
            self.db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting tables: ", ex)

    def delete_tables(self):
        try:
            self.db.execute("DROP TABLE IF EXISTS Listar_Creacion")
            self.db.execute("DROP TABLE IF EXISTS Consultar_Creacion")
            self.db.execute("DROP TABLE IF EXISTS Creacion")

            self.db.execute("DROP TABLE IF EXISTS Compra")
            self.db.execute("DROP TABLE IF EXISTS Videojuego")

            self.db.execute("DROP TABLE IF EXISTS Valoracion")
            self.db.execute("DROP TABLE IF EXISTS Articulo_obtenido")
            self.db.execute("DROP TABLE IF EXISTS Articulo")

            self.db.execute("DROP TABLE IF EXISTS Amistad")
            self.db.execute("DROP TABLE IF EXISTS Perfil")
            self.db.execute("DROP TABLE IF EXISTS Usuario")
            
            self.db.execute(f"DROP TRIGGER IF EXISTS actualizar_saldo")
            self.db.execute(f"DROP TRIGGER IF EXISTS crear_perfil")
            self.db.execute(f"DROP TRIGGER IF EXISTS anadir_articulo_usuario")
            self.db.execute(f"DROP TRIGGER IF EXISTS tipo_creacion_valido")
            
            self.db.commit()
        except Exception as ex:
            logging.error("Error deleting tables: ", ex)
            self.db.rollback()

    def insert_data(self):
        try:
            # Insert 10 users
            social(self.db).insert_usuario('acanas23', 'Antonio Cañas', 'acanas@gmail.com', 'acanas23', 80000, '')
            social(self.db).insert_usuario('swadder2', 'swadder2', 'swadder2@gmail.com', '1234', 2345, '')
            social(self.db).insert_usuario('swadder3', 'swadder3', 'swadder3@gmail.com', '1234', 4, '')
            social(self.db).insert_usuario('swadder4', 'swadder4', 'swadder4@gmail.com', '1234', 0, '')
            social(self.db).insert_usuario('swadder5', 'swadder5', 'swadder5@gmail.com', '1234', 3453, '')
            social(self.db).insert_usuario('swadder6', 'swadder6', 'swadder6@gmail.com', '1234', 1, '')
            social(self.db).insert_usuario('swadder7', 'swadder7', 'swadder7@gmail.com', '1234', 234, '')
            social(self.db).insert_usuario('swadder8', 'swadder8', 'swadder8@gmail.com', '1234', 0, '')
            social(self.db).insert_usuario('swadder9', 'swadder9', 'swadder9@gmail.com', '1234', 2343, '')
            social(self.db).insert_usuario('swadder10', 'swadder10', 'swadder10@gmail.com', '1234', 100, '')

            # Modificar perfil
            social(self.db).update_perfil('acanas23', '/resources/foto/acanas.png', 'EC mejor que AC', 'Millón de click en swad')
            social(self.db).update_perfil('swadder1', '/resources/foto/usuario1.png', 'Biografía de ejemplo del usuario1', 'Swad Souls No hit') 
            social(self.db).update_perfil('swadder5', '/resources/foto/usuario2.png', 'Biografía de ejemplo del usuario2', 'Tu primera victoria en Swad Battle Royale')
            social(self.db).update_perfil('swadder7', '/resources/foto/usuario3.png', 'Biografía de ejemplo del usuario3', 'New Super Cañas Bros sin conseguir ninguna moneda')
            social(self.db).update_perfil('swadder8', '/resources/foto/usuario4.png', 'Biografía de ejemplo del usuario4', 'Crafteo de una espada de diamante en Swadcraft')
            social(self.db).update_perfil('swadder9', '/resources/foto/usuario4.png', 'Biografía de ejemplo del usuario4', 'Hacer un pentakill en Swad Legends')

            social(self.db).insert_amistad('acanas23', 'swadder2')
            social(self.db).insert_amistad('swadder6', 'swadder3')
            social(self.db).insert_amistad('swadder8', 'swadder4')
            social(self.db).insert_amistad('swadder10', 'swadder5')

            social(self.db).accept_amistad('acanas23', 'swadder2')
            social(self.db).accept_amistad('swadder8', 'acanas23')

            # Insertar 10 videojuegos
            articulo(self.db).subir_articulo('New Super Cañas Bros', '100GB', 'Juego de plataformas en 2D', 'Juego de plataformas en 2D', 'Plataformas', '/resources/foto/juego1.png', '/resources/ejecutable/juego1.exe', 'Windows 10, 4GB RAM, 1GB VRAM')
            tienda(self.db).insert_videojuego('New Super Cañas Bros', 10, '1.0', 'acanas23', 'Plataformas')

            articulo(self.db).subir_articulo('Swadcraft', '200GB', 'Juego de construcción', 'Juego de construcción', 'Construcción', '/resources/foto/juego2.png', '/resources/ejecutable/juego2.exe', 'Windows 10, 4GB RAM, 2GB VRAM')
            tienda(self.db).insert_videojuego('Swadcraft', 20, '1.0', 'swadder8', 'Construcción')

            articulo(self.db).subir_articulo('Swad Legends', '300GB', 'Juego de Acción', 'Juego de lucha', 'Acción', '/resources/foto/juego3.png', '/resources/ejecutable/juego3.exe', 'Windows 10, 4GB RAM, 3GB VRAM')
            tienda(self.db).insert_videojuego('Swad Legends', 30, '1.0', 'swadder10', 'Acción')

            articulo(self.db).subir_articulo('Swad Souls', '400GB', 'Juego de rol', 'Juego de rol', 'Rol', '/resources/foto/juego4.png', '/resources/ejecutable/juego4.exe', 'Windows 10, 4GB RAM, 4GB VRAM')
            tienda(self.db).insert_videojuego('Swad Souls', 40, '1.0', 'acanas23', 'Rol')

            articulo(self.db).subir_articulo('Swad Battle Royale', '500GB', 'Juego de acción', 'Juego de acción', 'Acción', '/resources/foto/juego5.png', '/resources/ejecutable/juego5.exe', 'Windows 10, 4GB RAM, 5GB VRAM')
            tienda(self.db).insert_videojuego('Swad Battle Royale', 50, '1.0', 'acanas23', 'Acción')

            articulo(self.db).subir_articulo('Swad Souls 2', '600GB', 'Juego de rol', 'Juego de rol', 'Rol', '/resources/foto/juego6.png', '/resources/ejecutable/juego6.exe', 'Windows 10, 4GB RAM, 6GB VRAM')
            tienda(self.db).insert_videojuego('Swad Souls 2', 60, '1.0', 'acanas23', 'Rol')

            articulo(self.db).subir_articulo('Swad Souls 3', '700GB', 'Juego de rol', 'Juego de rol', 'Rol', '/resources/foto/juego7.png', '/resources/ejecutable/juego7.exe', 'Windows 10, 4GB RAM, 7GB VRAM')
            tienda(self.db).insert_videojuego('Swad Souls 3', 70, '1.0', 'acanas23', 'Rol')

            # Insertar 10 creaciones
            articulo(self.db).subir_articulo('Skin de Antonio Cañas', '100MB', 'Pack de textura de Cañas comprimida', 'Añade a Dark Souls 3 la skin de Antonio Cañas', 'Acción', '/resources/foto/creacion1.png', '/resources/ejecutable/creacion1.exe', 'Windows 10, 64GB RAM, 20GB VRAM')
            dev(self.db).subir_creacion('Skin de Antonio Cañas', 'TEXTURE_PACK', 'acanas23')

            articulo(self.db).subir_articulo('Mapa de Antonio Cañas', '200MB', 'Mapa de Cañas comprimido', 'Añade a Swadcraft el mapa de Antonio Cañas', 'Construcción', '/resources/foto/creacion2.png', '/resources/ejecutable/creacion2.exe', 'Windows 10, 64GB RAM, 20GB VRAM')
            dev(self.db).subir_creacion('Mapa de Antonio Cañas', 'MOD_JUGABLE', 'acanas23')

            articulo(self.db).subir_articulo('Mod de Antonio Cañas', '300MB', 'Mod de Cañas comprimido', 'Añade a Swadcraft el mod de Antonio Cañas', 'Construcción', '/resources/foto/creacion3.png', '/resources/ejecutable/creacion3.exe', 'Windows 10, 64GB RAM, 20GB VRAM')
            dev(self.db).subir_creacion('Mod de Antonio Cañas', 'MOD_JUGABLE', 'acanas23')

            articulo(self.db).subir_articulo('Fangame de Legend Of Cañas', '400MB', 'Fangame del famosísimo juego Legend Of Cañas', 'Un juego de acción y aventuras en donde escribes tu propia historia acompañado de Antonio Cañas', 'Acción', '/resources/foto/creacion4.png', '/resources/ejecutable/creacion4.exe', 'Uwuntu, 2GB RAM, 6GB VRAM')
            dev(self.db).subir_creacion('Fangame de Legend Of Cañas', 'FANGAME', 'swadder2')

            articulo(self.db).subir_articulo('Demo de Counter Strike Cañas Offensive', '500MB', 'Demo del famosísimo juego Counter Strike Cañas Offensive', 'Un juego de acción y disparos en donde escribes tu propia historia acompañado de Antonio Cañas', 'Acción', '/resources/foto/creacion5.png', '/resources/ejecutable/creacion5.exe', 'Arch Linux, 64GB RAM, 20GB VRAM')
            dev(self.db).subir_creacion('Demo de Counter Strike Cañas Offensive', 'DEMO', 'swadder2')

            articulo(self.db).subir_articulo('Pack de texturas del edificio de la ETSIIT', '600MB', 'Pack de texturas del edificio de la ETSII comprimido', 'Añade a Swad Battle Royale el pack de texturas del edificio de la ETSII', 'Construcción', '/resources/foto/creacion6.png', '/resources/ejecutable/creacion6.exe', 'Hanna Montana Linux, 6GB RAM, 0GB VRAM')
            dev(self.db).subir_creacion('Pack de texturas del edificio de la ETSIIT', 'TEXTURE_PACK', 'swadder2')

            # Compra
            tienda(self.db).comprar_videojuego('New Super Cañas Bros', 'acanas23')
            articulo(self.db).anadir_articulo_obtenido('acanas23', 'New Super Cañas Bros')

            tienda(self.db).comprar_videojuego('Swadcraft', 'acanas23')
            articulo(self.db).anadir_articulo_obtenido('acanas23', 'Swadcraft')

            tienda(self.db).comprar_videojuego('Swad Legends', 'acanas23')
            articulo(self.db).anadir_articulo_obtenido('acanas23', 'Swad Legends')

            tienda(self.db).comprar_videojuego('Swad Souls', 'acanas23')
            articulo(self.db).anadir_articulo_obtenido('acanas23', 'Swad Souls')

            tienda(self.db).comprar_videojuego('Swad Battle Royale', 'acanas23')
            articulo(self.db).anadir_articulo_obtenido('acanas23', 'Swad Battle Royale')

            tienda(self.db).comprar_videojuego('Swad Souls 2', 'acanas23')
            articulo(self.db).anadir_articulo_obtenido('acanas23', 'Swad Souls 2')

            tienda(self.db).comprar_videojuego('Swad Souls 3', 'acanas23')
            articulo(self.db).anadir_articulo_obtenido('acanas23', 'Swad Souls 3')


            tienda(self.db).comprar_videojuego('Swad Souls 3', 'swadder2')
            articulo(self.db).anadir_articulo_obtenido('swadder2', 'Swad Souls 3')


            # Valoraciones
            articulo(self.db).comentar('acanas23', 'New Super Cañas Bros', 5, 'GOTY')
            articulo(self.db).comentar('swadder2', 'New Super Cañas Bros', 5, 'Juegazo')

            articulo(self.db).comentar('swadder2', 'Swadcraft', 4, 'Mierdón bíblico')
            articulo(self.db).comentar('swadder3', 'Swad Souls 2', 3, 'Mejor que la pizza con piña')




        except Exception as ex:
            logging.error("Error inserting data: ", ex)
            self.db.rollback()


            
