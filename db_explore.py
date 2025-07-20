import sqlite3
import os
from datetime import datetime
from tabulate import tabulate

class DatabaseExplorer:
    def __init__(self, db_path='notes.db'):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Conectar a la base de datos"""
        if not os.path.exists(self.db_path):
            print(f"❌ No se encontró la base de datos '{self.db_path}'")
            return False
        
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print(f"✅ Conectado a la base de datos '{self.db_path}'")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error al conectar: {e}")
            return False
    
    def disconnect(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            print("👋 Conexión cerrada")
    
    def get_tables(self):
        """Obtener lista de tablas"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        return [table['name'] for table in tables]
    
    def get_table_info(self, table_name):
        """Obtener información de las columnas de una tabla"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        return cursor.fetchall()
    
    def get_table_count(self, table_name):
        """Obtener número de registros en una tabla"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        return cursor.fetchone()['count']
    
    def show_tables(self):
        """Mostrar todas las tablas con información"""
        tables = self.get_tables()
        
        print("\n📊 TABLAS EN LA BASE DE DATOS:")
        print("=" * 50)
        
        for table in tables:
            count = self.get_table_count(table)
            print(f"\n📁 Tabla: {table} ({count} registros)")
            
            # Obtener estructura de la tabla
            columns = self.get_table_info(table)
            col_data = []
            
            for col in columns:
                col_data.append([
                    col['name'],
                    col['type'],
                    '✓' if col['pk'] else '',
                    '✓' if col['notnull'] else '',
                    col['dflt_value'] if col['dflt_value'] else ''
                ])
            
            headers = ['Columna', 'Tipo', 'PK', 'NOT NULL', 'Default']
            print(tabulate(col_data, headers=headers, tablefmt='grid'))
    
    def show_users(self):
        """Mostrar todos los usuarios"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
        users = cursor.fetchall()
        
        print("\n👥 USUARIOS REGISTRADOS:")
        print("=" * 50)
        
        if users:
            user_data = []
            for user in users:
                user_data.append([
                    user['id'],
                    user['username'],
                    user['email'],
                    user['created_at']
                ])
            
            headers = ['ID', 'Usuario', 'Email', 'Fecha Registro']
            print(tabulate(user_data, headers=headers, tablefmt='grid'))
        else:
            print("No hay usuarios registrados")
    
    def show_notes(self, limit=10):
        """Mostrar las últimas notas"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT n.id, n.title, u.username, n.created_at, 
                   LENGTH(n.content) as content_length
            FROM notes n
            JOIN users u ON n.user_id = u.id
            ORDER BY n.created_at DESC
            LIMIT ?
        """, (limit,))
        notes = cursor.fetchall()
        
        print(f"\n📝 ÚLTIMAS {limit} NOTAS:")
        print("=" * 50)
        
        if notes:
            note_data = []
            for note in notes:
                note_data.append([
                    note['id'],
                    note['title'][:40] + '...' if len(note['title']) > 40 else note['title'],
                    note['username'],
                    f"{note['content_length']} chars",
                    note['created_at']
                ])
            
            headers = ['ID', 'Título', 'Usuario', 'Tamaño', 'Fecha']
            print(tabulate(note_data, headers=headers, tablefmt='grid'))
        else:
            print("No hay notas en la base de datos")
    
    def show_user_notes(self, username):
        """Mostrar notas de un usuario específico"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT n.id, n.title, n.created_at, n.updated_at
            FROM notes n
            JOIN users u ON n.user_id = u.id
            WHERE u.username = ?
            ORDER BY n.created_at DESC
        """, (username,))
        notes = cursor.fetchall()
        
        print(f"\n📝 NOTAS DE '{username}':")
        print("=" * 50)
        
        if notes:
            note_data = []
            for note in notes:
                note_data.append([
                    note['id'],
                    note['title'][:50] + '...' if len(note['title']) > 50 else note['title'],
                    note['created_at'],
                    note['updated_at'] if note['updated_at'] else 'No modificada'
                ])
            
            headers = ['ID', 'Título', 'Creada', 'Modificada']
            print(tabulate(note_data, headers=headers, tablefmt='grid'))
        else:
            print(f"No se encontraron notas para el usuario '{username}'")
    
    def show_statistics(self):
        """Mostrar estadísticas de la base de datos"""
        cursor = self.conn.cursor()
        
        print("\n📈 ESTADÍSTICAS:")
        print("=" * 50)
        
        # Total usuarios
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()['count']
        
        # Total notas
        cursor.execute("SELECT COUNT(*) as count FROM notes")
        total_notes = cursor.fetchone()['count']
        
        # Usuario con más notas
        cursor.execute("""
            SELECT u.username, COUNT(n.id) as note_count
            FROM users u
            LEFT JOIN notes n ON u.id = n.user_id
            GROUP BY u.id
            ORDER BY note_count DESC
            LIMIT 1
        """)
        top_user = cursor.fetchone()
        
        # Promedio de notas por usuario
        avg_notes = total_notes / total_users if total_users > 0 else 0
        
        stats_data = [
            ['Total de usuarios', total_users],
            ['Total de notas', total_notes],
            ['Promedio notas/usuario', f"{avg_notes:.2f}"],
            ['Usuario más activo', f"{top_user['username']} ({top_user['note_count']} notas)" if top_user else 'N/A']
        ]
        
        print(tabulate(stats_data, headers=['Métrica', 'Valor'], tablefmt='grid'))
    
    def execute_query(self, query):
        """Ejecutar una consulta SQL personalizada"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            # Si es SELECT, mostrar resultados
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                if results:
                    # Obtener nombres de columnas
                    columns = [description[0] for description in cursor.description]
                    
                    # Convertir resultados a lista
                    data = []
                    for row in results:
                        data.append([row[col] for col in columns])
                    
                    print(tabulate(data, headers=columns, tablefmt='grid'))
                else:
                    print("La consulta no devolvió resultados")
            else:
                self.conn.commit()
                print(f"✅ Consulta ejecutada. Filas afectadas: {cursor.rowcount}")
                
        except sqlite3.Error as e:
            print(f"❌ Error en la consulta: {e}")

