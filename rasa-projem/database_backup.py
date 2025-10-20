#!/usr/bin/env python3
"""
Database Backup Script
Runs weekly to backup MongoDB database
"""

import os
import sys
import logging
from datetime import datetime

# Add actions directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'actions'))

from actions.database.mongoclient import MongoDBClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main backup function"""
    logger.info("Starting database backup process")
    
    try:
        # Initialize MongoDB client
        mongo_client = MongoDBClient()
        
        # Create backup directory if it doesn't exist
        backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'backup_{timestamp}.json')
        
        logger.info(f"Creating backup at {backup_path}")
        mongo_client.backup_database(backup_path)
        
        # Clean up old backups (keep last 4 weeks)
        logger.info("Cleaning up old backups")
        import glob
        import time
        
        backup_files = glob.glob(os.path.join(backup_dir, 'backup_*.json'))
        current_time = time.time()
        
        for backup_file in backup_files:
            file_age_days = (current_time - os.path.getmtime(backup_file)) / 86400
            if file_age_days > 28:  # 4 weeks
                os.remove(backup_file)
                logger.info(f"Deleted old backup: {backup_file}")
        
        # Close MongoDB connection
        mongo_client.close()
        
        logger.info("Database backup completed successfully")
        
    except Exception as e:
        logger.error(f"Error in database backup: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
