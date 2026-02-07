#!/usr/bin/env python3
"""
SBS V2/V3 Mapping System - Command Line Interface
=================================================

Simple command-line tool for mapping SBS codes to price lists.

Usage:
    python sbs_mapping_cli.py --help
    python sbs_mapping_cli.py --v2v3-file mapping.xlsx --pricelist prices.xlsx
"""

import argparse
import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

try:
    from sbs_ai_mapping_system import (
        SBSMappingEngine, 
        MappingValidator,
        MatchConfidence
    )
except ImportError:
    print("ERROR: Could not import sbs_ai_mapping_system.py")
    print("Please ensure sbs_ai_mapping_system.py is in the same directory")
    sys.exit(1)


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════╗
║   SBS V2/V3 AI-Powered Mapping System             ║
║   Healthcare Provider Price List Integration      ║
╚═══════════════════════════════════════════════════╝
    """
    print(banner)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Map SBS billing codes to healthcare provider price lists',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic usage:
    python sbs_mapping_cli.py \\
        --v2v3-file SBS_V2_to_V3_Map.xlsx \\
        --pricelist my_pricelist.xlsx

  With custom column names:
    python sbs_mapping_cli.py \\
        --v2v3-file SBS_V2_to_V3_Map.xlsx \\
        --pricelist my_pricelist.xlsx \\
        --code-col "Service Code" \\
        --desc-col "Service Description" \\
        --price-col "Unit Price"

  Adjust similarity threshold:
    python sbs_mapping_cli.py \\
        --v2v3-file SBS_V2_to_V3_Map.xlsx \\
        --pricelist my_pricelist.xlsx \\
        --threshold 0.70

  Custom output directory:
    python sbs_mapping_cli.py \\
        --v2v3-file SBS_V2_to_V3_Map.xlsx \\
        --pricelist my_pricelist.xlsx \\
        --output-dir ./mapping_results
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--v2v3-file',
        required=True,
        help='Path to SBS V2-V3 mapping file (Excel)'
    )
    
    parser.add_argument(
        '--pricelist',
        required=True,
        help='Path to healthcare provider price list (Excel or CSV)'
    )
    
    # Price list column configuration
    parser.add_argument(
        '--code-col',
        default='Code',
        help='Column name for service codes in price list (default: Code)'
    )
    
    parser.add_argument(
        '--desc-col',
        default='Description',
        help='Column name for descriptions in price list (default: Description)'
    )
    
    parser.add_argument(
        '--price-col',
        default='Price',
        help='Column name for prices in price list (default: Price)'
    )
    
    # SBS mapping column configuration
    parser.add_argument(
        '--sbs-code-col',
        default='V3_Code',
        help='Column name for SBS codes (default: V3_Code)'
    )
    
    parser.add_argument(
        '--sbs-desc-col',
        default='V3_Description',
        help='Column name for SBS descriptions (default: V3_Description)'
    )
    
    # Matching parameters
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.60,
        help='Minimum similarity threshold 0-1 (default: 0.60)'
    )
    
    # Output configuration
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory for results (default: current directory)'
    )
    
    parser.add_argument(
        '--output-prefix',
        default='',
        help='Prefix for output filenames (default: none)'
    )
    
    # Options
    parser.add_argument(
        '--no-review-list',
        action='store_true',
        help='Skip generating review list'
    )
    
    parser.add_argument(
        '--no-visualizations',
        action='store_true',
        help='Skip generating visualization charts'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress messages'
    )
    
    return parser.parse_args()


def validate_files(args):
    """Validate that input files exist"""
    errors = []
    
    if not os.path.exists(args.v2v3_file):
        errors.append(f"V2-V3 mapping file not found: {args.v2v3_file}")
    
    if not os.path.exists(args.pricelist):
        errors.append(f"Price list file not found: {args.pricelist}")
    
    if errors:
        print("\nERROR: Input file validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


def create_output_directory(output_dir):
    """Create output directory if it doesn't exist"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def generate_output_filename(output_dir, prefix, filename):
    """Generate output filename with optional prefix"""
    if prefix:
        filename = f"{prefix}_{filename}"
    return os.path.join(output_dir, filename)


