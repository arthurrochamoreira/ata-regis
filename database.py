# Arquivo: database.py

import sqlite3
from typing import List, Dict, Any

DATABASE_NAME = 'atas_registro.db'

def connect_db():
    """Conecta ao banco de dados SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas como dicionário
    return conn

def init_db():
    """Cria as tabelas necessárias no banco de dados, se não existirem."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numeroAta TEXT NOT NULL,
            documentoSei TEXT,
            objeto TEXT NOT NULL,
            dataAssinatura TEXT NOT NULL,
            dataVigencia TEXT NOT NULL,
            fornecedor TEXT NOT NULL,
            createdAt TEXT,
            updatedAt TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telefones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ata_id INTEGER NOT NULL,
            telefone TEXT NOT NULL,
            FOREIGN KEY (ata_id) REFERENCES atas (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ata_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (ata_id) REFERENCES atas (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ata_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (ata_id) REFERENCES atas (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados inicializado.")

def insert_ata(ata_data: Dict[str, Any]):
    """Insere uma nova ata e seus dados relacionados."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO atas (numeroAta, documentoSei, objeto, dataAssinatura, dataVigencia, fornecedor, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        ata_data['numeroAta'],
        ata_data.get('documentoSei', ''),
        ata_data['objeto'],
        ata_data['dataAssinatura'],
        ata_data['dataVigencia'],
        ata_data['fornecedor'],
        ata_data['createdAt'],
        ata_data['updatedAt']
    ))
    
    ata_id = cursor.lastrowid
    
    for telefone in ata_data.get('telefonesFornecedor', []):
        cursor.execute('INSERT INTO telefones (ata_id, telefone) VALUES (?, ?)', (ata_id, telefone))
        
    for email in ata_data.get('emailsFornecedor', []):
        cursor.execute('INSERT INTO emails (ata_id, email) VALUES (?, ?)', (ata_id, email))
        
    for item in ata_data.get('items', []):
        cursor.execute('INSERT INTO itens (ata_id, descricao, quantidade, valor) VALUES (?, ?, ?, ?)',
                       (ata_id, item['descricao'], item['quantidade'], item['valor']))
                       
    conn.commit()
    conn.close()
    return ata_id

def get_all_atas() -> List[Dict[str, Any]]:
    """Retorna todas as atas com seus dados relacionados."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM atas ORDER BY dataVigencia DESC')
    atas = cursor.fetchall()
    
    result = []
    for ata in atas:
        ata_dict = dict(ata)
        
        cursor.execute('SELECT telefone FROM telefones WHERE ata_id = ?', (ata['id'],))
        ata_dict['telefonesFornecedor'] = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT email FROM emails WHERE ata_id = ?', (ata['id'],))
        ata_dict['emailsFornecedor'] = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT descricao, quantidade, valor FROM itens WHERE ata_id = ?', (ata['id'],))
        ata_dict['items'] = [dict(row) for row in cursor.fetchall()]
        
        result.append(ata_dict)
        
    conn.close()
    return result

def update_ata(ata_id: int, ata_data: Dict[str, Any]):
    """Atualiza uma ata existente no banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE atas
        SET numeroAta = ?, documentoSei = ?, objeto = ?, dataAssinatura = ?, dataVigencia = ?, fornecedor = ?, updatedAt = ?
        WHERE id = ?
    ''', (
        ata_data['numeroAta'],
        ata_data.get('documentoSei', ''),
        ata_data['objeto'],
        ata_data['dataAssinatura'],
        ata_data['dataVigencia'],
        ata_data['fornecedor'],
        ata_data['updatedAt'],
        ata_id
    ))
    
    # Deleta e reinsere telefones, emails e itens para simplificar a atualização
    cursor.execute('DELETE FROM telefones WHERE ata_id = ?', (ata_id,))
    for telefone in ata_data.get('telefonesFornecedor', []):
        cursor.execute('INSERT INTO telefones (ata_id, telefone) VALUES (?, ?)', (ata_id, telefone))
        
    cursor.execute('DELETE FROM emails WHERE ata_id = ?', (ata_id,))
    for email in ata_data.get('emailsFornecedor', []):
        cursor.execute('INSERT INTO emails (ata_id, email) VALUES (?, ?)', (ata_id, email))
        
    cursor.execute('DELETE FROM itens WHERE ata_id = ?', (ata_id,))
    for item in ata_data.get('items', []):
        cursor.execute('INSERT INTO itens (ata_id, descricao, quantidade, valor) VALUES (?, ?, ?, ?)',
                       (ata_id, item['descricao'], item['quantidade'], item['valor']))
                       
    conn.commit()
    conn.close()

def delete_ata(ata_id: int):
    """Deleta uma ata do banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM atas WHERE id = ?', (ata_id,))
    conn.commit()
    conn.close()