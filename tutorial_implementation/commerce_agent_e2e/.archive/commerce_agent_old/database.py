"""
Database utilities for Commerce Agent.
Handles SQLite schema setup and connection management.
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

from .models import (
    UserPreferences,
    InteractionRecord,
    UserFavorite,
    EngagementProfile,
    Product,
)
from .config import DATABASE_URL


def get_db_connection() -> sqlite3.Connection:
    """Get SQLite database connection"""
    db_path = DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> None:
    """Initialize database schema"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # User preferences table
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id TEXT PRIMARY KEY,
            preferences_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Interaction history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS interaction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            query TEXT,
            result_count INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_preferences(user_id)
        )
    """)
    
    # User favorites table
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            product_id TEXT,
            product_name TEXT,
            url TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_preferences(user_id)
        )
    """)
    
    # Product cache table
    c.execute("""
        CREATE TABLE IF NOT EXISTS product_cache (
            cache_key TEXT PRIMARY KEY,
            results_json TEXT,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ttl_seconds INTEGER DEFAULT 3600
        )
    """)
    
    conn.commit()
    conn.close()


def get_user_preferences(user_id: str) -> Optional[UserPreferences]:
    """Retrieve user preferences from database"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "SELECT preferences_json FROM user_preferences WHERE user_id = ?",
            (user_id,)
        )
        row = c.fetchone()
        conn.close()
        
        if row:
            data = json.loads(row[0])
            return UserPreferences(**data)
        return None
    except Exception as e:
        raise Exception(f"Failed to get user preferences: {str(e)}")


def save_user_preferences(user_id: str, prefs: UserPreferences) -> None:
    """Save user preferences to database"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        prefs_json = prefs.model_dump_json()
        c.execute(
            """INSERT OR REPLACE INTO user_preferences (user_id, preferences_json, updated_at)
            VALUES (?, ?, ?)""",
            (user_id, prefs_json, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to save user preferences: {str(e)}")


def add_interaction(record: InteractionRecord) -> None:
    """Add interaction record to history"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            """INSERT INTO interaction_history 
            (user_id, session_id, query, result_count, timestamp)
            VALUES (?, ?, ?, ?, ?)""",
            (
                record.user_id,
                record.session_id,
                record.query,
                record.result_count,
                record.timestamp.isoformat()
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to add interaction: {str(e)}")


def get_user_history(user_id: str, limit: int = 10) -> List[InteractionRecord]:
    """Get user interaction history"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            """SELECT user_id, session_id, query, result_count, timestamp
            FROM interaction_history WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT ?""",
            (user_id, limit)
        )
        rows = c.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            records.append(InteractionRecord(
                user_id=row[0],
                session_id=row[1],
                query=row[2],
                result_count=row[3],
                timestamp=datetime.fromisoformat(row[4])
            ))
        return records
    except Exception as e:
        raise Exception(f"Failed to get user history: {str(e)}")


def add_favorite(favorite: UserFavorite) -> None:
    """Add product to user favorites"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            """INSERT INTO user_favorites 
            (user_id, product_id, product_name, url, added_at)
            VALUES (?, ?, ?, ?, ?)""",
            (
                favorite.user_id,
                favorite.product_id,
                favorite.product_name,
                favorite.url,
                favorite.added_at.isoformat()
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to add favorite: {str(e)}")


def get_user_favorites(user_id: str) -> List[UserFavorite]:
    """Get user's favorite products"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            """SELECT user_id, product_id, product_name, url, added_at
            FROM user_favorites WHERE user_id = ?
            ORDER BY added_at DESC""",
            (user_id,)
        )
        rows = c.fetchall()
        conn.close()
        
        favorites = []
        for row in rows:
            favorites.append(UserFavorite(
                user_id=row[0],
                product_id=row[1],
                product_name=row[2],
                url=row[3],
                added_at=datetime.fromisoformat(row[4])
            ))
        return favorites
    except Exception as e:
        raise Exception(f"Failed to get favorites: {str(e)}")


def cache_search_results(cache_key: str, results: List[Product]) -> None:
    """Cache search results"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        results_json = json.dumps([r.model_dump() for r in results])
        c.execute(
            """INSERT OR REPLACE INTO product_cache 
            (cache_key, results_json, cached_at, ttl_seconds)
            VALUES (?, ?, ?, ?)""",
            (cache_key, results_json, datetime.utcnow().isoformat(), 3600)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to cache results: {str(e)}")


def get_cached_results(cache_key: str) -> Optional[List[Product]]:
    """Get cached search results if not expired"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            """SELECT results_json, cached_at, ttl_seconds FROM product_cache
            WHERE cache_key = ?""",
            (cache_key,)
        )
        row = c.fetchone()
        conn.close()
        
        if row:
            cached_at = datetime.fromisoformat(row[1])
            ttl = row[2]
            elapsed = (datetime.utcnow() - cached_at).total_seconds()
            
            if elapsed < ttl:
                data = json.loads(row[0])
                return [Product(**item) for item in data]
        
        return None
    except Exception as e:
        raise Exception(f"Failed to get cached results: {str(e)}")


def get_engagement_profile(user_id: str) -> EngagementProfile:
    """Calculate user engagement profile"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Total interactions
        c.execute(
            "SELECT COUNT(*) FROM interaction_history WHERE user_id = ?",
            (user_id,)
        )
        total_interactions = c.fetchone()[0]
        
        # Last interaction
        c.execute(
            """SELECT timestamp FROM interaction_history 
            WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1""",
            (user_id,)
        )
        last_row = c.fetchone()
        last_interaction = datetime.fromisoformat(last_row[0]) if last_row else None
        
        # Favorite categories (from preferences)
        c.execute(
            "SELECT preferences_json FROM user_preferences WHERE user_id = ?",
            (user_id,)
        )
        pref_row = c.fetchone()
        favorite_categories = []
        preferred_brands = []
        
        if pref_row:
            prefs = json.loads(pref_row[0])
            favorite_categories = prefs.get("sports", [])
            preferred_brands = prefs.get("brands", [])
        
        conn.close()
        
        return EngagementProfile(
            total_interactions=total_interactions,
            favorite_categories=favorite_categories,
            preferred_brands=preferred_brands,
            last_interaction=last_interaction,
            avg_session_duration=0.0
        )
    except Exception as e:
        raise Exception(f"Failed to get engagement profile: {str(e)}")
