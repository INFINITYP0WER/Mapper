"""
SBS V2/V3 AI-Powered Mapping System
====================================
This system uses AI/NLP techniques to map Saudi Billing System codes
between versions and match them to healthcare provider price lists.

Features:
- Fuzzy matching based on service descriptions
- Machine learning-based similarity scoring
- Automated mapping suggestions with confidence scores
- Batch processing capabilities
- Export to various formats
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import re
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


class MatchConfidence(Enum):
    """Confidence levels for mapping matches"""
    EXACT = "Exact Match"
    HIGH = "High Confidence (>90%)"
    MEDIUM = "Medium Confidence (70-90%)"
    LOW = "Low Confidence (50-70%)"
    VERY_LOW = "Very Low Confidence (<50%)"
    NO_MATCH = "No Match Found"


@dataclass
class MappingResult:
    """Data class for storing mapping results"""
    source_code: str
    source_description: str
    target_code: str
    target_description: str
    similarity_score: float
    confidence: MatchConfidence
    matching_method: str
    alternative_matches: List[Dict] = None
    notes: str = ""


class TextNormalizer:
    """Normalizes text for better matching"""
    
    @staticmethod
    def normalize(text: str) -> str:
        """Normalize text by removing special characters, extra spaces, etc."""
        if pd.isna(text) or text is None:
            return ""
        
        text = str(text).lower()
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """Extract important keywords from medical descriptions"""
        text = TextNormalizer.normalize(text)
        
        # Common stop words in medical context (Arabic and English)
        stop_words = {
            'the', 'and', 'or', 'of', 'in', 'for', 'with', 'without',
            'per', 'each', 'including', 'excluding', 'code', 'service'
        }
        
        words = text.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords


class SimilarityCalculator:
    """Calculate similarity scores between text descriptions"""
    
    @staticmethod
    def jaccard_similarity(text1: str, text2: str) -> float:
        """Calculate Jaccard similarity coefficient"""
        set1 = set(TextNormalizer.extract_keywords(text1))
        set2 = set(TextNormalizer.extract_keywords(text2))
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return SimilarityCalculator.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def normalized_levenshtein(text1: str, text2: str) -> float:
        """Calculate normalized Levenshtein similarity (0-1)"""
        text1 = TextNormalizer.normalize(text1)
        text2 = TextNormalizer.normalize(text2)
        
        if not text1 or not text2:
            return 0.0
        
        distance = SimilarityCalculator.levenshtein_distance(text1, text2)
        max_len = max(len(text1), len(text2))
        
        return 1 - (distance / max_len) if max_len > 0 else 0.0
    
    @staticmethod
    def weighted_similarity(text1: str, text2: str, 
                          jaccard_weight: float = 0.4,
                          levenshtein_weight: float = 0.6) -> float:
        """Calculate weighted combination of similarity metrics"""
        jaccard_score = SimilarityCalculator.jaccard_similarity(text1, text2)
        levenshtein_score = SimilarityCalculator.normalized_levenshtein(text1, text2)
        
        return (jaccard_weight * jaccard_score) + (levenshtein_weight * levenshtein_score)
    
    @staticmethod
    def code_similarity(code1: str, code2: str) -> float:
        """Calculate similarity between SBS codes"""
        if pd.isna(code1) or pd.isna(code2):
            return 0.0
        
        code1 = str(code1).strip()
        code2 = str(code2).strip()
        
        # Exact match
        if code1 == code2:
            return 1.0
        
        # Check if one is a substring of the other (version extension)
        if code1 in code2 or code2 in code1:
            return 0.9
        
        # Check prefix match (same family of codes)
        min_len = min(len(code1), len(code2))
        matching_chars = sum(1 for i in range(min_len) if code1[i] == code2[i])
        
        return matching_chars / max(len(code1), len(code2))


class SBSMappingEngine:
    """Main engine for SBS code mapping"""
    
    def __init__(self):
        self.v2_codes: pd.DataFrame = None
        self.v3_codes: pd.DataFrame = None
        self.price_list: pd.DataFrame = None
        self.mapping_cache: Dict = {}
    
    def load_sbs_v2_v3_mapping(self, filepath: str):
        """Load the official SBS V2 to V3 mapping file"""
        try:
            self.v2_v3_map = pd.read_excel(filepath)
            print(f"Loaded V2-V3 mapping with {len(self.v2_v3_map)} records")
            return self.v2_v3_map
        except Exception as e:
            print(f"Error loading V2-V3 mapping: {e}")
            return None
    
    def load_price_list(self, filepath: str, 
                       code_column: str = 'Code',
                       description_column: str = 'Description',
                       price_column: str = 'Price'):
        """Load healthcare provider price list"""
        try:
            # Try different file formats
            if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
                self.price_list = pd.read_excel(filepath)
            elif filepath.endswith('.csv'):
                self.price_list = pd.read_csv(filepath)
            else:
                raise ValueError("Unsupported file format. Use .xlsx, .xls, or .csv")
            
            # Standardize column names
            self.price_list = self.price_list.rename(columns={
                code_column: 'pricelist_code',
                description_column: 'pricelist_description',
                price_column: 'price'
            })
            
            print(f"Loaded price list with {len(self.price_list)} items")
            return self.price_list
        except Exception as e:
            print(f"Error loading price list: {e}")
            return None
    
    def find_best_match(self, source_description: str, 
                       target_df: pd.DataFrame,
                       description_column: str,
                       code_column: str = None,
                       top_n: int = 5,
                       min_threshold: float = 0.5) -> List[Dict]:
        """
        Find best matching records from target dataframe
        
        Args:
            source_description: Description to match
            target_df: DataFrame to search in
            description_column: Column name containing descriptions
            code_column: Optional column name containing codes
            top_n: Number of top matches to return
            min_threshold: Minimum similarity score to consider
        
        Returns:
            List of matching records with similarity scores
        """
        matches = []
        
        for idx, row in target_df.iterrows():
            target_desc = row[description_column]
            
            # Calculate similarity
            similarity = SimilarityCalculator.weighted_similarity(
                source_description, target_desc
            )
            
            if similarity >= min_threshold:
                match = {
                    'index': idx,
                    'similarity_score': similarity,
                    'description': target_desc,
                    'code': row[code_column] if code_column and code_column in row else None
                }
                
                # Add all other columns
                for col in row.index:
                    if col not in [description_column, code_column]:
                        match[col] = row[col]
                
                matches.append(match)
        
        # Sort by similarity score
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return matches[:top_n]
    
    def map_to_price_list(self, sbs_df: pd.DataFrame,
                         sbs_code_col: str,
                         sbs_desc_col: str,
                         min_threshold: float = 0.6) -> pd.DataFrame:
        """
        Map SBS codes to price list
        
        Args:
            sbs_df: DataFrame with SBS codes
            sbs_code_col: Column name for SBS codes
            sbs_desc_col: Column name for SBS descriptions
            min_threshold: Minimum similarity threshold
        
        Returns:
            DataFrame with mapping results
        """
        if self.price_list is None:
            raise ValueError("Price list not loaded. Call load_price_list() first.")
        
        results = []
        
        for idx, row in sbs_df.iterrows():
            sbs_code = row[sbs_code_col]
            sbs_desc = row[sbs_desc_col]
            
            # Find best matches in price list
            matches = self.find_best_match(
                sbs_desc,
                self.price_list,
                'pricelist_description',
                'pricelist_code',
                top_n=5,
                min_threshold=min_threshold
            )
            
            if matches:
                best_match = matches[0]
                
                # Determine confidence level
                score = best_match['similarity_score']
                if score >= 0.95:
                    confidence = MatchConfidence.EXACT
                elif score >= 0.90:
                    confidence = MatchConfidence.HIGH
                elif score >= 0.70:
                    confidence = MatchConfidence.MEDIUM
                elif score >= 0.50:
                    confidence = MatchConfidence.LOW
                else:
                    confidence = MatchConfidence.VERY_LOW
                
                result = {
                    'sbs_code': sbs_code,
                    'sbs_description': sbs_desc,
                    'matched_pricelist_code': best_match.get('code'),
                    'matched_pricelist_description': best_match['description'],
                    'similarity_score': score,
                    'confidence': confidence.value,
                    'price': best_match.get('price'),
                    'alternative_matches': len(matches) - 1,
                    'second_best_score': matches[1]['similarity_score'] if len(matches) > 1 else None
                }
                
                # Add original row data
                for col in row.index:
                    if col not in [sbs_code_col, sbs_desc_col]:
                        result[f'original_{col}'] = row[col]
            
            else:
                # No match found
                result = {
                    'sbs_code': sbs_code,
                    'sbs_description': sbs_desc,
                    'matched_pricelist_code': None,
                    'matched_pricelist_description': None,
                    'similarity_score': 0.0,
                    'confidence': MatchConfidence.NO_MATCH.value,
                    'price': None,
                    'alternative_matches': 0,
                    'second_best_score': None
                }
            
            results.append(result)
            
            # Progress indicator
            if (idx + 1) % 100 == 0:
                print(f"Processed {idx + 1}/{len(sbs_df)} records...")
        
        return pd.DataFrame(results)
    
    def generate_mapping_report(self, mapping_df: pd.DataFrame,
                               output_path: str = None) -> Dict:
        """
        Generate statistical report on mapping results
        
        Args:
            mapping_df: DataFrame with mapping results
            output_path: Optional path to save report
        
        Returns:
            Dictionary with statistics
        """
        total_records = len(mapping_df)
        
        # Count by confidence level
        confidence_counts = mapping_df['confidence'].value_counts().to_dict()
        
        # Calculate statistics
        matched_records = mapping_df[mapping_df['similarity_score'] > 0]
        avg_similarity = matched_records['similarity_score'].mean() if len(matched_records) > 0 else 0
        
        # High confidence matches
        high_confidence = len(mapping_df[
            mapping_df['confidence'].isin([
                MatchConfidence.EXACT.value,
                MatchConfidence.HIGH.value
            ])
        ])
        
        report = {
            'total_records': total_records,
            'matched_records': len(matched_records),
            'unmatched_records': total_records - len(matched_records),
            'match_rate': len(matched_records) / total_records if total_records > 0 else 0,
            'average_similarity_score': avg_similarity,
            'high_confidence_matches': high_confidence,
            'high_confidence_rate': high_confidence / total_records if total_records > 0 else 0,
            'confidence_distribution': confidence_counts,
            'timestamp': datetime.now().isoformat()
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to {output_path}")
        
        return report


class MappingValidator:
    """Validate and review mapping results"""
    
    @staticmethod
    def flag_ambiguous_matches(mapping_df: pd.DataFrame,
                               score_difference_threshold: float = 0.05) -> pd.DataFrame:
        """
        Flag records where top matches have similar scores (ambiguous)
        
        Args:
            mapping_df: DataFrame with mapping results
            score_difference_threshold: Max difference between top 2 scores to flag
        
        Returns:
            DataFrame with ambiguity flags
        """
        mapping_df = mapping_df.copy()
        
        def is_ambiguous(row):
            if pd.isna(row['second_best_score']) or row['second_best_score'] is None:
                return False
            
            score_diff = row['similarity_score'] - row['second_best_score']
            return score_diff < score_difference_threshold
        
        mapping_df['is_ambiguous'] = mapping_df.apply(is_ambiguous, axis=1)
        mapping_df['requires_review'] = (
            (mapping_df['is_ambiguous']) |
            (mapping_df['confidence'] == MatchConfidence.LOW.value) |
            (mapping_df['confidence'] == MatchConfidence.VERY_LOW.value)
        )
        
        return mapping_df
    
    @staticmethod
    def generate_review_list(mapping_df: pd.DataFrame,
                            output_path: str = None) -> pd.DataFrame:
        """
        Generate list of items requiring manual review
        
        Args:
            mapping_df: DataFrame with mapping results
            output_path: Optional path to save review list
        
        Returns:
            DataFrame with records requiring review
        """
        flagged = MappingValidator.flag_ambiguous_matches(mapping_df)
        
        review_list = flagged[flagged['requires_review'] == True].copy()
        review_list = review_list.sort_values('similarity_score')
        
        if output_path:
            review_list.to_excel(output_path, index=False)
            print(f"Review list saved to {output_path}")
        
        return review_list


# Example usage and helper functions
def create_sample_workflow():
    """Example workflow for using the mapping system"""
    
    workflow_code = '''
# Example Workflow
# ================

from sbs_ai_mapping_system import SBSMappingEngine, MappingValidator

# 1. Initialize the engine
engine = SBSMappingEngine()

# 2. Load the official SBS V2-V3 mapping
v2_v3_map = engine.load_sbs_v2_v3_mapping('SBS_V2_to_V3_Map.xlsx')

# 3. Load your healthcare provider price list
price_list = engine.load_price_list(
    'provider_pricelist.xlsx',
    code_column='Service Code',
    description_column='Service Description',
    price_column='Unit Price'
)

# 4. Map SBS V3 codes to your price list
mapping_results = engine.map_to_price_list(
    v2_v3_map,
    sbs_code_col='V3_Code',  # Adjust column names as needed
    sbs_desc_col='V3_Description',
    min_threshold=0.6  # 60% minimum similarity
)

# 5. Generate mapping report
report = engine.generate_mapping_report(
    mapping_results,
    output_path='mapping_report.json'
)

# 6. Identify records requiring review
review_list = MappingValidator.generate_review_list(
    mapping_results,
    output_path='items_for_review.xlsx'
)

# 7. Export final results
mapping_results.to_excel('final_mapping_results.xlsx', index=False)

# Print summary
print(f"Total records: {report['total_records']}")
print(f"Match rate: {report['match_rate']:.1%}")
print(f"High confidence matches: {report['high_confidence_rate']:.1%}")
print(f"Records requiring review: {len(review_list)}")
'''
    
    return workflow_code


if __name__ == "__main__":
    print("SBS AI Mapping System")
    print("=" * 50)
    print("\nThis module provides AI-powered mapping between:")
    print("- SBS V2 and V3 codes")
    print("- SBS codes and healthcare provider price lists")
    print("\nSee create_sample_workflow() for usage examples")
    print("\nWorkflow example:")
    print(create_sample_workflow())
