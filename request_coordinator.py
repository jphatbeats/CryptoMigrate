#!/usr/bin/env python3
"""
Request Coordination System for TAAPI.io
Prevents ChatGPT vs Discord bot API collisions
"""

import time
import threading
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json
import os

logger = logging.getLogger(__name__)

class RequestCoordinator:
    """Smart coordination system to prevent API collisions"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.active_requests = {}  # Track active requests
        self.request_queue = []    # Queue for pending requests
        self.chatgpt_priority_until = 0  # When ChatGPT has priority
        self.scan_paused_until = 0  # When scans are paused
        self.stats = {
            'chatgpt_requests': 0,
            'discord_requests': 0,
            'collisions_prevented': 0,
            'queue_delays': 0
        }
        
        # State persistence file
        self.state_file = "/tmp/taapi_coordinator_state.json"
        self.load_state()
    
    def request_access(self, requester_type: str, request_id: str, estimated_duration: int = 10) -> Dict[str, Any]:
        """
        Request access to TAAPI API
        
        Args:
            requester_type: 'chatgpt', 'discord_bot', 'manual'
            request_id: Unique identifier for this request
            estimated_duration: How long this request might take (seconds)
            
        Returns:
            {'granted': bool, 'wait_time': int, 'queue_position': int}
        """
        with self.lock:
            current_time = time.time()
            
            # Check if ChatGPT has priority and we're not ChatGPT
            if requester_type != 'chatgpt' and current_time < self.chatgpt_priority_until:
                wait_time = int(self.chatgpt_priority_until - current_time)
                logger.info(f"🤖 {requester_type} request blocked - ChatGPT has priority for {wait_time}s")
                return {
                    'granted': False, 
                    'wait_time': wait_time,
                    'reason': 'chatgpt_priority',
                    'queue_position': len(self.request_queue) + 1
                }
            
            # Check if scans are paused
            if requester_type == 'discord_bot' and current_time < self.scan_paused_until:
                wait_time = int(self.scan_paused_until - current_time)
                logger.info(f"⏸️ Discord bot scan paused for {wait_time}s")
                return {
                    'granted': False,
                    'wait_time': wait_time, 
                    'reason': 'scan_paused',
                    'queue_position': len(self.request_queue) + 1
                }
            
            # Check if there are active requests (maintain 1 req/3 sec limit)
            if self.active_requests:
                latest_request = max(self.active_requests.values(), key=lambda x: x['start_time'])
                time_since_latest = current_time - latest_request['start_time']
                
                if time_since_latest < 3.0:  # 3-second minimum gap
                    wait_time = int(3.0 - time_since_latest + 1)  # +1 second buffer
                    logger.info(f"⏳ Rate limit protection - {requester_type} must wait {wait_time}s")
                    return {
                        'granted': False,
                        'wait_time': wait_time,
                        'reason': 'rate_limit',
                        'queue_position': len(self.request_queue) + 1
                    }
            
            # Grant access
            self.active_requests[request_id] = {
                'requester_type': requester_type,
                'start_time': current_time,
                'estimated_end': current_time + estimated_duration
            }
            
            # Set ChatGPT priority if it's a ChatGPT request
            if requester_type == 'chatgpt':
                self.chatgpt_priority_until = current_time + estimated_duration + 5  # +5s buffer
                self.stats['chatgpt_requests'] += 1
                logger.info(f"🤖 ChatGPT granted priority for {estimated_duration + 5}s")
            else:
                self.stats['discord_requests'] += 1
            
            self.save_state()
            
            return {
                'granted': True,
                'wait_time': 0,
                'request_id': request_id,
                'priority_until': self.chatgpt_priority_until if requester_type == 'chatgpt' else 0
            }
    
    def release_access(self, request_id: str):
        """Release access when request is complete"""
        with self.lock:
            if request_id in self.active_requests:
                requester_type = self.active_requests[request_id]['requester_type']
                del self.active_requests[request_id]
                logger.info(f"✅ {requester_type} request {request_id} completed")
                self.save_state()
    
    def pause_scans(self, duration: int):
        """Pause Discord bot scans for specified duration"""
        with self.lock:
            self.scan_paused_until = time.time() + duration
            logger.info(f"⏸️ All Discord bot scans paused for {duration}s")
            self.save_state()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current coordinator status"""
        with self.lock:
            current_time = time.time()
            return {
                'active_requests': len(self.active_requests),
                'chatgpt_priority_active': current_time < self.chatgpt_priority_until,
                'chatgpt_priority_remaining': max(0, int(self.chatgpt_priority_until - current_time)),
                'scans_paused': current_time < self.scan_paused_until,
                'scan_pause_remaining': max(0, int(self.scan_paused_until - current_time)),
                'queue_length': len(self.request_queue),
                'stats': self.stats.copy(),
                'last_activity': datetime.now().isoformat()
            }
    
    def save_state(self):
        """Save coordinator state to file"""
        try:
            state = {
                'chatgpt_priority_until': self.chatgpt_priority_until,
                'scan_paused_until': self.scan_paused_until,
                'stats': self.stats,
                'timestamp': time.time()
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            logger.warning(f"Failed to save coordinator state: {e}")
    
    def load_state(self):
        """Load coordinator state from file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                
                # Only restore if state is recent (within 1 hour)
                if time.time() - state.get('timestamp', 0) < 3600:
                    self.chatgpt_priority_until = state.get('chatgpt_priority_until', 0)
                    self.scan_paused_until = state.get('scan_paused_until', 0)
                    self.stats = state.get('stats', self.stats)
                    logger.info("📋 Coordinator state restored from file")
        except Exception as e:
            logger.warning(f"Failed to load coordinator state: {e}")

# Global coordinator instance
coordinator = RequestCoordinator()