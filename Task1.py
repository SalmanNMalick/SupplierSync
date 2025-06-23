# ############# Author SALMAN NAWAZ MALIK
# ############# Multiple Entries and Database Optimization
# ############# USING CSV product.csv

# Import required libraries
import pandas as pd
import re
from rapidfuzz import fuzz, process
import time

# Configuration dictionary to store file paths and settings,
# making it easy to update inputs, outputs, and thresholds without changing code logic.
CONFIG = {
    # File path to the existing product database CSV
    'existing_products_file': r'C:\Users\Salman\Desktop\WAREHOUSE\panga\Productsfile.csv',
    # File path to the supplier pricelist CSV to be matched against existing products
    'supplier_pricelist_file': r'C:\Users\Salman\Desktop\WAREHOUSE\panga\products.csv',
    # Output CSV file path where the matching results will be saved
    'output_file': r'C:\Users\Salman\Desktop\WAREHOUSE\panga\supplier_product_matched_results.csv',
    # Similarity threshold for fuzzy matching (0-100 scale), adjustable to control strictness
    'match_threshold': 90,
    # Required columns to be present in both datasets for successful matching
    'required_columns': ['id', 'name', 'MPN'],
}

print("Starting supplier product matching script...")

# Record the starting time to measure total script execution duration
start_time = time.time()

# Load existing product data into a pandas DataFrame with low_memory=False to avoid dtype guessing warnings
print(f"Loading existing products from {CONFIG['existing_products_file']}...")
existing_df = pd.read_csv(CONFIG['existing_products_file'], low_memory=False)

# Load supplier pricelist data similarly
print(f"Loading supplier pricelist from {CONFIG['supplier_pricelist_file']}...")
supplier_df = pd.read_csv(CONFIG['supplier_pricelist_file'], low_memory=False)

# Validate both DataFrames to ensure they contain all required columns before proceeding
for df, name in [(existing_df, "Existing Products"), (supplier_df, "Supplier Pricelist")]:
    missing_cols = [col for col in CONFIG['required_columns'] if col not in df.columns]
    if missing_cols:
        # Stop execution if critical columns are missing to prevent errors later
        raise ValueError(f"{name} missing required columns: {missing_cols}")

print("Cleaning datasets...")
for df in [existing_df, supplier_df]:
    # Drop rows where 'id' is missing because IDs are essential unique identifiers
    df.dropna(subset=['id'], inplace=True)
    # Ensure IDs are integers to maintain consistent data type for lookups
    df['id'] = df['id'].astype(int)

print(f"Existing products count: {len(existing_df)}")
print(f"Supplier products count: {len(supplier_df)}")

def normalize_mpn(text):
    """
    Normalize the Manufacturer Part Number (MPN) strings for consistent matching by:
    - Returning empty string for missing values to avoid errors
    - Converting all text to lowercase for case-insensitive comparison
    - Removing common prefixes/suffixes like 'mpn-', 'part-', 'sku-', and version tags like '-rev', '-v1'
    - Stripping out any characters other than alphanumeric to eliminate formatting differences like dashes, spaces, etc.
    """
    if pd.isna(text):
        return ''
    text = str(text).lower()
    # Regex removes known MPN prefixes and suffixes that don't affect identity
    text = re.sub(r'^(mpn-|part-|sku-)|(-rev|-v\d+)$', '', text)
    # Keep only letters and numbers to unify formatting (e.g., remove spaces, punctuation)
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

def normalize_name(text):
    """
    Normalize product names for flexible matching by:
    - Returning empty string if missing to prevent errors
    - Converting to lowercase to avoid case mismatch
    - Removing any characters other than letters, numbers, and spaces
    - Splitting the name into tokens, sorting them alphabetically, then rejoining
      This handles cases where word order differs but tokens are the same (token_set_ratio-friendly)
    """
    if pd.isna(text):
        return ''
    text = str(text).lower()
    # Strip out punctuation/special characters but keep spaces for tokenization
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Sort tokens alphabetically for consistent comparison regardless of word order
    return ' '.join(sorted(text.split()))

print("Normalizing MPNs and names...")
# Apply normalization functions to both existing and supplier datasets
existing_df['norm_mpn'] = existing_df['MPN'].apply(normalize_mpn)
existing_df['norm_name'] = existing_df['name'].apply(normalize_name)
supplier_df['norm_mpn'] = supplier_df['MPN'].apply(normalize_mpn)
supplier_df['norm_name'] = supplier_df['name'].apply(normalize_name)