def main_menu():
    """Menú principal interactivo"""
    explorer = DatabaseExplorer()
    
    if not explorer.connect():
        return
    
    while True:
        print("\n🔍 EXPLORADOR DE BASE DE DATOS")
        print("=" * 50)
        print("1. Ver estructura de tablas")
        print("2. Ver usuarios registrados")
        print("3. Ver últimas notas")
        print("4. Ver notas de un usuario")
        print("5. Ver estadísticas")
        print("6. Ejecutar consulta SQL")
        print("0. Salir")
        
        choice = input("\nSelecciona una opción: ")
        
        if choice == '1':
            explorer.show_tables()
        
        elif choice == '2':
            explorer.show_users()
        
        elif choice == '3':
            limit = input("¿Cuántas notas mostrar? (default: 10): ")
            limit = int(limit) if limit.isdigit() else 10
            explorer.show_notes(limit)
        
        elif choice == '4':
            username = input("Nombre de usuario: ")
            explorer.show_user_notes(username)
        
        elif choice == '5':
            explorer.show_statistics()
        
        elif choice == '6':
            print("\n💡 Ejemplos de consultas:")
            print("  SELECT * FROM users LIMIT 5")
            print("  SELECT title, content FROM notes WHERE user_id = 1")
            print("  SELECT COUNT(*) FROM notes WHERE created_at > '2024-01-01'")
            query = input("\nEscribe tu consulta SQL: ")
            if query:
                explorer.execute_query(query)
        
        elif choice == '0':
            break
        
        else:
            print("❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")
    
    explorer.disconnect()

if __name__ == "__main__":
    # Si se ejecuta directamente, mostrar menú interactivo
    main_menu()