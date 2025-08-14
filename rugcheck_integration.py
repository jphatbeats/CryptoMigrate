#!/usr/bin/env python3
"""
Rugcheck.xyz Integration for Token Security Analysis
Provides comprehensive token security analysis including rug pull detection,
liquidity analysis, contract verification, and risk assessment.
"""

import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class RugCheckAPI:
    """
    Python wrapper for Rugcheck.xyz API
    Provides token security analysis and rug pull detection
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.rugcheck.xyz"
        self.api_key = api_key
        self.session = requests.Session()
        
        # Set headers
        headers = {
            'User-Agent': 'Crypto-Trading-Intelligence-Platform/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
            
        self.session.headers.update(headers)
    
    def check_token(self, token_address: str, chain: str = "solana") -> Dict:
        """
        Perform comprehensive token security analysis
        
        Args:
            token_address (str): Token contract address
            chain (str): Blockchain network (solana, ethereum, bsc)
            
        Returns:
            Dict: Token security analysis results
        """
        try:
            endpoint = f"/v1/tokens/{chain}/{token_address}"
            response = self.session.get(f"{self.base_url}{endpoint}")
            
            if response.status_code == 200:
                return self._process_token_analysis(response.json())
            elif response.status_code == 404:
                return {"error": "Token not found", "status": "not_found"}
            else:
                logger.error(f"RugCheck API error: {response.status_code}")
                return {"error": f"API error: {response.status_code}", "status": "error"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error accessing RugCheck: {e}")
            return {"error": f"Network error: {str(e)}", "status": "network_error"}
    
    def bulk_check_tokens(self, token_addresses: List[str], chain: str = "solana") -> Dict[str, Dict]:
        """
        Check multiple tokens in batch
        
        Args:
            token_addresses (List[str]): List of token contract addresses
            chain (str): Blockchain network
            
        Returns:
            Dict[str, Dict]: Dictionary of token addresses and their analysis results
        """
        results = {}
        
        for address in token_addresses:
            try:
                result = self.check_token(address, chain)
                results[address] = result
                
                # Add small delay to respect rate limits
                import time
                time.sleep(0.1)
                
            except Exception as e:
                results[address] = {
                    "error": f"Analysis failed: {str(e)}", 
                    "status": "failed"
                }
        
        return results
    
    def get_trending_tokens(self, chain: str = "solana", limit: int = 50) -> Dict:
        """
        Get trending tokens with security scores
        
        Args:
            chain (str): Blockchain network
            limit (int): Number of tokens to retrieve
            
        Returns:
            Dict: Trending tokens with security analysis
        """
        try:
            endpoint = f"/v1/trending/{chain}"
            params = {"limit": limit}
            
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error fetching trending tokens: {response.status_code}")
                return {"error": f"API error: {response.status_code}", "tokens": []}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching trending tokens: {e}")
            return {"error": f"Network error: {str(e)}", "tokens": []}
    
    def _process_token_analysis(self, raw_data: Dict) -> Dict:
        """
        Process and enhance raw RugCheck API response
        
        Args:
            raw_data (Dict): Raw API response
            
        Returns:
            Dict: Processed token analysis with enhanced risk assessment
        """
        try:
            # Extract key security metrics
            security_score = raw_data.get('score', 0)
            risks = raw_data.get('risks', [])
            liquidity = raw_data.get('liquidity', {})
            
            # Categorize risk level
            risk_level = self._categorize_risk(security_score, risks)
            
            # Generate trading recommendation
            recommendation = self._generate_recommendation(security_score, risks, liquidity)
            
            processed_data = {
                "token_address": raw_data.get('address', ''),
                "symbol": raw_data.get('symbol', ''),
                "name": raw_data.get('name', ''),
                "security_score": security_score,
                "risk_level": risk_level,
                "recommendation": recommendation,
                "risks": risks,
                "liquidity_analysis": liquidity,
                "contract_verified": raw_data.get('verified', False),
                "holder_distribution": raw_data.get('holders', {}),
                "trading_analysis": {
                    "volume_24h": raw_data.get('volume_24h', 0),
                    "price_change_24h": raw_data.get('price_change_24h', 0),
                    "market_cap": raw_data.get('market_cap', 0)
                },
                "timestamp": datetime.utcnow().isoformat(),
                "status": "success"
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing token analysis: {e}")
            return {
                "error": f"Processing error: {str(e)}",
                "raw_data": raw_data,
                "status": "processing_error"
            }
    
    def _categorize_risk(self, score: float, risks: List) -> str:
        """
        Categorize risk level based on security score and identified risks
        
        Args:
            score (float): Security score (0-100)
            risks (List): List of identified risks
            
        Returns:
            str: Risk category (SAFE, LOW, MEDIUM, HIGH, CRITICAL)
        """
        critical_risks = ['rugpull', 'honeypot', 'scam', 'fake_token']
        
        # Check for critical risks first
        if any(risk.get('type', '').lower() in critical_risks for risk in risks):
            return "CRITICAL"
        
        # Score-based categorization
        if score >= 80:
            return "SAFE"
        elif score >= 60:
            return "LOW"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _generate_recommendation(self, score: float, risks: List, liquidity: Dict) -> str:
        """
        Generate trading recommendation based on analysis
        
        Args:
            score (float): Security score
            risks (List): Identified risks
            liquidity (Dict): Liquidity analysis
            
        Returns:
            str: Trading recommendation
        """
        liquidity_score = liquidity.get('score', 0)
        
        if score >= 80 and liquidity_score >= 70:
            return "SAFE_TO_TRADE"
        elif score >= 60 and liquidity_score >= 50:
            return "MODERATE_RISK"
        elif score >= 40:
            return "HIGH_RISK"
        else:
            return "DO_NOT_TRADE"

class RugCheckAnalyzer:
    """
    Enhanced analyzer for integrating RugCheck with trading intelligence
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.rugcheck_api = RugCheckAPI(api_key)
        
    async def analyze_portfolio_security(self, token_addresses: List[str]) -> Dict:
        """
        Analyze security of entire portfolio
        
        Args:
            token_addresses (List[str]): List of token addresses in portfolio
            
        Returns:
            Dict: Portfolio security analysis
        """
        results = self.rugcheck_api.bulk_check_tokens(token_addresses)
        
        # Calculate portfolio security metrics
        total_tokens = len(results)
        safe_tokens = sum(1 for r in results.values() if r.get('risk_level') == 'SAFE')
        critical_risk = sum(1 for r in results.values() if r.get('risk_level') == 'CRITICAL')
        
        portfolio_score = (safe_tokens / total_tokens) * 100 if total_tokens > 0 else 0
        
        return {
            "portfolio_security_score": portfolio_score,
            "total_tokens_analyzed": total_tokens,
            "safe_tokens": safe_tokens,
            "critical_risk_tokens": critical_risk,
            "detailed_analysis": results,
            "recommendations": self._generate_portfolio_recommendations(results),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_portfolio_recommendations(self, analysis_results: Dict) -> List[str]:
        """
        Generate portfolio-level recommendations
        
        Args:
            analysis_results (Dict): Token analysis results
            
        Returns:
            List[str]: Portfolio recommendations
        """
        recommendations = []
        
        critical_tokens = [
            addr for addr, data in analysis_results.items() 
            if data.get('risk_level') == 'CRITICAL'
        ]
        
        if critical_tokens:
            recommendations.append(f"🚨 URGENT: Remove {len(critical_tokens)} critical risk tokens immediately")
        
        high_risk_tokens = [
            addr for addr, data in analysis_results.items() 
            if data.get('risk_level') == 'HIGH'
        ]
        
        if high_risk_tokens:
            recommendations.append(f"⚠️ Monitor {len(high_risk_tokens)} high-risk tokens closely")
        
        safe_percentage = len([
            r for r in analysis_results.values() 
            if r.get('risk_level') == 'SAFE'
        ]) / len(analysis_results) * 100
        
        if safe_percentage < 50:
            recommendations.append("📊 Consider rebalancing portfolio towards safer assets")
        
        return recommendations

# Utility functions for integration with main trading platform
def create_rugcheck_analyzer(api_key: Optional[str] = None) -> RugCheckAnalyzer:
    """
    Factory function to create RugCheck analyzer instance
    
    Args:
        api_key (Optional[str]): RugCheck API key
        
    Returns:
        RugCheckAnalyzer: Configured analyzer instance
    """
    return RugCheckAnalyzer(api_key)

def quick_token_check(token_address: str, chain: str = "solana") -> Dict:
    """
    Quick utility function for single token security check
    
    Args:
        token_address (str): Token contract address
        chain (str): Blockchain network
        
    Returns:
        Dict: Token security analysis
    """
    analyzer = RugCheckAnalyzer()
    return analyzer.rugcheck_api.check_token(token_address, chain)

if __name__ == "__main__":
    # Example usage
    analyzer = RugCheckAnalyzer()
    
    # Test with a known token (replace with actual token address)
    example_token = "So11111111111111111111111111111111111111112"  # Wrapped SOL
    result = analyzer.rugcheck_api.check_token(example_token, "solana")
    
    print("RugCheck Integration Test:")
    print(json.dumps(result, indent=2))