print("Preparing lookup dictionaries...")
# Create dictionaries keyed by product 'id' for quick normalized MPN and name lookups
id_to_norm_mpn = existing_df.set_index('id')['norm_mpn'].to_dict()
id_to_norm_name = existing_df.set_index('id')['norm_name'].to_dict()

# Extract lists of normalized MPNs, names, and corresponding IDs for rapid fuzzy matching
mpn_list = list(id_to_norm_mpn.values())
name_list = list(id_to_norm_name.values())
id_list = list(id_to_norm_mpn.keys())

print("Starting matching process...")
matches = []  # List to collect results of matching for each supplier product

# Iterate over each supplier product row for matching
for idx, row in supplier_df.iterrows():
    supplier_mpn_norm = row['norm_mpn']
    supplier_name_norm = row['norm_name']

    matched_id = None  # Holds matched existing product ID if found
    match_score = 0    # Similarity score of the match
    match_type = None  # Describes type of match (exact, fuzzy, etc.)

    # 1) Attempt exact match on normalized MPN first (most reliable match)
    if supplier_mpn_norm and supplier_mpn_norm in id_to_norm_mpn.values():
        # Find all existing product IDs matching this normalized MPN
        matched_ids = [k for k, v in id_to_norm_mpn.items() if v == supplier_mpn_norm]
        if len(matched_ids) == 1:
            # Unique exact MPN match found
            matched_id = matched_ids[0]
            match_score = 100  # Perfect match
            match_type = "Exact MPN"
        else:
            # Multiple matches found — ambiguous; log and skip this product to avoid incorrect matching
            match_type = "Multiple MPN matches"
            print(f"[{idx}] Multiple exact MPN matches for Supplier ID {row['id']}: {matched_ids}")
            continue  # Skip to next supplier product

    # 2) If no exact MPN match, try fuzzy matching on MPN using ratio similarity metric
    if not matched_id and supplier_mpn_norm:
        best_mpn_match = process.extractOne(
            supplier_mpn_norm,
            mpn_list,
            scorer=fuzz.ratio,
            score_cutoff=CONFIG['match_threshold'],  # Only accept matches above threshold
            processor=None
        )
        if best_mpn_match:
            # Get matched existing product ID by locating the matched normalized MPN's index
            matched_id = id_list[mpn_list.index(best_mpn_match[0])]
            match_score = best_mpn_match[1]
            match_type = "Fuzzy MPN"

    # 3) If MPN matching fails, fallback to fuzzy matching on normalized product name using token set ratio
    if not matched_id and supplier_name_norm:
        best_name_match = process.extractOne(
            supplier_name_norm,
            name_list,
            scorer=fuzz.token_set_ratio,
            score_cutoff=CONFIG['match_threshold'],
            processor=None
        )
        if best_name_match:
            matched_id = id_list[name_list.index(best_name_match[0])]
            match_score = best_name_match[1]
            match_type = "Fuzzy Name"

    # Log the match results for transparency and debugging
    if matched_id:
        print(f"[{idx}] {match_type} match (Score: {match_score}): Supplier ID {row['id']} -> Matched ID {matched_id}")
    else:
        print(f"[{idx}] No match found for Supplier ID {row['id']}")

    # Prepare dictionary of match info to save, including supplier product details and match results
    match_data = {
        'SupplierProductID': row['id'],
        'SupplierProductName': row['name'],
        'SupplierMPN': row['MPN'],
        'MatchedProductID': matched_id,
        'MatchScore': match_score,
        'MatchType': match_type or "No Match",
    }

    # Also include any additional columns from the supplier pricelist to keep context (e.g., price, stock)
    for col in supplier_df.columns:
        if col not in CONFIG['required_columns'] + ['norm_mpn', 'norm_name']:
            match_data[f'Supplier_{col}'] = row.get(col)

    # Append the match result to the results list
    matches.append(match_data)

print("Matching complete. Saving results...")
# Convert match results to a DataFrame for export
match_df = pd.DataFrame(matches)

# Save the results as a CSV file without the DataFrame index
match_df.to_csv(CONFIG['output_file'], index=False)

print(f"Results saved to {CONFIG['output_file']}")
# Display total execution time in seconds
print(f"Total time elapsed: {time.time() - start_time:.2f} seconds")
