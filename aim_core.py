"""
Adaptive Integration Middleware (AIM) Core Module

This module provides the foundational classes for managing AI integration pathways.
"""

from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MiddlewareManager:
    """Manages the registration and routing of AI modules."""
    
    def __init__(self):
        self.modules: Dict[str, Dict] = {}
        self.analytics: IntegrationAnalyzer = IntegrationAnalyzer()
        
    def register_module(self, module_id: str, metadata: Dict) -> bool:
        """
        Registers an AI module with AIM.
        
        Args:
            module_id: Unique identifier for the module.
            metadata: Dictionary containing module capabilities and requirements.
            
        Returns:
            True if registration is successful, False otherwise.
        """
        try:
            self.modules[module_id] = metadata
            logger.info(f"Module {module_id} registered successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to register module {module_id}: {str(e)}")
            return False
    
    def discover_module(self, query: Dict) -> List[str]:
        """
        Discovers modules that match the given capabilities.
        
        Args:
            query: Dictionary specifying required capabilities.
            
        Returns:
            List of module IDs matching the query.
        """
        try:
            matched = []
            for module_id, metadata in self.modules.items():
                if all(q in metadata for q in query):
                    matched.append(module_id)
            return matched
        except Exception as e:
            logger.error(f"Discovery failed: {str(e)}")
            return []
    
    def route_request(self, source: str, target: str) -> bool:
        """
        Routes a request from one module to another.
        
        Args:
            source: Source module ID.
            target: Target module ID.
            
        Returns:
            True if routing is successful, False otherwise.
        """
        try:
            # Record the interaction for learning
            self.analytics.log_interaction(source, target)
            return True
        except Exception as e:
            logger.error(f"Routing failed between {source} and {target}: {str(e)}")
            return False

class ModuleRegistry:
    """Handles module registration with AIM."""
    
    def __init__(self):
        self.aim = MiddlewareManager()
        
    def register(self, module_class):
        """
        Decorator to register AI modules with AIM.
        
        Args:
            module_class: The class of the AI module.
            
        Returns:
            The registered module class.
        """
        try:
            module_id = getattr(module_class, 'module_id', None)
            if not module_id:
                raise ValueError("Module must have a 'module_id' attribute.")
                
            metadata = self._build_metadata(module_class)
            self.aim.register_module(module_id, metadata)
            logger.info(f"Registered module {module_id}")
            return module_class
        except Exception as e:
            logger.error(f"Failed to register module: {str(e)}")
            raise
    
    def _build_metadata(self, module_class) -> Dict:
        """
        Builds metadata for the registered module.
        
        Args:
            module_class: The class of the AI module.
            
        Returns:
            Dictionary containing module capabilities and requirements.
        """
        return {
            'capabilities': self._get_capabilities(module_class),
            'requirements': self._get_requirements(module_class),
            'version': getattr(module_class, '__version__', '1.0'),
        }
    
    def _get_capabilities(self, module_class) -> List[str]:
        """Extracts capabilities from the module."""
        return getattr(module_class, 'capabilities', [])
    
    def _get_requirements(self, module_class) -> List[str]:
        """Extracts requirements for the module."""
        return getattr(module_class, 'requirements', [])

class IntegrationAnalyzer:
    """Analyzes and optimizes integration pathways."""
    
    def __init__(self):
        self.interactions = []
        
    def log_interaction(self, source: str, target: str, metrics: Optional[Dict] = None) -> None:
        """
        Logs an interaction between modules.
        
        Args:
            source: Source module ID.
            target: Target module ID.
            metrics: Dictionary containing interaction metrics (optional).
        """
        try:
            interaction = {
                'source': source,
                'target': target,
                'timestamp': self._get_current_time(),
                'metrics': metrics or {},
            }
            self.interactions.append(interaction)
            logger.info(f"Interaction logged between {source} and {target}")
        except Exception as e:
            logger.error(f"Failed to log interaction: {str(e)}")
    
    def _get_current_time(self) -> float:
        """Returns the current timestamp."""
        import time
        return time.time()
    
    def optimize_pathways(self) -> None:
        """
        Optimizes integration pathways based on logged interactions.
        
        Uses historical data to determine optimal connections.
        """
        try:
            #