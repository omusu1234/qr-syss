"""
Database synchronization module for syncing data across multiple MySQL servers
"""
import pymysql
from flask import current_app
from models import db, Attendance, LectureSession, User, Lecturer, Unit
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class DatabaseSync:
    """Handle synchronization across multiple database servers"""
    
    def __init__(self):
        self.servers = []
        self._init_servers()
    
    def _init_servers(self):
        """Initialize connections to all database servers"""
        from flask import has_app_context
        if not has_app_context():
            logger.warning("DatabaseSync initialized outside app context")
            return
            
        try:
            config = current_app.config
            # Skip if no servers configured (sync disabled)
            if not config.get('DATABASE_SERVERS'):
                logger.info("Database sync disabled - no servers configured")
                return
                
            for server_config in config['DATABASE_SERVERS']:
                try:
                    conn = pymysql.connect(
                        host=server_config['host'],
                        user=server_config['user'],
                        password=server_config['password'],
                        database=server_config['database'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        autocommit=False
                    )
                    self.servers.append({
                        'config': server_config,
                        'connection': conn
                    })
                    logger.info(f"Connected to database server {server_config['host']}")
                except Exception as e:
                    error_msg = f"Failed to connect to database server {server_config['host']}: {str(e)}"
                    if has_app_context():
                        current_app.logger.error(error_msg)
                    else:
                        logger.error(error_msg)
        except Exception as e:
            error_msg = f"Error initializing database servers: {str(e)}"
            if has_app_context():
                current_app.logger.error(error_msg)
            else:
                logger.error(error_msg)
    
    def _get_connection(self, server_config):
        """Get or create a connection to a database server"""
        from flask import has_app_context
        try:
            return pymysql.connect(
                host=server_config['host'],
                user=server_config['user'],
                password=server_config['password'],
                database=server_config['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
        except Exception as e:
            error_msg = f"Failed to connect to {server_config['host']}: {str(e)}"
            if has_app_context():
                current_app.logger.error(error_msg)
            else:
                logger.error(error_msg)
            return None
    
    def sync_attendance(self, attendance_data):
        """
        Sync attendance record to all database servers
        attendance_data: dict with attendance record fields
        """
        from flask import has_app_context
        synced_servers = []
        
        # Skip if no servers configured
        if not has_app_context() or not current_app.config.get('DATABASE_SERVERS'):
            return synced_servers
        
        # Reinitialize servers if empty (in case of first call or reset)
        if not self.servers:
            self._init_servers()
        
        for server in self.servers:
            try:
                conn = server['connection']
                # Check if connection is still alive
                try:
                    conn.ping(reconnect=False)
                except:
                    # Connection is dead, reconnect
                    server['connection'] = self._get_connection(server['config'])
                    conn = server['connection']
                    if conn is None:
                        continue
                
                with conn.cursor() as cursor:
                    # Insert attendance record
                    sql = """
                        INSERT INTO attendances 
                        (session_id, admission_no, student_name, submission_latitude, 
                         submission_longitude, submitted_at, ip_address)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        student_name=VALUES(student_name),
                        submission_latitude=VALUES(submission_latitude),
                        submission_longitude=VALUES(submission_longitude),
                        submitted_at=VALUES(submitted_at),
                        ip_address=VALUES(ip_address)
                    """
                    cursor.execute(sql, (
                        attendance_data['session_id'],
                        attendance_data['admission_no'],
                        attendance_data['student_name'],
                        attendance_data['submission_latitude'],
                        attendance_data['submission_longitude'],
                        attendance_data['submitted_at'],
                        attendance_data.get('ip_address')
                    ))
                    conn.commit()
                    synced_servers.append(server['config']['host'])
            except Exception as e:
                error_msg = f"Failed to sync attendance to {server['config']['host']}: {str(e)}"
                if has_app_context():
                    current_app.logger.error(error_msg)
                else:
                    logger.error(error_msg)
                # Try to reconnect for next time
                try:
                    server['connection'] = self._get_connection(server['config'])
                except:
                    pass
        
        return synced_servers
    
    def sync_session(self, session_data):
        """Sync lecture session to all database servers"""
        from flask import has_app_context
        synced_servers = []
        
        # Skip if no servers configured
        if not has_app_context() or not current_app.config.get('DATABASE_SERVERS'):
            return synced_servers
        
        # Reinitialize servers if empty (in case of first call or reset)
        if not self.servers:
            self._init_servers()
        
        for server in self.servers:
            try:
                conn = server['connection']
                # Check if connection is still alive
                try:
                    conn.ping(reconnect=False)
                except:
                    # Connection is dead, reconnect
                    server['connection'] = self._get_connection(server['config'])
                    conn = server['connection']
                    if conn is None:
                        continue
                
                with conn.cursor() as cursor:
                    sql = """
                        INSERT INTO lecture_sessions 
                        (id, unit_id, session_name, hall_name, qr_code_token, qr_code_data,
                         lecture_hall_latitude, lecture_hall_longitude, location_radius, created_at, 
                         expires_at, is_active)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        session_name=VALUES(session_name),
                        hall_name=VALUES(hall_name),
                        qr_code_data=VALUES(qr_code_data),
                        location_radius=VALUES(location_radius),
                        expires_at=VALUES(expires_at),
                        is_active=VALUES(is_active)
                    """
                    cursor.execute(sql, (
                        session_data['id'],
                        session_data['unit_id'],
                        session_data['session_name'],
                        session_data.get('hall_name'),
                        session_data['qr_code_token'],
                        session_data['qr_code_data'],
                        session_data['lecture_hall_latitude'],
                        session_data['lecture_hall_longitude'],
                        session_data.get('location_radius', 100),
                        session_data['created_at'],
                        session_data['expires_at'],
                        session_data['is_active']
                    ))
                    conn.commit()
                    synced_servers.append(server['config']['host'])
            except Exception as e:
                error_msg = f"Failed to sync session to {server['config']['host']}: {str(e)}"
                if has_app_context():
                    current_app.logger.error(error_msg)
                else:
                    logger.error(error_msg)
                # Try to reconnect for next time
                try:
                    server['connection'] = self._get_connection(server['config'])
                except:
                    pass
        
        return synced_servers
    
    def delete_session(self, session_id):
        """Delete a session from all database servers"""
        from flask import has_app_context
        synced_servers = []
        
        # Skip if no servers configured
        if not has_app_context() or not current_app.config.get('DATABASE_SERVERS'):
            return synced_servers
        
        # Reinitialize servers if empty (in case of first call or reset)
        if not self.servers:
            self._init_servers()
        
        for server in self.servers:
            try:
                conn = server['connection']
                # Check if connection is still alive
                try:
                    conn.ping(reconnect=False)
                except:
                    # Connection is dead, reconnect
                    server['connection'] = self._get_connection(server['config'])
                    conn = server['connection']
                    if conn is None:
                        continue
                
                with conn.cursor() as cursor:
                    # Delete the session (cascade will delete attendances)
                    sql = "DELETE FROM lecture_sessions WHERE id = %s"
                    cursor.execute(sql, (session_id,))
                    conn.commit()
                    synced_servers.append(server['config']['host'])
            except Exception as e:
                error_msg = f"Failed to delete session from {server['config']['host']}: {str(e)}"
                if has_app_context():
                    current_app.logger.error(error_msg)
                else:
                    logger.error(error_msg)
                # Try to reconnect for next time
                try:
                    server['connection'] = self._get_connection(server['config'])
                except:
                    pass
        
        return synced_servers
    
    def close_all(self):
        """Close all database connections"""
        for server in self.servers:
            try:
                server['connection'].close()
            except:
                pass

