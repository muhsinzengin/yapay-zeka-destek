#!/usr/bin/env python3
"""
Automated Training Script
Runs nightly to export conversations to NLU and train the model
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
    """Main automated training function"""
    logger.info("Starting automated training process")
    
    try:
        # Initialize MongoDB client
        mongo_client = MongoDBClient()
        
        # Export conversations to NLU format
        nlu_path = os.path.join(os.path.dirname(__file__), 'data', 'nlu.yml')
        logger.info(f"Exporting conversations to {nlu_path}")
        mongo_client.export_conversations_to_nlu(nlu_path)
        
        # Train the model
        logger.info("Starting model training")
        import subprocess
        result = subprocess.run([
            'rasa', 'train',
            '--domain', 'domain.yml',
            '--data', 'data',
            '--config', 'config.yml',
            '--out', 'models'
        ], cwd=os.path.dirname(__file__), capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Model training completed successfully")
        else:
            logger.error(f"Model training failed: {result.stderr}")
        
        # Cleanup old logs (30 days)
        logger.info("Cleaning up old logs")
        mongo_client.cleanup_old_logs(days=30)
        
        # Close MongoDB connection
        mongo_client.close()
        
        logger.info("Automated training process completed")
        
    except Exception as e:
        logger.error(f"Error in automated training: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