def print_progress(message, quiet=False):
    """Print progress message unless quiet mode is enabled"""
    if not quiet:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def main():
    """Main execution function"""
    args = parse_arguments()
    
    if not args.quiet:
        print_banner()
    
    # Validate inputs
    print_progress("Validating input files...", args.quiet)
    validate_files(args)
    
    # Create output directory
    print_progress(f"Creating output directory: {args.output_dir}", args.quiet)
    create_output_directory(args.output_dir)
    
    # Initialize engine
    print_progress("Initializing mapping engine...", args.quiet)
    engine = SBSMappingEngine()
    
    # Load SBS V2-V3 mapping
    print_progress(f"Loading SBS V2-V3 mapping from: {args.v2v3_file}", args.quiet)
    v2_v3_map = engine.load_sbs_v2_v3_mapping(args.v2v3_file)
    
    if v2_v3_map is None:
        print("ERROR: Failed to load V2-V3 mapping file")
        sys.exit(1)
    
    print_progress(f"  ✓ Loaded {len(v2_v3_map)} V2-V3 mappings", args.quiet)
    
    # Load price list
    print_progress(f"Loading price list from: {args.pricelist}", args.quiet)
    price_list = engine.load_price_list(
        args.pricelist,
        code_column=args.code_col,
        description_column=args.desc_col,
        price_column=args.price_col
    )
    
    if price_list is None:
        print("ERROR: Failed to load price list file")
        sys.exit(1)
    
    print_progress(f"  ✓ Loaded {len(price_list)} price list items", args.quiet)
    
    # Run mapping
    print_progress(f"Running mapping process (threshold: {args.threshold:.0%})...", args.quiet)
    print_progress("  This may take several minutes for large datasets...", args.quiet)
    
    mapping_results = engine.map_to_price_list(
        sbs_df=v2_v3_map,
        sbs_code_col=args.sbs_code_col,
        sbs_desc_col=args.sbs_desc_col,
        min_threshold=args.threshold
    )
    
    print_progress(f"  ✓ Mapping complete", args.quiet)
    
    # Generate report
    print_progress("Generating mapping report...", args.quiet)
    report_file = generate_output_filename(args.output_dir, args.output_prefix, 'mapping_report.json')
    report = engine.generate_mapping_report(mapping_results, report_file)
    
    # Print summary
    if not args.quiet:
        print("\n" + "="*60)
        print("MAPPING SUMMARY")
        print("="*60)
        print(f"Total Records:          {report['total_records']:,}")
        print(f"Matched Records:        {report['matched_records']:,}")
        print(f"Unmatched Records:      {report['unmatched_records']:,}")
        print(f"Match Rate:             {report['match_rate']:.1%}")
        print(f"Avg Similarity Score:   {report['average_similarity_score']:.2%}")
        print(f"High Confidence:        {report['high_confidence_matches']:,} ({report['high_confidence_rate']:.1%})")
        print("="*60 + "\n")
    
    # Export main results
    print_progress("Exporting mapping results...", args.quiet)
    main_output = generate_output_filename(args.output_dir, args.output_prefix, 'mapping_results.xlsx')
    mapping_results.to_excel(main_output, index=False)
    print_progress(f"  ✓ Saved to: {main_output}", args.quiet)
    
    # Export high confidence matches
    print_progress("Exporting high confidence matches...", args.quiet)
    high_confidence = mapping_results[
        mapping_results['confidence'].isin([
            MatchConfidence.EXACT.value,
            MatchConfidence.HIGH.value
        ])
    ]
    hc_output = generate_output_filename(args.output_dir, args.output_prefix, 'high_confidence_mappings.xlsx')
    high_confidence.to_excel(hc_output, index=False)
    print_progress(f"  ✓ Saved {len(high_confidence)} high confidence matches to: {hc_output}", args.quiet)
    
    # Generate review list
    if not args.no_review_list:
        print_progress("Generating review list...", args.quiet)
        review_output = generate_output_filename(args.output_dir, args.output_prefix, 'items_for_review.xlsx')
        review_list = MappingValidator.generate_review_list(mapping_results, review_output)
        print_progress(f"  ✓ Flagged {len(review_list)} items for review: {review_output}", args.quiet)
    
    # Generate visualizations
    if not args.no_visualizations:
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            print_progress("Generating visualization charts...", args.quiet)
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Confidence distribution
            confidence_data = mapping_results['confidence'].value_counts()
            axes[0, 0].bar(range(len(confidence_data)), confidence_data.values)
            axes[0, 0].set_xticks(range(len(confidence_data)))
            axes[0, 0].set_xticklabels(confidence_data.index, rotation=45, ha='right')
            axes[0, 0].set_title('Mapping Confidence Distribution')
            axes[0, 0].set_ylabel('Number of Records')
            
            # Similarity score distribution
            matched_only = mapping_results[mapping_results['similarity_score'] > 0]
            axes[0, 1].hist(matched_only['similarity_score'], bins=20, edgecolor='black')
            axes[0, 1].set_title('Similarity Score Distribution')
            axes[0, 1].set_xlabel('Similarity Score')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].axvline(x=0.9, color='r', linestyle='--', label='90% threshold')
            axes[0, 1].legend()
            
            # Match vs no match
            match_counts = [
                len(mapping_results[mapping_results['similarity_score'] > 0]),
                len(mapping_results[mapping_results['similarity_score'] == 0])
            ]
            axes[1, 0].pie(match_counts, labels=['Matched', 'No Match'], autopct='%1.1f%%', startangle=90)
            axes[1, 0].set_title('Overall Match Rate')
            
            # Alternative matches
            alt_match_dist = mapping_results['alternative_matches'].value_counts().sort_index()
            axes[1, 1].bar(alt_match_dist.index, alt_match_dist.values)
            axes[1, 1].set_title('Alternative Matches Available')
            axes[1, 1].set_xlabel('Number of Alternatives')
            axes[1, 1].set_ylabel('Number of Records')
            
            plt.tight_layout()
            viz_output = generate_output_filename(args.output_dir, args.output_prefix, 'mapping_visualization.png')
            plt.savefig(viz_output, dpi=300, bbox_inches='tight')
            plt.close()
            
            print_progress(f"  ✓ Saved visualization to: {viz_output}", args.quiet)
        
        except ImportError:
            print_progress("  ⚠ Skipping visualization (matplotlib not available)", args.quiet)
        except Exception as e:
            print_progress(f"  ⚠ Visualization failed: {e}", args.quiet)
    
    # Final summary
    if not args.quiet:
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"\nOutput files saved to: {args.output_dir}")
        print(f"  1. {os.path.basename(main_output)} - Complete mapping results")
        print(f"  2. {os.path.basename(hc_output)} - High confidence mappings")
        if not args.no_review_list:
            print(f"  3. {os.path.basename(review_output)} - Items for manual review")
        print(f"  4. {os.path.basename(report_file)} - Statistical report")
        if not args.no_visualizations and 'viz_output' in locals():
            print(f"  5. {os.path.basename(viz_output)} - Visualization charts")
        
        print("\nNext Steps:")
        print(f"  1. Review high confidence matches in {os.path.basename(hc_output)}")
        if not args.no_review_list:
            print(f"  2. Manually review items in {os.path.basename(review_output)}")
        print(f"  3. Import validated mappings into your billing system")
        print("="*60 + "\n")
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
